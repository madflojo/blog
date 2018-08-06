---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Best Practices
- Linux
- Linux Commands
date: '2011-06-28T04:16:00'
draft: false
header:
  caption: ''
  image: ''
tags:
- cron
- linux
- tech
title: The safest way to deploy a crontab
url: /2011/06/28/the-safest-way-to-deploy-a-crontab

---

Many would look at this topic and laugh at the simplicity of the subject, but in an environment where seconds of downtime are a matter of millions of dollars. This is anything but a simple subject.

In many cases some very important tasks run through cron, for a quick example log file cleanup. If log clean up doesn't occur eventually a filesystem can get out of hand and fill up causing an application to not be able to write logs. Which depending on how the application is designed could prove to be an outage.

I do recognize that the following is simply my opinion, feel free to come to your own conclusions but this is where I'm at.

In my case crontab files are controlled through a version control system, everyone running an enterprise environment with crontabs for application users should consider version controlling their crontab files.

## There are 3 main ways of deploying a crontab file

### 1. Edit the cron manually

    # crontab -u <user> -e

Pros:

  * Easy to perform
  * If crontab command is used then the edits are seen by crond without additional action
  * The crontab command will perform a syntax check

Cons:

  * Prone to copy & paste errors
  * Gives people freedom to add lines that may not match version control
  * Easy to forget the -u <username> or switching to user and running without -u

### 2. Copy the file to /var/spool/cron/

    # cp filename /var/spool/cron/  
    # touch /var/spool/cron

Pros:

  * Keeps file consistent with version control
  * Quick to perform
  * Difficult to deploy to wrong user

Cons:

  * Easy to forget to run the touch command
  * Does not perform any syntax checking

### 3. Copy the file to the server and deploy with the crontab command

    # crontab -u <user> /tmp/filename

Pros:

  * Keeps file consistent with version control
  * Quick to perform
  * Edits are seen by crond without additional action
  * Crontab command performs syntax checking

Cons:

  * Easy to miss the -u and deploy a file to the wrong user

In my opinion the safest way to deploy a crontab is #3.

1.  Proves to be a problem when people get lazy and forget to ensure the file matches your version control. This can lead to jobs going missing after a redeployment.
2.  Is actually probably the safest way to deploy the file, but the problem is everyone, and I mean EVERYONE forgets the touch command. Which if not run has the effect of crond not seeing the changes and keep running the old crontab file. This can lead to some very, very confusing troubleshooting.
3.  Could be somewhat dangerous if a person forgets the -u but it is the happy middle ground. It ensures the files integrity with version control but also ensures the new modifications are seen immediately by crond. If a person did mix up the -u you can implement procedures to have them validate the files are correct and if not you can re-deploy from version control.

At the end of the day someone can miss any type of step, and the goal as a system administrator is to minimize the impact of missed steps.

**Update** This topic sparked a bit of debate on my facebook feed but here are some additional tips from friends of mine.

  * Always use diff to validate your changes before executing - Evan
  * Using version control along with an automated configuration management (i.e. Puppet) is another good way of ensuring the files are deployed properly. - Brandon (I summarized)
