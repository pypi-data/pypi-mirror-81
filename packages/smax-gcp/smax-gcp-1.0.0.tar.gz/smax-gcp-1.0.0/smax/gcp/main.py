from sharelib.gcp.gcp_program import GcpProgram
from .install import Install
from .uninstall import Uninstall

__version__ = "0.0.1"
__program__ = "smax-gcp"


class MyProgram(GcpProgram):
    @property
    def version(self) -> str:
        return __version__

    @property
    def program_name(self) -> str:
        return __program__

    def add_subcommands(self):
        super().add_subcommands()
        self.simple_parser.add_sub_cmd(Install())
        self.simple_parser.add_sub_cmd(Uninstall())

    @property
    def module(self) -> str:
        return __file__


def main():
    MyProgram().run()


if __name__ == "__main__":
    main()
