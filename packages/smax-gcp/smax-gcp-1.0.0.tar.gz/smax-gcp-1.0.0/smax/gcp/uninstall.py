import os
import pathlib
from argparse import Namespace, ArgumentParser

from fabric import Connection

from sharelib.base_act import BaseAct
from sharelib.utility import set_log


class Uninstall(BaseAct):
    @property
    def name(self):
        return "uninstall"

    @property
    def help(self):
        return "Uninstall Suite on existing infra"

    def args(self, sub_parser: ArgumentParser):
        sub_parser.add_argument(
            "--timeout",
            dest="timeout",
            help="time out in seconds",
            default=3 * 60 * 60,
            type=int,
            required=False,
        )

    def the_act(self, args: Namespace):
        logger = set_log(use_color=args.color_log, verbose=args.debug_log)
        infra = self.__get_infra_info__(args)
        infra_info = infra.data
        logger.debug("found infra => ")
        logger.debug(os.linesep + infra.as_table())
        if not infra.has("ssh_private_key"):
            logger.error("Cannot get ssh private key to connect remote bastion")
            return
        private_key_target = pathlib.Path(".id_rsa").relative_to(".")
        private_key = infra_info.ssh_private_key
        with private_key_target.open("w") as f:
            f.write(private_key)

        c = Connection(
            infra_info.bastion_ip,
            user=infra_info.bastion_user,
            connect_kwargs={
                "key_filename": str(private_key_target),
            },
            connect_timeout=args.timeout,
        )
        suite_ns = f"itsma-{args.deployment_id}"
        logger.info(f"remove suite namespace: {suite_ns} ...")
        cmd = f"kubectl delete namespaces {suite_ns} --wait=true --timeout=15m || :"
        logger.debug(
            f"run command {infra_info.bastion_user}@{infra_info.bastion_ip} => "
        )
        logger.debug(cmd)
        c.run(cmd)

        logger.info("remove cdf namespace: core ...")
        cmd = "kubectl delete namespaces core --wait=true --timeout=15m || :"
        logger.debug(
            f"run command {infra_info.bastion_user}@{infra_info.bastion_ip} => "
        )
        logger.debug(cmd)
        c.run(cmd)
        private_key_target.unlink()
