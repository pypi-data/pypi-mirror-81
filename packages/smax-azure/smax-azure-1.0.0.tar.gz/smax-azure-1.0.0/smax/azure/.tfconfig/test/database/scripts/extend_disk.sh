#!/bin/bash
echo "d
2
n
p
2
 
 
w
" | fdisk /dev/sda
partx -u /dev/sda2
xfs_growfs -d /dev/sda2 