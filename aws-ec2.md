# Increasing the size of an EBS volume


# Extending EC2 Ubuntu File System
After increasing the volume of an ESB, the file system [must be increased](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html) to use the increased volume. The system can be resized as soon as the volume is in the `optimizing` state.

## Extending a partition
Your EBS volume might have a partition that contains the file system and data. Increasing the size of a volume does not increase the size of the partition. Before you extend the file system on a resized volume, check whether the volume has a partition that must be extended to the new size of the volume.

You can view information about the block devices by using the `lsblk` command. If a resized volume has a partition and the partition does not reflect the new size of the volume, use the `growpart` command to extend the partition.

A T2 instance may look like this:
```
[ec2-user ~]$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0  16G  0 disk
└─xvda1 202:1    0   8G  0 part /
xvdf    202:80   0  30G  0 disk
└─xvdf1 202:81   0   8G  0 part /data
```

The root volume, /dev/xvda, has a partition, /dev/xvda1. While the size of the volume is 16 GB, the size of the partition is still 8 GB and must be extended.

The volume /dev/xvdf has a partition, /dev/xvdf1. While the size of the volume is 30G, the size of the partition is still 8 GB and must be extended.

To extend the partition on each volume, use the following growpart commands. Note that there is a space between the device name and the partition number.

```
sudo growpart /dev/xvda 1
sudo growpart /dev/xvdf 1
```

You can verify that the partitions reflect the increased volume size by using the lsblk command again

```
[ec2-user ~]$ lsblk
NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
xvda    202:0    0  16G  0 disk
└─xvda1 202:1    0  16G  0 part /
xvdf    202:80   0  30G  0 disk
└─xvdf1 202:81   0  30G  0 part /data
```

## Extending the filesystem
Use a file system-specific command to resize each file system to the new volume capacity. For a file system other than the examples shown here, refer to the documentation for the file system for instructions.

Use the `df -h` command to verify the size of the file system for each volume. In this example, both `/dev/xvda1` and `/dev/xvdf` reflect the original size of the volumes, 8 GB.

```
[ec2-user ~]$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/xvda1       8.0G  1.9G  6.2G  24% /
/dev/xvdf1       8.0G   45M  8.0G   1% /data
...
```

Use the `resize2fs` command to extend the file system on each volume.

```
[ec2-user ~]$ sudo resize2fs /dev/xvda1
[ec2-user ~]$ sudo resize2fs /dev/xvdf1
```

You can verify that each file system reflects the increased volume size by using the `df -h` command again.

```
[ec2-user ~]$ df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/xvda1        16G  1.9G  6.2G  12% /
/dev/xvdf1        30G   45M  8.0G   1% /data
...
```
