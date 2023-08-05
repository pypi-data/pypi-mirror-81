import shutil
from argparse import ArgumentParser
from sharelib.base_install import BaseInstall


class WuKongInstall(BaseInstall):
    @property
    def name(self):
        return "install-wukong"

    @property
    def help(self):
        return "Install WuKong to Gcp"

    def args(self, sub_parser: ArgumentParser):
        super().args(sub_parser)
        sub_parser.add_argument(
            "--size",
            dest="size",
            default="small",
            type=str,
            required=False,
        )

    def the_act(self, args):
        super().the_act(args)
        self.run_in_bastion("./install-wukong.sh")
        self.logger.info("WuKong Installed!")
