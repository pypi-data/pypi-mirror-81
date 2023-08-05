import pathlib
import os
from jinja2 import Environment, FileSystemLoader
from argparse import ArgumentParser, Namespace
from types import SimpleNamespace

from sharelib.base_install import BaseInstall
from .create_pv import create_pvs


class Install(BaseInstall):
    def __init__(self):
        super().__init__()
        self._kube_config_file: pathlib.Path = None

    @property
    def name(self):
        return "install"

    @property
    def help(self):
        return "Install Suite on existing infra"

    @property
    def secret_ns_name(self):
        return "u-r-fool"

    @property
    def kube_config(self):
        if self._kube_config_file and self._kube_config_file.exists():
            return str(self._kube_config_file)
        self._kube_config_file = self.context_dir.joinpath("kube-config")
        with self._kube_config_file.open("w") as f:
            f.write(self.infra_info.data.kube_config)
        return str(self._kube_config_file)

    def args(self, sub_parser: ArgumentParser):
        super().args(sub_parser)
        sub_parser.add_argument(
            "--registry-org",
            dest="registry_org",
            help="Azure registry organization name",
            default="hpeswitomsandbox",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--registry-url",
            dest="registry_url",
            help="Azure registry organization name",
            default="itomsma.azurecr.io",
            type=str,
            required=False,
        )
        sub_parser.add_argument(
            "--registry-user",
            dest="registry_user",
            help="Azure registry organization name",
            default="itomsma",
            type=str,
            required=False,
        )

        acr_pwd = (
            os.environ["ACR_PASSWORD"] if "ACR_PASSWORD" in os.environ else None
        )

        sub_parser.add_argument(
            "--registry-pwd",
            dest="registry_pwd",
            help="Azure registry organization name",
            default=acr_pwd,
            type=str,
            required=True if not acr_pwd else False,
        )

    def pre_act(self, args: Namespace):
        super().pre_act(args)
        self.render_config(args)

    def the_act(self, args: Namespace):
        super().the_act(args)
        self.mount_azfile()
        self.build_pv()
        self.create_ns_secret()
        self.setup_db(args)
        self.silent_install(args)

    def build_pv(self):
        create_pv_args = SimpleNamespace()
        create_pv_args.kube_config_file = self.kube_config
        create_pv_args.logger = self.logger
        create_pv_args.ssa = self.infra_info.data.ssa_name
        create_pv_args.ssb = self.infra_info.data.ssb_name
        create_pv_args.cdf_ns = "core"
        create_pv_args.smax_ns = self.suite_ns_name
        create_pv_args.cdf_azfile_secret = "azure-secret"
        create_pv_args.smax_azfile_secret = "azure-secret"
        create_pv_args.secret_ns = self.secret_ns_name
        create_pvs(create_pv_args)

    def mount_azfile(self):
        infra = self.infra_info.data
        cmd = (
            f" sudo ./mount_az_file.sh {infra.azfile_account_name} {infra.azfile_primary_key} {infra.ssa_name}"
            f" && sudo ./mount_az_file.sh {infra.azfile_account_name} {infra.azfile_primary_key} {infra.ssb_name}"
            f" && ./create_folder_generic.sh  {infra.ssa_name}"
            f" && ./create_folder_analytics.sh  {infra.ssb_name}"
        )
        self.run_in_bastion(cmd)

    def create_ns_secret(self):
        infra = self.infra_info.data
        cmd = (
            f"cd {self.remote_dir}"
            f" && ./prepare_ns.sh {infra.azfile_account_name} {infra.azfile_primary_key} {self.secret_ns_name} || :"
        )
        self.run_in_bastion(cmd)

    def silent_install(self, args: Namespace):
        remote_dir = self.remote_dir
        infra = self.infra_info.data
        cmd = (
            f"cd {remote_dir}"
            f" && sudo ./silent_install.sh"
            f" -c {self.cdf_pkg_name}"
            f" -s {self.suite_metadata_pkg_name}"
            f" --db-host {infra.database_ip}"
            f" --cdf-api-db {args.cdf_api_db}"
            f" --cdf-api-db-user {args.cdf_api_db_user}"
            f" --cdf-api-db-password {args.cdf_api_db_password}"
            f" --use-external-db {args.cdf_use_external_db}"
            f" --cdf-admin-password {args.cdf_admin_password}"
            f" --fqdn {infra.fqdn_name}"
            f" --registry-org {args.registry_org}"
            f" --registry-url {args.registry_url}"
            f" --registry-user {args.registry_user}"
            f" --registry-pwd {args.registry_pwd}"
            f" --suite-ns {self.suite_ns_name}"
        )
        self.run_in_bastion(cmd)

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
