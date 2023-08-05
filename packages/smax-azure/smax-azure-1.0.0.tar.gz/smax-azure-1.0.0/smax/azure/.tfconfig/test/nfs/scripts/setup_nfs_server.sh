#!/bin/bash

sudo yum install -y rpcbind
sudo yum install -y nfs-utils
sudo systemctl enable rpcbind
sudo systemctl start rpcbind

function create_directory() {
    local volume=$1
    if [ -d "$volume" ]; then
        echo "Removing legacy cdf volume"
        sudo rm -rf "$volume"
    fi
    sudo mkdir -p $volume
    sudo chown -R 1999:1999 $volume
    sudo chmod 755 $volume
}
function make_volume() {
    local nfs_volume=$1
    if [ ! -f /etc/exports ]; then
        sudo touch /etc/exports
    fi
    #creates the directory
    create_directory $nfs_volume
    if grep -q "$nfs_volume\\b" /etc/exports; then
        echo "Volume already added to exports: $nfs_volume"
    else
        echo "$nfs_volume *(rw,async,anonuid=1999,anongid=1999,all_squash)" | sudo tee -a /etc/exports
        #sudo sed -i -e "a\$nfs_volume *(rw,sync,anonuid=1999,anongid=1999,all_squash)" /etc/exports
    fi
}
function finalize() {
    # make sure all directories are owned by itsma/itsma
    sudo chown -R 1999:1999 /var/vols/itom
    sudo exportfs -ra
    sudo systemctl restart rpcbind
    sudo systemctl restart nfs-server
    sudo systemctl enable nfs-server
}
#make volumes
echo "Creating volumes..."
make_volume /var/vols/itom/itsma/core
make_volume /var/vols/itom/itsma/db-backup-vol
make_volume /var/vols/itom/itsma/db-single-vol
make_volume /var/vols/itom/itsma/global-volume
make_volume /var/vols/itom/itsma/smartanalytics-volume
make_volume /var/vols/itom/itsma/db-volume
make_volume /var/vols/itom/itsma/db-volume-1
make_volume /var/vols/itom/itsma/db-volume-2
make_volume /var/vols/itom/itsma/rabbitmq-infra-rabbitmq-0
make_volume /var/vols/itom/itsma/rabbitmq-infra-rabbitmq-1
make_volume /var/vols/itom/itsma/rabbitmq-infra-rabbitmq-2
make_volume /var/vols/itom/itsma/itom-logging-vol
make_volume /var/vols/itom/itsma/volume10
make_volume /var/vols/itom/itsma/itsma-smarta-sawarc-con-0
make_volume /var/vols/itom/itsma/itsma-smarta-sawarc-con-1
make_volume /var/vols/itom/itsma/itsma-smarta-sawarc-con-a-0
make_volume /var/vols/itom/itsma/itsma-smarta-sawarc-con-a-1
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-0
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-1
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-2
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-3
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-4
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-5
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-0
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-1
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-2
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-3
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-4
make_volume /var/vols/itom/itsma/itsma-smarta-saw-con-a-5
make_volume /var/vols/itom/itsma/itsma-smarta-sawmeta-con-0
make_volume /var/vols/itom/itsma/itsma-smarta-sawmeta-con-1
make_volume /var/vols/itom/itsma/itsma-smarta-sawmeta-con-a-0
make_volume /var/vols/itom/itsma/itsma-smarta-sawmeta-con-a-1

if [[ "$1" < "2019.02"   ]]; then
  make_volume /var/vols/itom/itsma/itsma-smarta-saw-dah-0
  make_volume /var/vols/itom/itsma/itsma-smarta-saw-dah-1
  make_volume /var/vols/itom/itsma/itsma-smarta-saw-dah-2
  make_volume /var/vols/itom/itsma/itsma-smarta-sawmeta-dah-0
  make_volume /var/vols/itom/itsma/itsma-smarta-stx-dah-0
  make_volume /var/vols/itom/itsma/itsma-smarta-sawarc-dah-0
fi


if [ ! $(id -g itsma >/dev/null) ]; then
    echo "Adding group itsma"
    sudo groupadd -g 1999 itsma
fi
if [ ! $(id -u itsma >/dev/null) ]; then
    echo "Adding user itsma"
    sudo useradd -g 1999 -u 1999 itsma
fi
echo "Restarting services..."
finalize
echo "NFS Server setup done!"
