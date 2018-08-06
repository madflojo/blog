---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Automation Tools
- Command Line
- How To and Tutorials
- Linux
- Saltstack
date: '2013-09-23T09:49:08'
description: A guide on using the Remote Command Execution abilities of SaltStack
draft: false
header:
  caption: ''
  image: ''
tags:
- automation tool
- automation tools
- configuration management
- linux os
- nginx
- saltstack
- scripting
- scripts
- servers
- shell commands
- ssh
- systems automation
- ubuntu linux
- ubuntu os
- unix
- unix and linux
- unix linux
title: Remote Command Execution with SaltStack
url: /2013/09/23/remote-command-execution-with-saltstack

---

A few weeks back I wrote an article [Getting started with SaltStack](http://bencane.com/2013/09/03/getting-started-with-saltstack-by-example-automatically-installing-nginx/); that article covered Configuration and Package Automation with Saltstack. In Today's article I am going to cover SaltStack's Remote Execution abilities, a feature that I feel Saltstack has implemented better than other automation tools.

## Running a command in a State

If you remember from the previous article SaltStack's states are permanent configurations. Adding a command in a Salt state is used when you want to have a command that is run after provisioning a server, run every time Salt manages the state of the system or run when certain conditions are true.

For today's article we will be using the same nginx state file as our last article.

For this example let's pretend that we want to execute the script /root/scripts/test.sh on systems with the nginx software loaded. To do this we can simply add the command into the nginx state file.

**On the Salt Master edit the nginx/init.sls file:**

    # vi /salt/states/base/nginx/init.sls

**Append the following:**

    test.sh:
      cmd:
        - run
        - name: /root/scripts/test.sh

The above entry will tell Salt to run the command named `/root/scripts/test.sh` every time the systems state is managed.

### Using onlyif and unless

What if we only want to run the command when certain conditions are true? Well salt can handle that too. We can us the `onlyif` and `unless` options to tell Salt to only run the command if certain conditions are met.

#### Onlyif

`Onlyif` will execute the command only if the supplied command is true. In the below example we will only execute test.sh if the file exists.

**Example:**

    test.sh:
      cmd:
        - run
        - name: /root/scripts/test.sh
        - onlyif: test -f /root/scripts/test.sh

#### Unless

While `onlyif` executes the named command if the supplied command returns true, `unless` will only execute the named command if the supplied command returns false. In this example we will execute the command test.sh only when the nginx configtest fails.

**Example:**

    test.sh:
      cmd:
        - run
        - name: /root/scripts/test.sh
        - unless: /usr/sbin/service nginx configtest

### Stateful commands

If you want Salt to understand whether your script passed or failed you can do this by making the command `stateful`.

#### Adding stateful to the state file

In the state file we will tell Salt that the command is stateful by appending `- stateful: True`.

**Example:**

    test.sh:
      cmd:
        - run
        - name: /root/scripts/test.sh
        - unless: /usr/sbin/service nginx configtest
        - stateful: True

#### Adding state status to the script

Now that salt knows the command is "stateful" the script must also tell Salt what has changed and if it was successful or not. To do this you can append two lines at the end of the scripts output.

**Example of a good run:**

    echo "" ## This echos an empty line and is required
    echo "changed=yes comment='I executed something and it changed'"

**Example of a failed run:**

    echo "" ## This echos an empty line and is required
    echo "changed=no comment='I executed something and it did not change'"

It's ok if your script also has other output. Salt will only be looking at the last two lines of output; so you must make sure that these lines are at the end. For more information about running commands in states check out the [Saltstack cmd state docs](http://docs.saltstack.com/ref/states/all/salt.states.cmd.html#execution-of-arbitrary-commands).

## Running adhoc commands with Salt

Unlike many configuration management tools, Saltstack can be used to run one time only commands as well. This functionality along with the ability to filter which minions to execute the command on, is one of the key things that I feel sets Saltstack apart from other automation tools.

### Running an adhoc command on all hosts

To run a command on all of the minions the syntax is pretty basic. We will call salt with the cmd.run module and then supply it with a command to run followed by single or double quotes.

    # salt '*' cmd.run "<command to execute>"

The below example shows running the `hostname -s` command via Saltstack on all of the attached minions.

**Example:**

    # salt '*' cmd.run "hostname -s"
    dbsalt01:
      dbsalt01
    websalt02:
      websalt02
    websalt:
      websalt
    saltminion:
      saltminion

### Running an adhoc command on specific hosts

While running commands on every host is great for many tasks, it is rare that we actually want to run a command on every single host. Usually we want to run a command on a subset of hosts. Below I am going to show a few examples of how this could be done.

#### Hostname globs

When calling salt you can use globs to specify a hostname pattern. For example if all of your mail servers had a naming convention of mailserver01, than you could simply use `mail*`. If you wanted to run a command on all of your development servers and they had a hostname of someserver.dev.example.com you could use `*dev.example.com`.

The below example will run service nginx restart on all of my servers that have a hostname that starts with `web`.

**Example:**

    # salt 'web*' cmd.run 'service nginx restart'
    websalt02:
      Restarting nginx: nginx.
    websalt:
      Restarting nginx: nginx.

#### Using Grains

In addition to globs you can also ask Salt to run commands based on the grains available on those hosts. To do this you can use the `-G` flag followed by the `grain:value` that you are looking for.

The below example will run `uname -r` on all of my Ubuntu hosts.

**Example:**

    # salt -G 'os:Ubuntu' cmd.run "uname -r"
    saltminion:
      3.2.0-53-generic
    websalt02:
      3.2.0-53-generic
    dbsalt01:
      3.2.0-53-generic
    websalt:
      3.2.0-53-generic

#### Using a list of hosts

If neither of the options above works for your situation, you could always simply specify the hostnames with the `-L` flag.

The below will only execute the "service nginx status" command on the hosts named **websalt** and **saltminion**.

**Example:**

  # salt -L 'websalt,saltminion' cmd.run "service nginx status"
    websalt:
      * nginx is running
    saltminion:
      * nginx is running

## Some things to keep in mind

### You can't run interactive scripts

While the remote execution abilities of Saltstack are great, there is one catch to them. Due to the method that Saltstack sends commands to systems; Saltstack is not expecting them to ask for user input. These types of commands will fail, as Saltstack cannot supply the expected input.

    # salt 'saltminion*' cmd.run "/root/scripts/test.sh"
    saltminion:
      Can I ask you something? [y/n]:
      Error! Failed to get user input

### You can run commands without SSH running

Saltstack communicates to the minions via ZeroMQ. This communication layer is outside of SSH, because of this you can use Saltstack to restart SSH on any servers where it may have died unexpectedly. This allows you to have a second path into a system without having to launch a KVM or go to the systems console.

    # salt 'saltminion*' cmd.run "service ssh status"
    saltminion:
      ssh stop/waiting
