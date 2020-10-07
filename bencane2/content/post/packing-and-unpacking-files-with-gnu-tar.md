---
authors:
- Benjamin Cane
categories:
- Command Line
- Linux
- Linux Commands
- SysAdmin Basics
- Unix
- Unix Commands
date: '2013-05-23T15:07:37'
description: Simple guide on using a basic Unix and Linux tool GNU tar
draft: false
header:
  caption: ''
  image: ''
tags:
- all
- extracting a tar file
- linux
- linux os
- red hat os
- tar command
- tarcopy
- tarpipe
title: Packing and Unpacking files with GNU Tar
url: /2013/05/23/packing-and-unpacking-files-with-gnu-tar

---

One of the most basic tasks for any Sysadmin is packing and unpacking files for various reasons. While there are many ways to perform this task GNU Tar is probably one of the most recognized and commonly used tools by Linux/Unix users.

## A little history on tar

The tar command is a command that appeared in the early days of Unix and has had several changes made over time. Originally the command was used to take files, combine them into one file and write them to a **t**ape **ar**chive (tar). Nowadays tar is used mostly as a general purpose tool to package and compress many files into one single file for distribution or backup.

There are several common implementations of tar that are in use today, because there are multiple implementations there are also some differences in the options and formats available. In today's article I will not be showing all of the various options of tar (that's what man pages are for), but rather will be showing commonly used flags and some not so common tricks.

## Tar Basics

#### Creating a tar file

To create a basic tar you really only need to specify a few things.
	
  * `-c` Stands for create, you will see this a lot in our examples today
  * `-f` or `--file` immediately followed by a file or device will tell tar where to create the tar file
  * And finally the files or directories to package

**Example:**

    $ tar -cf tarfile.tar file1.txt

#### Extracting a tar file

Extracting a tar file is just as simple as creating one.
	
  * `-x` Stands for extract
  * `-f` or `--file` immediately followed by a file or device has the same usage as create

**Example:**

    $ tar -xf tarfile.tar

#### Adding verbosity

By default tar does not output what it is doing, you can add this by adding verbosity to the command with the `-v` flag. In addition to adding verbosity we are also going to tar more than one file in our example. Packaging more than one file is the point of tar after all isn't it?

    $ tar -cvf tarfile.tar files_dir/ file1.txt
    files_dir/
    files_dir/file3.txt
    files_dir/file4.txt
    file1.txt

As you can see packaging an entire directory is as simple as adding it to the list of files to package into a tar file.

#### Listing files in an existing tar

Sometimes you simply want to look at the files within a tar file without extracting, to do so we can use the `-t` or `--list` flag. As a side note it is generally a good practice when you receive a tar file from an outside source to list the contents of the tarball to ensure you are not overwriting files you do not intend to.

    $ tar -tf tarfile.tar
    files_dir/
    files_dir/file3.txt
    files_dir/file4.txt
    file1.txt

We can also add the verbose option and show the files attributes such as permissions, size and timestamps.

    $ tar -tvf tarfile.tar
    drwxrwxr-x madflojo/madflojo 0 2013-05-22 21:00 files_dir/
    -rw-rw-r-- madflojo/madflojo 0 2013-05-22 21:00 files_dir/file3.txt
    -rw-rw-r-- madflojo/madflojo 0 2013-05-22 21:00 files_dir/file4.txt
    -rw-rw-r-- madflojo/madflojo 0 2013-05-22 20:42 file1.txt

An important note on tar is that it has the ability of retaining file attributes such as permissions, size and timestamps. When extracted as a user with proper privileges these attributes will be applied to the newly created files or overwritten files.

#### Appending files to an existing tar

Once a tar file is created it is possible to add files with the `-r` or `--append` option. The append option however is not allowed when the file had been compressed.

    $ tar -rvf tarfile.tar file2.txt
     file2.txt

#### Adding gzip compression

Early versions of tar used Unix compress for file compression, after some time gzip compression was also added.

##### The old way

Some systems had implemented the gzip command but not a tar command that added gzip inherently. Originally if users wanted to create a tarball that was gzip compressed they would need to tar the file and then gzip it.

    $ tar -cvf tarfile.tar file1.txt file2.txt
    file1.txt
    file2.txt
    $ gzip tarfile.tar
    $ ls -la tarfile.tar.gz
    -rw-rw-r-- 1 madflojo madflojo 136 May 22 21:22 tarfile.tar.gz

##### The new way

Modern implementations of tar add gzip compression inherently; you can add this compression at the creation of the tar file with the `-z` or `--gzip` option.

    $ tar -cvzf tarfile.tar.gz file1.txt file2.txt
    file1.txt
    file2.txt

#### Adding bzip2 compression

bzip2 is a compression tool much like gzip however it uses a different algorithm to compress files and is generally better at compression however it takes longer to compress items. To add bzip2 compression we simply add a `-j` to the command.

    $ tar -cjvf tarfile.tar.bz files_dir
    files_dir/
    files_dir/file3.txt
    files_dir/file4.txt

#### Extracting tarballs with compression

Any-time you are dealing with tarfiles that have been compressed you will need to add the appropriate compression flag to other tar commands such as extract or list. The following is an example of extracting a bzip2 file.

    $ tar -xjvf tarfile.tar.bz files_dir
    files_dir/
    files_dir/file3.txt
    files_dir/file4.txt

#### Listing tarballs with compression

The following is an example of listing a tar files contents that has gzip compression.

    $ tar -cjvf tarfile.tar.bz files_dir
    files_dir/
    files_dir/file3.txt
    files_dir/file4.txt

#### Extract without replacing old files

The tar commands on today's systems have the ability to extract files without overwriting and existing file. To enable this you will need to specify `-k` on the extract command.

    $ tar -czf tarfile.tar.gz file1.txt file2.txt
    $ rm file2.txt && echo "I removed file2" >> file1.txt
    $ tar -xvzkf tarfile.tar.gz
    file1.txt
    file2.txt
    $ cat file1.txt
    I removed file2

## Beyond the basic tar commands

#### Creating a tar with --files-from to avoid argument list too long

Sometimes specifying the files for tar to package is difficult. Either due to the number of files, the names of files or simply because it is too much to type. Tar has the ability to read a file and create a tarball of the files listed within the input file.

Below is an example of one way to get around the [argument list too long](http://bencane.com/2011/07/argument-list-too-long/) problem.

**The problem:**

    $ tar -czf ../tarfile.tgz *
    bash: /bin/tar: Argument list too long

**Solution:**

    $ ls > ../filestocopy.txt
    $ tar -T ../filestocopy.txt -czf ../tarfile.tgz

In addition to the argument list too long scenario the `-T` flag can be useful for automated jobs that may need to run tar against many files.

#### Tarpipe (or TarCopy)

Tarpipe or sometimes refereed to as tarcopy is the process where one would use tar to copy files from one place to another.

The idea behind tarpipe is that tar has the ability to send the packaged files to stdout rather than to a file. When you use this you can pipe that stdout to another tar command in a different directory.

    $ tar -cf - file* | (cd ../files_copied/ && tar -xf -)

The `-` after `-f` where a file name would normally go is what tells tar to send the output to standard out.

##### Why use tar and not cp?

Originally the cp command did not support preserving timestamps and file permissions and that was one of the major reasons to use tarpipe rather than cp. However times have changed and modern-day cp commands do have the `-p` (preserve) option, but there is still one reason to use tarpipe over cp. It's Faster!

**Tar**

    $ time tar -cf - file* | (cd ../files_copied/ && tar -xf -)
    real 0m0.010s
    user 0m0.004s
    sys 0m0.004s

**cp**

    $ time cp -p file* ../files_copied/
    real 0m0.024s
    user 0m0.000s
    sys 0m0.000s

While .006s does not seem like a long time the above command only copied 2 files. If these files are large in size or if we start talking about millions of files, that .006s starts adding up.

#### Using tarpipe to copy files to a remote system

Sometimes you may need to copy files from one system to another retaining permissions and timestamps. Luckily tarpipe isn't only limited to local system copies, you can also use it to copy to remote systems through SSH. While on most modern systems its probably better/faster to use rsync, if you are supporting an older OS that doesn't have rsync this could save you sometime.

    $ tar -cf - file* | ssh remote-server "(cd /files_copied/ && tar -xf -)"
