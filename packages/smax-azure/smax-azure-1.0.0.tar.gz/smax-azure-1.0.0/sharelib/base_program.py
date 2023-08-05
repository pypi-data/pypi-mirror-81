import logging
import os
from abc import ABC, abstractmethod
from argparse import Namespace

from .simple_arg_parser import SimpleArgParser
from .utility import set_log


class BaseProgram(ABC):
    def __init__(self):
        self.simple_parser = SimpleArgParser()

    @property
    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def program_name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def module(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def add_subcommands(self):
        raise NotImplementedError()

    @property
    def default_tf_config_name(self):
        return "test"

    def add_common_args(self):
        parser = self.simple_parser.parser
        parser.add_argument(
            "--version",
            action="version",
            version=f"{self.program_name} {self.version}",
        )
        deployment_id = (
            os.environ["DEPLOYMENT_ID"]
            if "DEPLOYMENT_ID" in os.environ
            else "testonly"
        )
        backend_user = (
            os.environ["ARTIFACT_USER"] if "ARTIFACT_USER" in os.environ else ""
        )
        backend_password = (
            os.environ["ARTIFACT_PWD"] if "ARTIFACT_PWD" in os.environ else ""
        )
        parser.add_argument(
            "-x",
            "--deployment-id",
            dest="deployment_id",
            help="id to mark provision, install and destroy"
            "by default use env: DEPLOYMENT_ID",
            default=deployment_id,
            type=str,
            required=True if not deployment_id else False,
        )

        parser.add_argument(
            "-atu",
            "--artifact-user",
            dest="artifact_user",
            help="terraform backend(artifactory) user"
            "by default use env: ARTIFACT_USER",
            type=str,
            default=backend_user,
            required=True if not backend_user else False,
        )

        parser.add_argument(
            "-atp",
            "--artifact-password",
            dest="artifact_password",
            help="terraform backend(artifactory) password"
            "by default use env: ARTIFACT_PWD",
            type=str,
            default=backend_password,
            required=True if not backend_password else False,
        )

        parser.add_argument(
            "--color-log",
            dest="color_log",
            action="store_true",
            help="Use color log",
            default=False,
        )
        parser.add_argument(
            "--no-cache",
            dest="no_cache",
            action="store_true",
            help="clean after run",
            default=False,
        )
        parser.add_argument(
            "--debug",
            dest="debug_log",
            action="store_true",
            help="Output log in debug level",
            default=False,
        )

        parser.add_argument(
            "-t",
            "--tf-config-name",
            dest="tf_config_name",
            help="terraform config name",
            type=str,
            default=self.default_tf_config_name,
            required=False,
        )

    def pre_run(self, args: Namespace):
        args.program_info = ProgramInfo(
            self.program_name,
            self.module,
            set_log(
                use_color=args.color_log,
                verbose=args.debug_log,
                name=self.program_name,
            ),
        )

    def run(self):
        self.add_common_args()
        self.add_subcommands()
        self.pre_run(self.simple_parser.parse())
        self.simple_parser.execute_sub()


class ProgramInfo:
    def __init__(self, name: str, module: str, logger: logging):
        self.name = name
        self.module = module
        self.logger = logger
