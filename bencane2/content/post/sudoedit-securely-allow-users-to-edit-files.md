---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Best Practices
- How To and Tutorials
- Linux
- Linux Commands
- Security
- Unix
- Unix Commands
date: '2012-02-26T18:04:56'
draft: false
header:
  caption: ''
  image: ''
tags:
- editors
- linkedin
- linux
- security
- sudo
- sudoedit
- tech
- unix
- vi
title: 'Sudoedit: Securely allow users to edit files'
url: /2012/02/26/sudoedit-securely-allow-users-to-edit-files

---

Allowing unprivileged users to edit files that are normally beyond their rights is a task that is easy to perform however it requires a great deal of forethought to implement without opening security holes. You can give users the ability to edit privileged files by using User/Group Permissions, ACL's, or even sudo; but no matter which way you choose there are some things you must consider.

For an example lets take a look at 2 files `/etc/services` and `/etc/cron.daily/tmpwatch`; For these files lets ask ourself two basic questions you should always ask when allowing unprivileged users the ability to write to privileged files.

**1. Is this file executable?**

**Answer:** `/etc/services` is a file with permissions of 644 and owned by root:root (in general). `/etc/cron.daily/tmpwatch` however is a file with permissions of 755 and owned by root:root.

**Comment:** Simply having these permissions in this case doesn't mean someone can exploit your server but it is an indicator that this script is often executed.

**2. Is this file executed by privileged users?**

**Answer:** `/etc/services` is a file that is read by many different applications but never executed. `/etc/cron.daily/tmpwatch` is executed daily by cron and cron will run this script with root privileges.

**Comment:** Because the process runs as root if someone puts a command in this script it will be run as root as well thus allowing the user to execute any command they wish.

After answering these 2 questions it seems pretty obvious that allowing a user to edit `/etc/services` seems pretty benign however allowing a user to edit `/etc/cron.daily/tmpwatch` can be extremely dangerous.

## How and why to setup sudoedit

When I want to give users the ability to edit files I generally lean towards User/Group permissions or ACL's; however not every environment is the same. In certain situations you will need to use sudo to give the users the ability to edit files. Whenever you use sudo to edit files you should always use sudoedit over your normal editors such as vi, emacs, or others.

Let's look at the below example of why you should avoid the normal editors.

**sudo rule:**
     
     testuser	ALL = (root) NOPASSWD: /bin/vi /etc/services

The above rule looks pretty secure right? It only allows the user to edit `/etc/services` right? **Wrong.**
     
     [testuser@laptop ~]$ sudo vi /etc/services
     (In vi hit esc and type the following)
     :!bash
     [root@laptop testuser]# whoami
     root

As you can see it didn't take very long for me to gain root access with vi, and the same can be said with most other editors as well. Most editors have the ability to break out into a sub shell and when invoked by sudo the sub shell will have the permissions of the user running the program. Which in this case, was root.

To show how sudoedit is different we are going to try the same thing.

**sudo rule:**
     
     testuser	ALL = (root) NOPASSWD: sudoedit /etc/services

Rather than using vi you simply use the command sudoedit in its place.
     
    [testuser@laptop ~]$ sudoedit /etc/services
    (In vi hit esc and type the following)
    :!bash 
    [testuser@laptop ~]$ whoami 
    testuser

As you can see sudoedit dropped me into a subshell just like vi does, but this time I'm still the unprivileged user. This is one of the many ways sudo edit can give you the flexibility to edit files without sacrificing your security.

As a caveat I do want to say that in general when giving users permissions to edit files I usually choose sudoedit last. I do this because in the past there have been ways to exploit sudo edit and gain elevated privileges but that is only because the command is running as a different user. It's a lot harder to exploit a set of ACL's or User/Group privileges than it is to exploit sudo, but when you need it sudoedit is a great alternative to allowing users to just use vi with sudo.
