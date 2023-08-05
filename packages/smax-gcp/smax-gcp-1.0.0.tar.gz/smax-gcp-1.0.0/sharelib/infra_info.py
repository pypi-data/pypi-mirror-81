import json
import pathlib
from types import SimpleNamespace

from fabric import Connection
from tabulate import tabulate


class InfraInfo:
    def __init__(self, output: str):
        self.data = SimpleNamespace()
        d = json.loads(output)
        for k in d:
            setattr(self.data, k, d[k]["value"])

    @property
    def dict(self):
        return self.data.__dict__

    def has(self, key):
        return key in self.dict

    def as_table(self):
        t = {
            k: v
            for k, v in self.dict.items()
            if "ssh" not in k and "kube_config" not in k
        }
        return tabulate(t.items())


def connect_bastion(infra: InfraInfo, timeout=3 * 60 * 60):
    private_key_target = pathlib.Path(".id_rsa").relative_to(".")
    private_key = infra.data.ssh_private_key
    with private_key_target.open("w") as f:
        f.write(private_key)
    c = Connection(
        infra.data.bastion_ip,
        user=infra.data.bastion_user,
        connect_kwargs={
            "key_filename": str(private_key_target),
        },
        connect_timeout=timeout,
    )
    private_key_target.unlink()
    return c
