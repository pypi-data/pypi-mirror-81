import os
import logging
import pathlib
from abc import ABC, abstractmethod
from argparse import Namespace
from distutils.dir_util import copy_tree, remove_tree

from pieterraform import Terraform

from .base_program import ProgramInfo
from .infra_info import InfraInfo
from .simple_arg_parser import SimpleSubCmdIf


class BaseAct(SimpleSubCmdIf, ABC):
    def __init__(self):
        self.deployment_id = ""
        self.program_parent = None
        self.program_name = ""
        self._infra_info = None
        self.tf_inited = False
        self.artifact_user = None
        self.artifact_pwd = None
        self.logger: logging = None

    @property
    def infra_info(self):
        if self._infra_info:
            return self._infra_info
        self._infra_info = self.__get_infra_info__()
        logger = self.logger
        if logger:
            logger.debug("found infra => ")
            logger.debug(os.linesep + self._infra_info.as_table())
        return self._infra_info

    @property
    def context_dir(self):
        return pathlib.Path(
            f".context.{self.program_name}.{self.deployment_id}"
        )

    @property
    def tf_dir(self):
        return self.context_dir.joinpath("tf")

    @property
    def backend_config_file(self):
        return self.program_parent.joinpath("backend.config")

    def __get_infra_info__(self, showlog=True) -> InfraInfo:
        logger = self.logger
        if not showlog:
            logger = None
        context = Terraform(logger=logger).workdir(str(self.tf_dir))
        if not self.tf_inited:
            (
                context.init()
                .reconfigure()
                .backend_config(str(self.backend_config_file))
                .backend_config(f"username={self.artifact_user}")
                .backend_config(f"password={self.artifact_pwd}")
                .backend_config(
                    f"subpath={self.program_name}.{self.deployment_id}"
                )
                .no_color()
                .run()
            )
            self.tf_inited = True
        if logger:
            logger.info("fetching infra info...")
        context._logger = None
        output_json_str = str.join(
            "", context.output().json().run().last_result.output
        )
        return InfraInfo(output_json_str)

    def pre_act(self, args: Namespace):
        i: ProgramInfo = args.program_info
        self.logger = i.logger
        self.program_name = i.name
        self.program_parent = pathlib.Path(i.module).parents[0]
        self.deployment_id = args.deployment_id
        self.artifact_user = args.artifact_user
        self.artifact_pwd = args.artifact_password
        source_config = self.program_parent.joinpath(".tfconfig").joinpath(
            args.tf_config_name
        )
        copy_tree(str(source_config), str(self.tf_dir))

    def post_act(self, args: Namespace):
        if args.no_cache:
            remove_tree(self.context_dir)

    @abstractmethod
    def the_act(self, args: Namespace):
        raise NotImplementedError()

    def act(self, args: Namespace):
        try:
            self.pre_act(args)
            self.the_act(args)
        finally:
            self.post_act(args)
