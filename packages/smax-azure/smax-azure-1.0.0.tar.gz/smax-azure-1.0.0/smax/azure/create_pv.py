pv_yaml = """
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {0}
spec:
  accessModes:
  - {9}
  capacity:
    storage: {1}
  claimRef:
    apiVersion: v1
    kind: PersistentVolumeClaim
    namespace: {2}
    name: {3}
  azureFile:
    shareName: {4}
    secretName: {5}
    secretNamespace: {6}
  mountOptions:
  - dir_mode=0775
  - uid=1999
  - gid=1999
  - mfsymlinks
  {8}
  persistentVolumeReclaimPolicy: Retain
  storageClassName: {7}
  volumeMode: Filesystem
"""

cdf_core_volumes = [
    ("itom-vol", "5Gi"),
    ("itom-logging-vol", "1Mi"),
    ("db-node1-vol", "10Gi"),
    ("db-node2-vol", "10Gi"),
    ("db-single-vol", "5Gi"),
]

cdf_volumes = [
    ("global-volume", "1Mi"),
    ("db-backup-vol", "1Mi"),
    ("db-volume", "1Mi"),
    ("db-volume-1", "1Mi"),
    ("db-volume-2", "1Mi"),
    ("rabbitmq-infra-rabbitmq-0", "1Mi"),
    ("rabbitmq-infra-rabbitmq-1", "1Mi"),
    ("rabbitmq-infra-rabbitmq-2", "1Mi"),
    ("smartanalytics-volume", "1Mi"),
]

suite_volumes = [
    ("itsma-smarta-sawarc-con-0", "1Mi"),
    ("itsma-smarta-sawarc-con-1", "1Mi"),
    ("itsma-smarta-sawarc-con-a-0", "1Mi"),
    ("itsma-smarta-sawarc-con-a-1", "1Mi"),
    ("itsma-smarta-saw-con-0", "1Mi"),
    ("itsma-smarta-saw-con-1", "1Mi"),
    ("itsma-smarta-saw-con-2", "1Mi"),
    ("itsma-smarta-saw-con-3", "1Mi"),
    ("itsma-smarta-saw-con-4", "1Mi"),
    ("itsma-smarta-saw-con-5", "1Mi"),
    ("itsma-smarta-saw-con-a-0", "1Mi"),
    ("itsma-smarta-saw-con-a-1", "1Mi"),
    ("itsma-smarta-saw-con-a-2", "1Mi"),
    ("itsma-smarta-saw-con-a-3", "1Mi"),
    ("itsma-smarta-saw-con-a-4", "1Mi"),
    ("itsma-smarta-saw-con-a-5", "1Mi"),
    ("itsma-smarta-sawmeta-con-0", "1Mi"),
    ("itsma-smarta-sawmeta-con-1", "1Mi"),
    ("itsma-smarta-sawmeta-con-a-0", "1Mi"),
    ("itsma-smarta-sawmeta-con-a-1", "1Mi"),
]


class PVDefine:
    def __init__(
        self,
        name,
        storage,
        pvc_ns,
        pvc_name,
        share_name,
        share_mount,
        secret_name,
        storage_class,
        mount_opt="",
        access_mode="ReadWriteMany",
    ):
        self.name = name
        self.storage = storage
        self.pvc_ns = pvc_ns
        self.pvc_name = pvc_name
        self.share_name = share_name
        self.share_mount = share_mount
        self.storage_class = storage_class
        self.secret_name = secret_name
        self.mount_opt = mount_opt
        self.access_mode = access_mode


from types import SimpleNamespace

import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException

from sharelib.utility import get_env_proxy


def create_pvs(args: SimpleNamespace):
    all_volumes = []
    for v in cdf_core_volumes:
        pv = PVDefine(
            name=v[0],
            storage=v[1],
            pvc_ns=args.cdf_ns,
            pvc_name=v[0],
            share_name="/var/vols/itom/itsma/" + v[0],
            share_mount=args.ssa,
            secret_name=args.cdf_azfile_secret,
            storage_class="cdf-default",
        )
        if v[0].lower() == "itom-vol":
            pv = PVDefine(
                name=v[0],
                storage=v[1],
                pvc_ns=args.cdf_ns,
                pvc_name=v[0] + "-claim",
                share_name="/var/vols/itom/itsma/core",
                share_mount=args.ssa,
                secret_name=args.cdf_azfile_secret,
                storage_class="cdf-default",
            )
        all_volumes.append(pv)
    for v in cdf_volumes:
        pv = PVDefine(
            name=args.smax_ns + "-" + v[0],
            storage=v[1],
            pvc_ns=args.smax_ns,
            pvc_name=v[0],
            share_name="/var/vols/itom/itsma/" + v[0],
            share_mount=args.ssa,
            secret_name=args.smax_azfile_secret,
            storage_class="cdf-default",
        )
        if pv.name.find("smartanalytics") != -1:
            pv.share_mount = args.ssb
        all_volumes.append(pv)

    for v in suite_volumes:
        pv = PVDefine(
            name=args.smax_ns + "-" + v[0],
            storage=v[1],
            pvc_ns=args.smax_ns,
            pvc_name=v[0],
            share_name="/var/vols/itom/itsma/" + v[0],
            share_mount=args.ssb,
            secret_name=args.smax_azfile_secret,
            storage_class="itom-fast",
        )
        if pv.name.find("-smarta-") != -1:
            pv.access_mode = "ReadWriteOnce"
        all_volumes.append(pv)

    config.load_kube_config(config_file=args.kube_config_file)
    client.Configuration._default.proxy = get_env_proxy()
    v1 = client.CoreV1Api()
    for pv in all_volumes:
        t = "- nobrl" if pv.name.find("smartanalytics") != -1 else ""
        real_yaml = pv_yaml.format(
            pv.name,
            pv.storage,
            pv.pvc_ns,
            pv.pvc_name,
            pv.share_mount + pv.share_name,
            pv.secret_name,
            args.secret_ns,
            pv.storage_class,
            t,
            pv.access_mode,
        )
        try:
            v1.delete_persistent_volume(pv.name)
        except ApiException as e:
            pass

        resp = v1.create_persistent_volume(
            body=yaml.safe_load(real_yaml),
        )

        if args.logger:
            args.logger.info(f"PV created: {resp.metadata.name}")
