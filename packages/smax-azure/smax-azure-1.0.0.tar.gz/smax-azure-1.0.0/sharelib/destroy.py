import os
from argparse import Namespace

from pieterraform import Terraform

from .base_infra_act import BaseInfraAct


class Destroy(BaseInfraAct):
    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return "destroy"

    @property
    def help(self):
        return "Destroy all infra on cloud"

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        logger = self.logger
        logger.info("existing infra => ")
        logger.info(os.linesep * 2)
        logger.info(self.infra_info.as_table())
        self.keys_folder.joinpath("id_rsa").touch()
        self.keys_folder.joinpath("id_rsa.pub").touch()

    def the_act(self, args: Namespace):
        logger = self.logger
        logger.info("Deleting terraform infra")
        destroyer = (
            Terraform(logger=logger)
            .workdir(self.tf_dir)
            .destroy()
            .auto_approve()
        )
        for item in args.tf_vars:
            (k, v) = item.split("=")
            destroyer.var(k, v)
        destroyer.run()
