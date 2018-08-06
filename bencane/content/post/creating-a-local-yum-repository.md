---
authors:
- Benjamin Cane
categories:
- How To and Tutorials
- Linux
- Linux Commands
- Linux Distributions
- Red Hat
date: '2013-04-15T12:30:44'
description: A walkthrough on creating your own local Yum Repository and keeping it
  synchronized automatically
draft: false
header:
  caption: ''
  image: ''
tags:
- config
- fedora
- linkedin
- proxy server
- red hat
- rpm
- yum
- yum local repository
- yum repositories
- yum repository
title: Creating a local Yum Repository
url: /2013/04/15/creating-a-local-yum-repository

---

When it comes to package management on Red Hat based systems Yum (Yellowdog Updater, Modified) is my preferred method. It's a quick and easy way of installing desired rpm's and their dependencies as Yum will automatically resolve dependencies before installation.

Most Red Hat base distributions include a public facing Yum repository that you can configure yum to use in order to save from having to maintain a local copy of every package on each system. While this is incredibly useful it also requires each system to have internet access; in many environments internet access on every server is not desirable.

In the below article I am going to show you how to set up one server with access to the internet (even over a proxy) and use it as a local Yum repository.

## Setting up the local Yum Repository Server

### Using a proxy with Yum

In order to keep the local repository current it is best to have that server able to connect to the internet and configured to use the desired distributions public repositories. Some environments may not allow direct access to the internet but rather through a proxy. The below configuration will allow Yum to connect to the public repositories via a proxy server.

    # vi /etc/yum.conf

**Append:**

    proxy=http://someproxyserver.com:8000
    proxy_username=proxyuser
    proxy_password=proxypass

Make sure when adding the proxy address that you specify which TCP port to connect to.

### Replicate the public mirrors packages with reposync

Reposync is a tool that allows you to synchronize each local directory with your current yum repositories. We will be using this command to download all of the relevant packages from the currently configured Yum repositories.

#### Install reposync

Reposync is installed with the yum-utils package, if you do not already have this package installed you can install it with yum.

    # yum install yum-utils

#### Synchronize with your configured repositories

For our example we are going to put all of our packages in `/var/www/html` so that we can present this directory with apache. If you are using another protocol such as ftp or nfs this directory may differ.

    # reposync -p /var/www/html/

### Create Yum XML Metadata with createrepo

Createrepo is a tool used to create the necessary XML Metadata files that Yum uses to know what packages are available. Every time a repository is updated with new or removed packages these XML Metadata files will need to be updated with createrepo.

    # createrepo /var/www/html/fedora/Packages

The test system I am using is fedora based and reposync created the `fedora/Packages` directories. Your path may very depending on your repo configuration.

#### Updating the XML Metadata

In order to keep this Yum repository up to date you can have `reposync` and `createrepo` run via cron. When updating the XML Metadata you can save some time and I/O operations by using the `--update` flag.

    # createrepo --update /var/www/html/fedora/Packages

### Make files available via Apache

Once all of the files are available on the local file system we need to make these files available to other systems. This can be done in a variety of ways as yum can support obtaining the files from multiple methods however we will use http for our example.

#### Install Apache

    # yum install httpd

#### Start Apache

Because we placed the repository in `/var/www/html` which is the default directory for Red Hat based Apache installations; we will not need to change any of the apache configuration. When implementing this you may want to review the configuration to ensure that it meets your security requirements.

    # chkconfig httpd on
    # service httpd start

At this point you should be able to point your browser to **http://ip_of_your_server/fedora/Packages** and see a directory listing of the downloaded packages.

## Configuring Yum Clients

#### Creating your Repo Configuration File

Now that the Yum Repository server is set up we will need to point the clients to this new repository. To do this we will create a repository configuration file.

    # vi /etc/yum.repos.d/local.repo

**Insert:**

    [Local-Repository]
    name=Fedora $releasever - $basearch - Local
    baseurl=http://ip_of_your_server/fedora/Packages
    enabled=1
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearc

The configuration above may need to change depending on the distribution you are using. The `gpgcheck` and `gpgkey` options are optional and can be disabled by setting `gpgcheck=0`.

After creating the new repository file any default repositories will need to be disabled as your clients will not have access to them. To do this edit any files except `local.repo` in `/etc/yum.repos.d/`

    # cd /etc/yum.repos.d
    # vi <default files>.repo

**Find:**

    enabled=1

**Replace with:**

    enabled=0

#### Refresh Yum Cached Repository List

After disabling the default repositories and enabling the new local repository, we will need to update Yum's cached repository list.

    # yum makecache
