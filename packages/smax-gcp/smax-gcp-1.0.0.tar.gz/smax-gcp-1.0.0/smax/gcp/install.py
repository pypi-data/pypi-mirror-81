import shutil
from argparse import ArgumentParser, Namespace

from jinja2 import Environment, FileSystemLoader

from sharelib.base_install import BaseInstall


class Install(BaseInstall):
    @property
    def name(self):
        return "install"

    @property
    def help(self):
        return "Install Suite on Gcp infra"

    def args(self, sub_parser: ArgumentParser):
        super().args(sub_parser)
        sub_parser.add_argument(
            "--registry-org",
            dest="registry_org",
            help="GCP registry organization name",
            default="itom-smax-nonprod",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--registry-key",
            dest="registry_key_file",
            help="registry key file used to" "access GCP container registry",
            default="./keys/svc-key.json",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--no-set-nfs",
            dest="no_set_nfs",
            help="Ignore setup nfs volumes",
            action="store_true",
            default=False,
        )

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        shutil.copy(
            args.registry_key_file, self.upload_folder.joinpath("registry-key")
        )
        self.render_config(args)

    def render_config(self, args: Namespace):
        install_path = self.install_script_folder
        env = Environment(loader=FileSystemLoader(install_path))
        template_name = "config.json.jinja2"
        output_file_path = self.upload_folder.joinpath(
            template_name.rsplit(".", 1)[0]
        )
        template = env.get_template(template_name)
        self.logger.debug(f"rendering suite config : {template_name}")
        infra_info = self.infra_info.data
        output_from_parsed_template = template.render(
            external_host_name=infra_info.fqdn_name,
            nfs_server_host_name=infra_info.nfs_ip,
            nfs_share_name=infra_info.nfs_share_name,
            db_host_name=infra_info.database_ip,
            db_host_port=5432,
            idm_db=args.idm_db,
            idm_db_user=args.idm_db_user,
            idm_db_user_password=args.idm_db_password,
            db_login_user="postgres",
            db_login_password=infra_info.default_database_user_password,
            suite_size=args.suite_size,
            suite_version=args.suite_version,
            default_admin_password=args.cdf_admin_password,
        )
        with output_file_path.open("w") as f:
            f.write(output_from_parsed_template)

    def setup_nfs(self, args):
        logger = self.logger
        infra_info = self.infra_info.data
        if not args.no_set_nfs:
            logger.info("setup nfs volumes ...")
            cmd = (
                f" sudo ./setup_nfs_volumes.sh"
                f" {infra_info.nfs_ip}"
                f" {infra_info.nfs_share_name}"
            )
            self.run_in_bastion(cmd)

    def silent_install(self, args):
        logger = self.logger
        infra_info = self.infra_info.data
        logger.info("make install script rooted ...")
        cmd = (
            f" sudo chown root:root ./silent_install.sh"
            f" && sudo chmod 4755 ./silent_install.sh"
        )
        self.run_in_bastion(cmd)
        logger.info("install cdf & suite ...")
        cmd = (
            f" sudo ./silent_install.sh"
            f" -c {self.cdf_pkg_name}"
            f" -s {self.suite_metadata_pkg_name}"
            f" --db-host {infra_info.database_ip}"
            f" --cdf-api-db {args.cdf_api_db}"
            f" --cdf-api-db-user {args.cdf_api_db_user}"
            f" --cdf-api-db-password {args.cdf_api_db_password}"
            f" --use-external-db {args.cdf_use_external_db}"
            f" --nfs-host {infra_info.nfs_ip}"
            f" --nfs-shared-name {infra_info.nfs_share_name}"
            f" --cdf-admin-password {args.cdf_admin_password}"
            f" --fqdn {infra_info.fqdn_name}"
            f" --fqdn-ip {infra_info.fqdn_ip}"
            f" --registry-org {args.registry_org}"
            f" --suite-ns {self.suite_ns_name}"
        )
        self.run_in_bastion(cmd)

    def the_act(self, args):
        super().the_act(args)
        self.setup_db(args)
        self.setup_nfs(args)
        self.silent_install(args)
        infra_info = self.infra_info.data
        self.logger.info(
            "Finished. Run:\n"
            f"ssh -i {str(self.bastion_private_key_path)}"
            f" {infra_info.bastion_user}@{infra_info.bastion_ip}\n"
            "to login your bastion to check"
        )
