import os
from argparse import ArgumentParser, Namespace

from pieterraform import TfVars
from tabulate import tabulate

from sharelib.base_act import BaseAct


class Show(BaseAct):
    @property
    def name(self):
        return "tfshow"

    @property
    def help(self):
        return "Inspect infra"

    def args(self, parser: ArgumentParser):
        parser.add_argument(
            "-c",
            "--class",
            dest="target",
            choices=["config", "infra"],
            type=str,
            default="config",
            required=False,
        )

    def the_act(self, args: Namespace):
        if args.target == "config":
            config_names = []
            if args.tf_config_name == "all":
                for d in self.tf_dir.glob("*"):
                    if d.is_dir():
                        config_names.append(d.name)
            else:
                config_names = [args.tf_config_name]
            table = []
            for name in config_names:
                d = args.tf_dir.joinpath(name)
                if d.is_dir():
                    help = ""
                    if d.joinpath("README.md").exists():
                        with d.joinpath("README.md").open("r") as f:
                            help = f.read()
                    vars = ""
                    for v in TfVars(d, "variables.tf").vars.values():
                        vars = (
                            vars + f"{v.name}(default:{v.default})" + os.linesep
                        )
                    table.append((name, help, vars))
            print(
                tabulate(
                    table,
                    headers=["Config", "Description", "Vars"],
                    tablefmt="grid",
                )
            )
        if args.target == "infra":
            log = self.logger
            self.logger = None
            print(os.linesep + self.infra_info.as_table())
            self.logger = log
