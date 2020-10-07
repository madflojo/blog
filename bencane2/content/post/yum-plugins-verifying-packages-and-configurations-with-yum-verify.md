---
authors:
- Benjamin Cane
categories:
- Linux
- Yum
- Red Hat
date: '2013-12-23T08:00:00'
description: An introduction to Yum Plugins and Yum Verify
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- redhat
- yum
- yum plugins
- centos
- package manager
- yellowdog update manager
title: 'Yum Plugins: Verifying packages and configurations with Yum Verify'
url: /2013/12/23/yum-plugins-verifying-packages-and-configurations-with-yum-verify

---

While taking a Red Hat Training course the instructor showed us a Yum plugin called verify. I've never used any of the Yum plugins before and after a while of playing with Yum Verify, I have decided that I should share this very cool plugin and introduce others to Yum plugins.

## What are Yum Plugins

Yum plugins are packages that can be installed to provide extra functionality to the **Yellowdog Update Manager** or `yum`. A plugin my provide an extra command or something for yum to execute in the background like finding the fastest mirror. There are quite a few Yum plugins available, for a comprehensive list you can check out [The Yum Wiki](http://yum.baseurl.org/wiki/YumUtils#Plugins).

### Enable or Disable yum plugins

You can enable or disable the ability to use yum plugins by editing the `/etc/yum.conf`. Within the `[main]` section there should be an entry for **plugins**, To enable the use of plugins we will change this value to `1`.

#### To Enable All Plugins

    # vi /etc/yum.conf

**Find:**

    plugins=0

**Replace With:**

    plugins=1

If the plugins entry is not already in the `/etc/yum.conf` file you can add it anywhere under the `[main]` section.

#### To Disable All Plugins

    # vi /etc/yum.conf

**Find:**

    plugins=1

**Replace With:**

    plugins=0


### Enable or Disable individual yum plugins

In addition to enabling or disabling all yum plugins, you can enable or disable an individual plugin as well. This is helpful if a specific package is interfering with the installation, removal of upgrading of a specific package.

#### To Disable A Specific Plugin

Each plugin has it's own configuration file in `/etc/yum/pluginconf.d/`. By default an installed plugin is enabled, but they can be disabled by changing the `enabled=1` value to `0`.

    # vi /etc/yum/pluginconf.d/<plugin-name>.conf

**Find:**

    enabled=1

**Replace With:**

    enabled=0

To re-enable the plugin you can switch `enabled=0` to `enabled=1`. 

As a word of advice, if a specific plugin is interfering with the installation of a package I highly recommend disabling that specific package before disabling all plugins.

## Yum Plugin: Verify

The verify plugin is the main reason I wanted to write this article. It adds the ability for yum to validate that installed packages are "intact" per the packages specification. As an example if you suspected that the permissions of a configuration file are modified or a binary was removed. You could simply run `yum verify-all` to identify if that configuration was modified outside of the packages specifications. This can be extremely useful when troubleshooting a broken server.

## Install yum-verify

To get started with Yum Verify we will first need to install the plugins package.

    # yum install yum-plugin-verify

Once the package is installed we can start using it.

### Verify a Specific Package

First we will run verify against the grep package that is currently untouched.

    # yum verify grep
    Loaded plugins: fastestmirror, verify
    verify done

As you can see verify did not detect any abnormalities about the grep package. At least, not yet.

    # chmod 0 /bin/grep
    # yum verify grep
    Loaded plugins: fastestmirror, verify
    ==================== Installed Packages ====================
    grep.x86_64 : Pattern matching utilities
    File: /bin/grep
    Problem: mode does not match
    Current: user:---, group:---, other:---
    Original: user:wrx, group:-rx, other:-rx
    verify done

After I had changed the permissions on the grep binary, Yum verify was able to detect that the permissions on the grep binary had been changed and reported it back.

### Verify all packages

You can also run yum verify against all packages by running `yum verify-all`. The `verify-all` option works in a similar way to `verify`, however it is used to identify all changes to all packages. The `verify-all` option can be extremely useful if you are not aware of which package might be causing the issue.

    # yum verify-all
    udev.x86_64 : A userspace implementation of devfs
    File: /etc/dev.d
    Tags: ghost
        Problem:  file is missing
    File: /etc/scsi_id.config
    Tags: ghost, configuration, missing ok
        Problem:  file is missing
    File: /etc/udev/devices
    Tags: ghost
        Problem:  file is missing
    File: /etc/udev/scripts
    Tags: ghost
        Problem:  file is missing

As a word of warning, just because a file has been modified outside of the original packages specification does not necessarily mean that it is not working correctly. Configuration files are designed to be modified, so when it comes to config files take the output of yum verify with a grain of salt. Binaries however, are a different story. In general if a binary doesn't match the packages there is either a very good reason or it is potentially a problem. Either way, Yum verify is a great tool for finding inconsistencies within a broken server.
