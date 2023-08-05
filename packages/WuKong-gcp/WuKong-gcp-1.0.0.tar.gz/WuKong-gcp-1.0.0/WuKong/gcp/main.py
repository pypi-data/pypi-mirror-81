from sharelib.gcp.gcp_program import GcpProgram
from .install import WuKongInstall


class MyProgram(GcpProgram):
    @property
    def version(self) -> str:
        return "1.0.0"  # Your program's version

    @property
    def program_name(self) -> str:
        return "wukong-gcp"  # Your program's name

    def add_subcommands(self):
        super().add_subcommands()
        self.simple_parser.add_sub_cmd(WuKongInstall())

    @property
    def module(self) -> str:
        return __file__


def main():  # MUST HAVE!!
    MyProgram().run()


if __name__ == "__main__":
    main()
