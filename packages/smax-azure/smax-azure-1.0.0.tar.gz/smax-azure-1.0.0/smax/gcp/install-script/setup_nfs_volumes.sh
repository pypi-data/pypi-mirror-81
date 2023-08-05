#!/bin/bash

SUITE_USER_UID=1999
SUITE_USER_GID=1999
MOUNT_POINT="/mnt/nfs"
NFS_SERVER=$1
ROOT_FOLDER=$2
NFS_VERSION=3
NFS_PARENT="var/vols/itom"

if [ ! -d $MOUNT_POINT ]; then
    mkdir -p $MOUNT_POINT
fi

declare -a arr=(
"itsma/core"
"itsma/db-backup-vol"
"itsma/db-single-vol"
"itsma/global-volume"
"itsma/db-volume"
"itsma/db-volume-1"
"itsma/db-volume-2"
"itsma/rabbitmq-infra-rabbitmq-0"
"itsma/rabbitmq-infra-rabbitmq-1"
"itsma/rabbitmq-infra-rabbitmq-2"
"itsma/itom-logging-vol"
#"itsma/db-node1-vol"
#"itsma/db-node2-vol"
"itsma/smartanalytics-volume"
"itsma/itsma-smarta-sawarc-con-0"
"itsma/itsma-smarta-sawarc-con-1"
"itsma/itsma-smarta-sawarc-con-a-0"
"itsma/itsma-smarta-sawarc-con-a-1"
"itsma/itsma-smarta-saw-con-0"
"itsma/itsma-smarta-saw-con-1"
"itsma/itsma-smarta-saw-con-2"
"itsma/itsma-smarta-saw-con-3"
"itsma/itsma-smarta-saw-con-4"
"itsma/itsma-smarta-saw-con-5"
"itsma/itsma-smarta-saw-con-a-0"
"itsma/itsma-smarta-saw-con-a-1"
"itsma/itsma-smarta-saw-con-a-2"
"itsma/itsma-smarta-saw-con-a-3"
"itsma/itsma-smarta-saw-con-a-4"
"itsma/itsma-smarta-saw-con-a-5"
"itsma/itsma-smarta-sawmeta-con-0"
"itsma/itsma-smarta-sawmeta-con-1"
"itsma/itsma-smarta-sawmeta-con-a-0"
"itsma/itsma-smarta-sawmeta-con-a-1"
)

mountNFS() {
    umount $MOUNT_POINT || :
    mount -t nfs -o nfsvers=$NFS_VERSION $NFS_SERVER:/$ROOT_FOLDER $MOUNT_POINT
    if [ $? -eq 0 ] || [ $? -eq 32 ]; then
        echo "Successfully mount NFS"
        sed -i '$a\'"$NFS_SERVER:/$ROOT_FOLDER $MOUNT_POINT nfs nfsvers=$NFS_VERSION 0 0" /etc/fstab
    else
        echo "Could not mount NFS"
        exit 1
    fi
}

make_volume() {
    local VOLUME=$1
    pushd $(pwd)
    cd $MOUNT_POINT
    local MOUNTED_PV=$MOUNT_POINT/$NFS_PARENT/$VOLUME
    mkdir -p $MOUNTED_PV
    chown -R $SUITE_USER_UID:$SUITE_USER_GID $MOUNTED_PV
    chmod g+w $MOUNTED_PV
    chmod g+s $MOUNTED_PV
    popd
}

mountNFS

MOUNTED_PRE=$MOUNT_POINT/$NFS_PARENT
sudo rm -fr $MOUNTED_PRE/*

for i in "${arr[@]}"; do
    make_volume $i
done
