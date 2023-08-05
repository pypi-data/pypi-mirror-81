import argparse
import collections
import json
import logging
import os
import sys
from pathlib import Path

import sagemaker
from sagemaker.inputs import TrainingInput

from . import constants
from .sm_project import SageMakerProject

logger = logging.getLogger(__name__)


def fileValidation(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    return arg


def fileOrS3Validation(parser, arg):
    if not arg.startswith("s3://") and not os.path.exists(arg):
        parser.error("%s has to be either a file or a s3 path!" % arg)
    return arg


InputTuple = collections.namedtuple("Input", ("path", "distribution"))
Input_S3Tuple = collections.namedtuple(
    "Input_S3", ("input_name", "s3_uri", "distribution")
)
Input_Task_Tuple = collections.namedtuple(
    "Input_Task", ("input_name", "task_name", "type", "distribution")
)


def help_for_input_type(tuple, additional_text=""):
    field_names = " ".join([x.upper() for x in tuple._fields[:-1]])
    res = f"{tuple.__name__.upper()}: {field_names} [distribution]"
    if additional_text:
        res += "\n" + additional_text
    return res


class InputActionBase(argparse.Action):
    def __init__(self, option_strings, dest, tuple, nargs=None, **kwargs):
        self.__nargs = len(tuple._fields)
        self.__tuple = tuple
        super(InputActionBase, self).__init__(option_strings, dest, "+", **kwargs)

    def __append__(self, args, values):
        dist_options = ["FullyReplicated", "ShardedByS3Key"]
        default_dist = "FullyReplicated"
        if len(values) == self.__nargs - 1:
            values.append(default_dist)
        elif len(values) == self.__nargs:
            if values[-1] not in dist_options:
                raise argparse.ArgumentTypeError(
                    f"distribution has to be one of {dist_options}"
                )
        else:
            raise argparse.ArgumentTypeError(
                f"{self.dest} has to contain {self.__nargs}/{self.__nargs-1} arguments, got {values}"
            )
        value = self.__tuple(*values)
        if not args.__getattribute__(self.dest):
            setattr(args, self.dest, [value])
        else:
            args.__getattribute__(self.dest).append(value)


class InputAction(InputActionBase):
    def __call__(self, parser, args, values, option_string=None):
        if not os.path.exists(values[0]) and not values[0].startswith("s3://"):
            raise ValueError(f"{values[1]} has to be a local/s3 path!")

        self.__append__(args, values)


class Input_S3Action(InputActionBase):
    def __call__(self, parser, args, values, option_string=None):
        if not values[1].startswith("s3://"):
            raise ValueError(f"{values[1]} has to be a s3 path!")

        self.__append__(args, values)


Input_Task_Types = ["state", "model", "source", "output"]


class Input_Task_Action(InputActionBase):
    def __call__(self, parser, args, values, option_string=None):
        # print (f'{args} {values} {option_string}')
        # print("****", values, hasattr(args, self.dest))
        if values[2] not in Input_Task_Types:
            raise ValueError(f"{values[2]} has to be one of {Input_Task_Types}!")
        self.__append__(args, values)


def addDownloadArgs(download_params):
    download_params.add_argument(
        "--output_path",
        "-o",
        default=None,
        help="Local path to download the outputs to.",
    )
    download_params.add_argument(
        "--download_state",
        default=False,
        action="store_true",
        help="Download the state once task is finished",
    )
    download_params.add_argument(
        "--download_model",
        default=False,
        action="store_true",
        help="Download the model once task is finished",
    )
    download_params.add_argument(
        "--download_output",
        default=False,
        action="store_true",
        help="Download the output once task is finished",
    )


def runArguments(run_parser, shell=False):
    if shell:
        run_parser.set_defaults(func=shellHandler)
    else:
        run_parser.set_defaults(func=runHandler)

    code_group = run_parser.add_argument_group("Code")
    instance_group = run_parser.add_argument_group("Instance")
    image_group = run_parser.add_argument_group("Image")
    running_params = run_parser.add_argument_group("Running")
    IO_params = run_parser.add_argument_group("I/O")
    download_params = run_parser.add_argument_group("Download")

    # general
    # parser.add("--config-file", "-c", is_config_file=True, help="Config file path.")
    run_parser.add_argument("--project_name", "-p", required=True, help="Project name.")
    run_parser.add_argument("--task_name", "-t", required=True, help="Task name.")
    IO_params.add_argument(
        "--bucket_name",
        "-b",
        help="S3 bucket name (a default one is used if not given).",
    )

    if shell:
        code_group.add_argument(
            "--cmd_line",
            "--cmd",
            help="""The command line to run.""",
        )
        code_group.add_argument(
            "--dir_files",
            help="""Path to a directory with files that are expected to be in root folder where cmd_line is executed.
            Note: this is intended to be used for shell script / small files. Input data should be given with relevant
            other parameters).""",
        )
    else:
        # coding params
        code_group.add_argument(
            "--source_dir",
            "-s",
            type=lambda x: fileValidation(run_parser, x),
            help="""Path (absolute, relative or an S3 URI) to a directory with any other source
            code dependencies aside from the entry point file. If source_dir is an S3 URI,
            it must point to a tar.gz file. Structure within this directory are preserved when running on Amazon SageMaker.""",
        )
        code_group.add_argument(
            "--entry_point",
            "-e",
            required=True,
            # type=lambda x: fileValidation(parser, x),
            help="""Path (absolute or relative) to the local Python source file which should be executed as the entry point.
            If source_dir is specified, then entry_point must point to a file located at the root of source_dir.""",
        )
    code_group.add_argument(
        "--dependencies",
        "-d",
        nargs="+",
        type=lambda x: fileValidation(run_parser, x),
        help="""A list of paths to directories (absolute or relative) with any additional libraries that will be exported to the container
        The library folders will be copied to SageMaker in the same folder where the entrypoint is copied.""",
    )
    # instance params
    instance_group.add_argument(
        "--instance_type",
        "--it",
        default=constants.DEFAULT_INSTANCE_TYPE,
        help="Type of EC2 instance to use.",
    )
    instance_group.add_argument(
        "--instance_count",
        "--ic",
        type=int,
        default=constants.DEFAULT_INSTANCE_COUNT,
        help="Number of EC2 instances to use.",
    )
    instance_group.add_argument(
        "--volume_size",
        "-v",
        type=int,
        default=constants.DEFAULT_VOLUME_SIZE,
        help="""Size in GB of the EBS volume to use for storing input data.
        Must be large enough to store input data.""",
    )
    instance_group.add_argument(
        "--no_spot",
        dest="use_spot_instances",
        action="store_false",
        help="Use on demand instances",
    )
    instance_group.add_argument(
        "--use_spot_instances",
        dest="use_spot_instances",
        action="store_true",
        help="""Specifies whether to use SageMaker Managed Spot instances.""",
    )
    instance_group.set_defaults(use_spot_instances=constants.DEFAULT_USE_SPOT)
    instance_group.add_argument(
        "--max_wait_mins",
        type=int,
        default=constants.DEFAULT_MAX_WAIT,
        help="""Timeout in minutes waiting for spot instances.
        After this amount of time Amazon SageMaker will stop waiting for Spot instances to become available.
        If 0 is specified and spot instances are used, it's set to max_run_mins""",
    )
    instance_group.add_argument(
        "--max_run_mins",
        type=int,
        default=constants.DEFAULT_MAX_RUN,
        help="""Timeout in minutes for running.
        After this amount of time Amazon SageMaker terminates the job regardless of its current status.""",
    )
    # image params
    image_group.add_argument("--aws_repo_name", "--ar", help="Name of ECS repository.")
    image_group.add_argument("--repo_name", "--rn", help="Name of local repository.")
    image_group.add_argument(
        "--image_tag", default=constants.DEFAULT_REPO_TAG, help="Image tag."
    )
    image_group.add_argument(
        "--docker_file_path_or_content",
        "--df",
        help="""Path to a directory containing the DockerFile. The base image should be set to
        `__BASE_IMAGE__` within the Dockerfile, and is automatically replaced with the correct base image.""",
    )
    image_group.add_argument(
        "--framework",
        "-f",
        help="The framework to use, see https://github.com/aws/deep-learning-containers/blob/master/available_images.md",
        choices=["pytorch", "tensorflow"],
        default="pytorch",
    )
    image_group.add_argument(
        "--framework_version",
        "--fv",
        help="The framework version",
    )
    image_group.add_argument(
        "--py_version",
        "--pv",
        help="The python version",
    )
    # run params
    IO_params.add_argument(
        "--input_path",
        "-i",
        action=InputAction,
        help=help_for_input_type(
            InputTuple,
            """Local/s3 path for the input data. If a local path is given, it will be sync'ed to the task
            folder on the selected S3 bucket before launching the task.""",
        ),
        tuple=InputTuple,
    )
    IO_params.add_argument(
        "--model_uri",
        help="""URI where a pre-trained model is stored, either locally or in S3.
            If specified, the estimator will create a channel pointing to the model so the training job can
            download it. This model can be a ‘model.tar.gz’ from a previous training job, or other artifacts
            coming from a different source.""",
    )
    IO_params.add_argument(
        "--input_s3",
        "--iis",
        action=Input_S3Action,
        help=help_for_input_type(
            Input_S3Tuple, "Additional S3 input sources (a few can be given)."
        ),
        tuple=Input_S3Tuple,
    )
    IO_params.add_argument(
        "--input_task",
        "--iit",
        action=Input_Task_Action,
        help=help_for_input_type(
            Input_Task_Tuple,
            f"""Use an output of a completed task in the same project as an input source (a few can be given).
            Type should be one of {Input_Task_Types}.""",
        ),
        tuple=Input_Task_Tuple,
    )
    running_params.add_argument(
        "--force_running",
        default=False,
        action="store_true",
        help="Force running the task even if it's already completed.",
    )
    running_params.add_argument(
        "--distribution",
        help="""Tensorflows' distribution policy, see
        https://sagemaker.readthedocs.io/en/stable/frameworks/tensorflow/using_tf.html#distributed-training.""",
        type=lambda x: json.loads(x),
    )
    IO_params.add_argument(
        "--clean_state",
        "--cs",
        default=False,
        action="store_true",
        help="Clear the task state before running it. The task will be running again even if it was already completed before.",
    )
    IO_params.add_argument(
        "--keep_state",
        "--ks",
        action="store_false",
        dest="clean_state",
        help="Keep the current task state. If the task is already completed, its current output will \
             be taken without running it again.",
    )
    IO_params.add_argument(
        "--metric_definitions",
        "--md",
        nargs=2,
        metavar=("name", "regexp"),
        action="append",
        help="Name and regexp for a metric definition, a few can be given. \
            See https://docs.aws.amazon.com/sagemaker/latest/dg/training-metrics.html.",
    )
    IO_params.add_argument(
        "--enable_sagemaker_metrics",
        "-m",
        default=False,
        action="store_true",
        help="Enables SageMaker Metrics Time Series. \
            See https://docs.aws.amazon.com/sagemaker/latest/dg/training-metrics.html.",
    )
    running_params.add_argument(
        "--tag",
        nargs=2,
        metavar=("key", "value"),
        action="append",
        help="Tag to be attached to the jobs executed for this task.",
    )
    addDownloadArgs(download_params)


def dataArguments(data_parser):
    data_parser.add_argument(
        "--project_name", "-p", required=True, help="Project name."
    )
    data_parser.add_argument("--task_name", "-t", required=True, help="Task name.")
    data_parser.add_argument(
        "--bucket_name",
        "-b",
        help="S3 bucket name (a default one is used if not given).",
    )
    data_parser.add_argument(
        "--clean_state",
        "--cs",
        default=False,
        action="store_true",
        help="Clean the task state.",
    )
    data_parser.set_defaults(func=dataHandler)
    addDownloadArgs(data_parser)


def parseArgs():
    parser = argparse.ArgumentParser(
        # config_file_parser_class=configargparse.DefaultConfigFileParser,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers()
    run_parser = subparsers.add_parser("run", help="Run a task")
    shell_parser = subparsers.add_parser("shell", help="Run a command line task")
    data_parser = subparsers.add_parser("data", help="Manage task data")

    runArguments(run_parser)
    runArguments(shell_parser, True)
    dataArguments(data_parser)

    args, rest = parser.parse_known_args()
    return args, rest


def addParam(args, argName, paramName, params):
    if hasattr(args, argName):
        arg = args.__getattribute__(argName)
        if arg is not None:
            params[paramName] = arg


def getAllParams(args, mapping):
    params = dict()
    for k, v in mapping.items():
        addParam(args, k, v, params)
    return params


def parseInputsAndAllowAccess(args, sm_project):
    input_data_path = None
    distribution = "FullyReplicated"
    if args.input_path:
        input_data_path, distribution = args.input_path[0]

    inputs = dict()
    if args.input_task:
        for (input_name, task_name, ttype, distribution) in args.input_task:
            inputs[input_name] = sm_project.getInputConfig(
                task_name, ttype, distribution=distribution
            )
    if args.input_s3:
        for (input_name, s3_uri, distribution) in args.input_s3:
            bucket, _ = sagemaker.s3.parse_s3_url(s3_uri)
            sm_project.allowAccessToS3Bucket(bucket)
            inputs[input_name] = TrainingInput(s3_uri, distribution=distribution)

    return input_data_path, distribution, inputs


def parseHyperparams(rest):
    res = dict()
    for i in range(0, len(rest), 2):
        res[rest[i].strip("-")] = rest[i + 1]
    return res


def shellHandler(args, rest):
    shell_launcher = Path(__file__).parent / "shell_launcher.py"
    rest.extend(["--SSM_CMD_LINE", args.cmd_line])

    if args.dir_files:
        if not args.dependencies:
            args.dependencies = list()
        files = [str(x) for x in Path(args.dir_files).glob("*")]
        args.dependencies.extend(files)

    args.entry_point = str(shell_launcher)
    runHandler(args, rest)


def runHandler(args, rest):
    code_params = getAllParams(
        args,
        {
            "project_name": "project_name",
            "bucket_name": "bucket_name",
        },
    )
    if "local" in args.instance_type:
        code_params["local_mode"] = True
    sm_project = SageMakerProject(**code_params)

    sm_project.setDefaultCodeParams(
        **getAllParams(
            args,
            {
                "source_dir": "source_dir",
                "entry_point": "entry_point",
                "dependencies": "dependencies",
            },
        )
    )
    sm_project.setDefaultInstanceParams(
        **getAllParams(
            args,
            {
                "instance_count": "instance_count",
                "instance_type": "instance_type",
                "volume_size": "volume_size",
                "use_spot_instances": "use_spot_instances",
                "max_run_mins": "max_run_mins",
                "max_wait_mins": "max_wait_mins",
            },
        )
    )
    sm_project.setDefaultImageParams(
        **getAllParams(
            args,
            {
                "aws_repo_name": "aws_repo_name",
                "repo_name": "repo_name",
                "image_tag": "image_tag",
                "docker_file_path_or_content": "docker_file_path_or_content",
                "framework": "framework",
                "framework_version": "framework_version",
                "py_version": "py_version",
            },
        )
    )

    image_uri = sm_project.buildOrGetImage(
        instance_type=sm_project.defaultInstanceParams.instance_type
    )

    running_params = getAllParams(
        args,
        {
            "clean_state": "clean_state",
            "enable_sagemaker_metrics": "enable_sagemaker_metrics",
            "force_running": "force_running",
            "distribution": "distribution",
            "model_uri": "model_uri",
        },
    )

    input_data_path, input_distribution, inputs = parseInputsAndAllowAccess(
        args, sm_project
    )
    hyperparameters = parseHyperparams(rest)
    tags = {} if args.tag is None else {k: v for (k, v) in args.tag}
    metric_definitions = (
        {}
        if args.metric_definitions is None
        else {k: v for (k, v) in args.metric_definitions}
    )

    sm_project.runTask(
        args.task_name,
        image_uri,
        hyperparameters=hyperparameters,
        input_data_path=input_data_path,
        input_distribution=input_distribution,
        additional_inputs=inputs,
        tags=tags,
        metric_definitions=metric_definitions,
        **running_params,
    )

    if args.output_path:
        sm_project.downloadResults(
            args.task_name,
            args.output_path,
            logs=True,
            state=args.download_state,
            model=args.download_model,
            output=args.download_output,
        )


def dataHandler(args, rest):
    sm_project = SageMakerProject(
        **getAllParams(
            args,
            {
                "project_name": "project_name",
                "bucket_name": "bucket_name",
            },
        )
    )
    if args.clean_state:
        sm_project.cleanState(args.task_name)
    if args.output_path:
        sm_project.downloadResults(
            args.task_name,
            args.output_path,
            logs=True,
            state=args.download_state,
            model=args.download_model,
            output=args.download_output,
        )


def main():
    format = "%(levelname)-.1s [%(asctime)s][%(name)-.30s] %(message)s"
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=format,
    )
    logger.info(f"Running ssm cli, args:{sys.argv}")
    args, rest = parseArgs()
    args.func(args, rest)


if __name__ == "__main__":
    main()
