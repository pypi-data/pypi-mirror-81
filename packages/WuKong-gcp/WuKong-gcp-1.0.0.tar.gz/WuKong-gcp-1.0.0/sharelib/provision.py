import os
import pathlib
import shutil
from argparse import Namespace, ArgumentParser

from pieterraform import Terraform

from .base_infra_act import BaseInfraAct
from .ssh_gen import generate_ssh_keys


class Provision(BaseInfraAct):
    @property
    def name(self):
        return "provision"

    @property
    def help(self):
        return "Create all infra on cloud"

    def args(self, sub_parser: ArgumentParser):
        super().args(sub_parser)
        sub_parser.add_argument(
            "-sk",
            "--ssh-key-private",
            dest="ssh_private_key",
            help="SSH private key file used to access bastion"
            "SSH pub key file must be in same path and named with .pub"
            "e.g. private key file passed in is ./id_rsa, "
            "then public key file MUST be ./id_rsa.pub",
            type=str,
            default=None,
            required=False,
        )

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        ssh_private_key = (
            pathlib.Path(args.ssh_private_key) if args.ssh_private_key else None
        )

        args.auto_ssh_key = False
        if not ssh_private_key:
            args.auto_ssh_key = True

        private_key_target = self.keys_folder.joinpath("id_rsa")
        public_key_target = self.keys_folder.joinpath("id_rsa.pub")
        if not args.auto_ssh_key:
            if not ssh_private_key.exists() or str(
                ssh_private_key.absolute()
            ) != str(private_key_target.absolute()):
                shutil.copy(ssh_private_key, private_key_target)
            ssh_public_key = ssh_private_key.parents[0].joinpath(
                f"{ssh_private_key.name}.pub"
            )
            if not ssh_public_key.exists() or str(
                ssh_public_key.absolute()
            ) != str(public_key_target.absolute()):
                shutil.copy(ssh_public_key, public_key_target)
        else:
            logger = self.logger
            if self.infra_info.has("ssh_private_key") and self.infra_info.has(
                "ssh_public_key"
            ):
                logger.debug("Get existing ssh keys")
                private_key = self.infra_info.data.ssh_private_key.encode(
                    "utf-8"
                )
                public_key = self.infra_info.data.ssh_public_key.encode("utf-8")
            else:
                logger.debug("Generate ssh keys automatically")
                private_key, public_key = generate_ssh_keys()
            if private_key_target.exists():
                private_key_target.unlink()
            with private_key_target.open("wb") as f:
                f.write(private_key)
            os.chmod(private_key_target, 0o400)
            if public_key_target.exists():
                public_key_target.unlink()
            with public_key_target.open("wb") as f:
                f.write(public_key)

    def the_act(self, args: Namespace):
        logger = self.logger
        context = Terraform(logger=logger).workdir(self.tf_dir)
        planner = (
            context.plan()
            .no_color()
            .out("xplan")
            .var("resource_prefix", args.deployment_id)
        )
        for item in args.tf_vars:
            (k, v) = item.split("=")
            planner.var(k, v)
        planner.run()
        context.apply().no_color().use_plan("xplan").run()
        logger.debug("infra built => ")
        logger.debug(os.linesep + self.infra_info.as_table())
        logger.info(
            f"Finished. Your deployment id is: {args.deployment_id} \n"
            f"Next: try to install suite by: \n"
            f"{self.program_name} -x {args.deployment_id} install"
        )
