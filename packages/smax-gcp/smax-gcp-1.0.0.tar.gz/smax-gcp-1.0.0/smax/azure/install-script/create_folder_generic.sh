#!/bin/bash
MOUNTPOINT=/mnt/nfs/$1
cd $MOUNTPOINT
sudo mkdir  -p var/vols/itom/itsma/core
sudo mkdir  -p var/vols/itom/itsma/db-backup-vol
sudo mkdir  -p var/vols/itom/itsma/db-single-vol
sudo mkdir  -p var/vols/itom/itsma/global-volume
sudo mkdir  -p var/vols/itom/itsma/db-volume
sudo mkdir  -p var/vols/itom/itsma/db-volume-1
sudo mkdir  -p var/vols/itom/itsma/db-volume-2
sudo mkdir  -p var/vols/itom/itsma/rabbitmq-infra-rabbitmq-0
sudo mkdir  -p var/vols/itom/itsma/rabbitmq-infra-rabbitmq-1
sudo mkdir  -p var/vols/itom/itsma/rabbitmq-infra-rabbitmq-2
sudo mkdir  -p var/vols/itom/itsma/itom-logging-vol
sudo mkdir  -p var/vols/itom/itsma/db-node1-vol
sudo mkdir  -p var/vols/itom/itsma/db-node2-vol
