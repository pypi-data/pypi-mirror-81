import os
import pathlib
from argparse import ArgumentParser, Namespace
from distutils.dir_util import copy_tree

from fabric import Connection

from sharelib.base_act import BaseAct
from sharelib.utility import (
    get_suite_base_ver,
    download_or_copy,
    get_cdf_version,
)


class BaseInstall(BaseAct):
    def __init__(self):
        super().__init__()
        self._bastion_connect = None
        self.remote_dir = "/tmp/suite-install/"
        self.time_out = 3 * 3 * 60
        self.cdf_pkg_name = None
        self.suite_metadata_pkg_name = None
        self.__ch_exist = False

    @property
    def name(self):
        return "install"

    @property
    def help(self):
        return "Install Suite on existing infra"

    @property
    def install_script_folder(self):
        return self.program_parent.joinpath("install-script")

    @property
    def secret_ns_name(self):
        return "u-r-fool"

    @property
    def suite_ns_name(self):
        return f"itsma-{self.deployment_id}"

    @property
    def command_history(self):
        path = (
            pathlib.Path(self.remote_dir)
            .joinpath(f"command-history.{self.deployment_id}")
            .as_posix()
        )
        if not self.__ch_exist:
            self._bastion_connect.run(
                f"mkdir -p {self.remote_dir}" f" && touch {path}"
            )
            self.__ch_exist = True
        return path

    @property
    def upload_folder(self):
        return self.context_dir.joinpath("upload.install")

    @property
    def bastion_private_key_path(self):
        return self.context_dir.joinpath("id_rsa.bastion")

    @property
    def bastion_connection(self):
        if self._bastion_connect:
            return self._bastion_connect
        infra = self.infra_info.data
        if self.bastion_private_key_path.exists():
            self.bastion_private_key_path.unlink()
        private_key = infra.ssh_private_key
        with self.bastion_private_key_path.open("w") as f:
            f.write(private_key)
        os.chmod(self.bastion_private_key_path, 0o400)
        c = Connection(
            infra.bastion_ip,
            user=infra.bastion_user,
            connect_kwargs={
                "key_filename": str(self.bastion_private_key_path),
            },
            connect_timeout=self.time_out,
        )
        self._bastion_connect = c
        return self._bastion_connect

    def args(self, sub_parser: ArgumentParser):
        sub_parser.add_argument(
            "-c",
            "--cdf-package-path",
            dest="cdf_pkg_path",
            help="CDF pkg path, can be a url or local path",
            type=str,
            required=True,
        )
        sub_parser.add_argument(
            "-s",
            "--suite-package-path",
            dest="smax_pkg_path",
            help="Suite pkg path, can be a url or local path",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--cdf-api-db",
            dest="cdf_api_db",
            help="cdf api db name",
            default="cdfapiserverdb",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--cdf-api-db-user",
            dest="cdf_api_db_user",
            help="cdf api db user",
            default="cdfapiserver",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--cdf-api-db-password",
            dest="cdf_api_db_password",
            help="cdf api db password",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--use-external-db",
            dest="cdf_use_external_db",
            help="cdf use external db",
            default=True,
            type=bool,
            required=False,
        )
        sub_parser.add_argument(
            "--idm-db",
            dest="idm_db",
            help="idm db name",
            default="cdfidm",
            type=str,
            required=False,
        )

        sub_parser.add_argument(
            "--idm-db-user",
            dest="idm_db_user",
            help="idm db user",
            default="cdfidmuser",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--idm-db-password",
            dest="idm_db_password",
            help="idm db password",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--cdf-admin-password",
            dest="cdf_admin_password",
            help="cdf admin password",
            default="Admin_1234",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--no-upload",
            dest="no_upload",
            help="Ignore upload files",
            action="store_true",
            default=False,
        )
        sub_parser.add_argument(
            "--suite-size",
            dest="suite_size",
            help="Suite size to install",
            default="demo",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--suite-version",
            dest="suite_version",
            help="Suite version to install",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--timeout",
            dest="timeout",
            help="time out in seconds",
            default=3 * 60 * 60,
            type=int,
            required=False,
        )
        sub_parser.add_argument(
            "--no-set-db",
            dest="no_set_db",
            help="Ignore setup db",
            action="store_true",
            default=False,
        )

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        cdf_pkg_path, suite_pkg_path = self.__download__pkgs__(args)
        self.cdf_pkg_name = cdf_pkg_path.name
        self.suite_metadata_pkg_name = suite_pkg_path.name
        self.time_out = args.timeout
        if not args.suite_version:
            args.suite_version = get_suite_base_ver(suite_pkg_path)
        if not args.cdf_api_db_password:
            args.cdf_api_db_password = (
                self.infra_info.data.default_database_user_password
            )
        if not args.idm_db_password:
            args.idm_db_password = (
                self.infra_info.data.default_database_user_password
            )
        if get_cdf_version(cdf_pkg_path) < "2019.11":
            self.logger.warn(
                "CDF before 2019.11 cannot use external db!!"
                "So this installation will NOT user external db!!"
            )
            args.cdf_use_external_db = False

    def run_in_bastion(self, cmd: str):
        command = f"cd {self.remote_dir} && " + cmd
        infra = self.infra_info.data
        self.logger.debug(
            f"Run: {command} -> {infra.bastion_user}@{infra.bastion_ip}"
        )
        self.bastion_connection.run(
            f"echo '{command}' >> {self.command_history}"
        )
        self.bastion_connection.run(command)

    def __download__pkgs__(self, args: Namespace):
        cdf_pkg_file_path = download_or_copy(
            args.cdf_pkg_path, self.upload_folder, self.logger
        )
        suite_metadata_pkg_file_path = download_or_copy(
            args.smax_pkg_path, self.upload_folder, self.logger
        )
        return (cdf_pkg_file_path, suite_metadata_pkg_file_path)

    def the_act(self, args: Namespace):
        self.upload(args)

    def upload(self, args):
        if args.no_upload:
            return
        logger = self.logger
        c = self.bastion_connection
        infra = self.infra_info.data
        remote_dir = self.remote_dir
        install_path = self.install_script_folder
        copy_tree(install_path, str(self.upload_folder))
        self.bastion_connection.run(f"mkdir -p {remote_dir}")
        for f in pathlib.Path(self.upload_folder).glob("*"):
            logger.info(
                f"Upload: {f} ->{remote_dir}:{infra.bastion_user}@{infra.bastion_ip}"
            )
            c.put(f, remote_dir)
        logger.debug("Files have been uploaded:")
        self.run_in_bastion(f"cd {remote_dir} && ls -l && chmod +x *.sh")

    def setup_db(self, args):
        logger = self.logger
        infra_info = self.infra_info.data
        if not args.no_set_db:
            logger.info("setup postgres db ...")
            cmd = (
                f" ./setup_pg.sh"
                f" --db-host {infra_info.database_ip}"
                f" --default-db-user {infra_info.default_database_user}"
                f" --default-db-password {infra_info.default_database_user_password}"
                f" --cdf-api-db {args.cdf_api_db}"
                f" --cdf-api-db-user {args.cdf_api_db_user}"
                f" --cdf-api-db-password {args.cdf_api_db_password}"
                f" --idm-db {args.idm_db}"
                f" --idm-db-user {args.idm_db_user}"
                f" --idm-db-password {args.idm_db_password}"
            )
            self.run_in_bastion(cmd)
