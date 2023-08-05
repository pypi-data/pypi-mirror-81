#!/bin/bash

MOUNTPOINT=/mnt/nfs/$3
CRED="/etc/smbcredentials/$1.cred"
umount $MOUNTPOINT || :
mkdir -p $MOUNTPOINT
mkdir -p /etc/smbcredentials
rm -fr $CRED
touch $CRED
chmod 600 $CRED
echo "username=$1" >> $CRED
echo "password=$2" >> $CRED
echo "//$1.file.core.windows.net/$3 $MOUNTPOINT cifs nofail,vers=3.0,credentials=$CRED,dir_mode=0777,file_mode=0777,serverino,mfsymlinks" >> /etc/fstab
mount -t cifs //$1.file.core.windows.net/$3 $MOUNTPOINT -o vers=3.0,credentials=$CRED,dir_mode=0777,file_mode=0777,serverino,mfsymlinks
