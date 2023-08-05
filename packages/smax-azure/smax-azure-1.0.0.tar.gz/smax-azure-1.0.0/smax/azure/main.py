from sharelib.azure.azure_program import AzureProgram
from .install import Install

__version__ = "0.0.1"
__program__ = "smax-azure"


class MyProgram(AzureProgram):
    @property
    def version(self) -> str:
        return __version__

    @property
    def program_name(self) -> str:
        return __program__

    def add_subcommands(self):
        super().add_subcommands()
        self.simple_parser.add_sub_cmd(Install())

    @property
    def module(self) -> str:
        return __file__


def main():
    MyProgram().run()


if __name__ == "__main__":
    main()
