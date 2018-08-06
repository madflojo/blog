---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Best Practices
- How To and Tutorials
- SysAdmin Basics
date: '2013-06-24T14:00:20'
description: An indepth guide on how to create and modify users and some simple tips
  that make user administration less of a nightmare
draft: false
header:
  caption: ''
  image: ''
tags:
- home directories
- linux
- linux os
- red hat os
- systems administration
- useradd
- usermod
title: Adding and Modifying Users and Groups in Linux
url: /2013/06/24/adding-and-modifying-users-groups-in-linux

---

Adding and Modifying Users and Groups is a core systems administration task. The act of adding a user and group is fairly easy however there are some tricks that help make the long-term management of users easier.

## Tips for easier management

#### Keep user attributes consistent amongst all systems

A common mistake sysadmins make when building a new environment is they will allow uid's, gid's, home directories and other user attributes to be mis-matched from system to system. While this isn't a big deal initially while managing users locally, this can be rather difficult to deal with when adding LDAP or other Authentication Services into your environment.

When you add Authentication Services into an environment user id's and group id's will need to be the same, if you take care of this and manage it early on than these tools will be easier to implement.

Consistency also helps with any custom scripts and general administration of the environment.

#### Define User and Group ID Ranges for People and Applications

When creating users it is a good practice to define a range for user and group id's based on the role of the user. For example on an environment I recently setup I specified all application UID's within the range of 2000 - 2999. I also specified that all people users will have a UID within the range of 4000 - 4999.

While I highly doubt that I will exceed more than 999 application users, I kept an extra 1,000 UID's available in the event that I do. By having the people users as the higher range I can easily extend that range without interfering with application User ID's if my environment exceeds 999 people users. I am more likely to reach 1000 unique people users than application users.

For group id's I have a similar configuration, GID's 500 - 699 are for applications, and GID's 800 - 899 are for people.

## Adding Users and Groups

Once you have defined your user and group attributes the act of adding the users and groups is fairly easy.

#### Adding a Group

While the command to add a user can also create a group for that user, if you want to specify the group id it is generally a good idea to create the group ahead of time.

To add a user group we will use the groupadd command.

    # groupadd -g 800 people

#### Adding a User

Within the Linux distributions there are several commands to add a user. The Debian based distributions seem to have many newer tools that make it easier for a sysadmin. Whereas the Red Hat based distributions seem to use the same old tools that have been around for a while. For consistency sake we will use the useradd command for this article, which is available amongst both distributions.

    # useradd -u 4000 -md /home/someuser -c "Some User" -g people -G specialpeople,others -s /bin/bash someuser

While there are many options available for the useradd command the above are the basics that most situations would need.

Let's breakdown the command a bit.

    # useradd -u uid -md homedir -c "comment" -g group -G additional groups -s usershell username

A couple of things that are not obvious from the above are, `-m` the **"m"** on the user directory specification tells useradd to create the user's directory if it does not exist. If only the `-d` option is given the directory will not be created.

The `-G` flag is used for adding the user to any additional groups outside their initial login group. If you need to add multiple additional groups they can be specified using a `,` to separate each group.

## Modifying Users and Groups

Sometimes you need to modify a user or user group, to either add them to an additional group, change their shell or change a groups GID.

#### Modifying a group with groupmod

The groupmod command is not used very often, really the only time that one would need to use it is to either change the GID of a group, or change the name of a group.

The below command will show both.

    # groupmod -g 802 -n otherpeeps others

#### Modifying a User with usermod

In the below example we will add the user to the "folks" group and change his shell to ksh; To do this we will use the usermod command.

    # usermod -aG folks -s /bin/ksh someuser

The usermod command utilizes the same flags as useradd, however in the example above there is a new flag `-a`. The `-a` flag is given to tell usermod to add the user to the folks group. Without the `-a` flag the user someuser would have been removed from the specialpeople and others group and added to the folks group.

## Print a Users UID and GID

While the `id` command does not change or create a user it is a good command to use to quickly display a users uid, gid, and assigned additional groups.

    # id someuser
    uid=4000(someuser) gid=800(people) groups=800(people),801(specialpeople),803(folks),802(otherpeeps)

## Deleting Users and Groups

After a user or group has been added they can be deleted with the groupdel and userdel commands. While the add and modify commands have many options the delete commands have very minimal.

#### Deleting a Group

    # groupdel folks

The groupdel command will remove all references of the folks group from the `/etc/group` file.

    # grep -c folks /etc/group
    0

#### Deleting a User

    # userdel -r someuser

The `-r` flag in the above command tells userdel to also remove the user's home directory, this is not the default action and is good practice if you are truly deleting the user for good and do not want the contents of their home directory.
