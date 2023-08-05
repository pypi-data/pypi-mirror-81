#!/bin/bash

curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod 755 kubectl
sudo mv kubectl /bin

sudo yum install -y docker
sudo groupadd docker
sudo usermod -a -G docker ${USER}
sudo usermod -a -G docker $1
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl enable docker
sudo yum install -y nfs-utils
sudo yum install -y unzip
sudo yum install -y python3

#sudo yum install https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm -y
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
###add a workround for bug https://www.postgresql.org/message-id/16295-7ca0beea2d6f6ad8%40postgresql.org
sudo sed -i -e 's@\[pgdg96-updates-debuginfo\]k@\[pgdg96-updates-debuginfo\]@g' /etc/yum.repos.d/pgdg-redhat-all.repo
sudo sed -i -e 's@\[pgdg95-updates-debuginfo\]k@\[pgdg95-updates-debuginfo\]@g' /etc/yum.repos.d/pgdg-redhat-all.repo

sudo yum install -y postgresql10

mkdir -p ${HOME}/.kube
cp kube-config ${HOME}/.kube/config

export KUBECONFIG=${HOME}/.kube/config
echo 'export KUBECONFIG=$HOME/.kube/config' >> ${HOME}/.bashrc

sudo cp -R .kube /root/
sudo chown -R root:root /root/.kube
