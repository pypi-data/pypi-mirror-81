#!/bin/bash

cd ~
sudo chmod og+rX /home /home/$USER

sudo systemctl stop firewalld
sudo systemctl disable firewalld
#sudo yum install -y https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
###add a workround for bug https://www.postgresql.org/message-id/16295-7ca0beea2d6f6ad8%40postgresql.org
sudo sed -i -e 's@\[pgdg96-updates-debuginfo\]k@\[pgdg96-updates-debuginfo\]@g' /etc/yum.repos.d/pgdg-redhat-all.repo
sudo sed -i -e 's@\[pgdg95-updates-debuginfo\]k@\[pgdg95-updates-debuginfo\]@g' /etc/yum.repos.d/pgdg-redhat-all.repo
sudo yum install -y postgresql10-server
sudo yum install -y postgresql10-contrib
sudo /usr/pgsql-10/bin/postgresql-10-setup initdb
sudo systemctl enable postgresql-10

sudo systemctl start postgresql-10
sudo chown postgres:postgres *.conf
sudo chmod 700 *.conf
sudo cp -rf *.conf /var/lib/pgsql/10/data/
sudo -u postgres psql template1 -c "ALTER USER postgres WITH PASSWORD '${db_password}'";
sudo systemctl restart postgresql-10

sudo -u postgres psql << EOF
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
CREATE SCHEMA postgres AUTHORIZATION postgres;
EOF
