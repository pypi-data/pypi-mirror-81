import pathlib
import shutil
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from argparse import Namespace

from pieterraform import TfVars

from .base_act import BaseAct


class BaseInfraAct(BaseAct, ABC):
    def __init__(self):
        super().__init__()

    @property
    def keys_folder(self):
        v = pathlib.Path(self.tf_dir).joinpath("keys")
        v.mkdir(parents=True, exist_ok=True)
        return v

    @property
    def svc_key_file(self):
        return "svc-key.json"

    @property
    def svc_key_file_path(self):
        return self.keys_folder.joinpath(self.svc_key_file)

    @property
    def backend_config_file(self):
        return self.program_parent.joinpath("backend.config")

    def args(self, sub_parser: ArgumentParser):
        sub_parser.add_argument(
            "-k",
            "--account-key-file",
            dest="svc_key_file",
            help="service account key file in json format",
            type=str,
            default=f"./keys/{self.svc_key_file}",
            required=False,
        )

        sub_parser.add_argument(
            "-var",
            "--tf-var",
            dest="tf_vars",
            action="append",
            help="Extra vars passed to terraform in <key>=<value>",
            default=[],
            required=False,
        )

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        svc_key = pathlib.Path(args.svc_key_file)
        if not svc_key.exists() or str(svc_key.absolute()) != str(
            self.svc_key_file_path.absolute()
        ):
            shutil.copy(svc_key, self.svc_key_file_path)

        if (
            hasattr(args, "tf_vars")
            and "context_folder"
            in TfVars(self.tf_dir, "variables.tf").vars.keys()
        ):
            args.tf_vars.append(f"context_folder={str(self.context_dir)}")

    @abstractmethod
    def the_act(self, args: Namespace):
        raise NotImplementedError()

    def act(self, args: Namespace):
        try:
            self.pre_act(args)
            self.the_act(args)
        finally:
            pass
            # self.post_act(args)
