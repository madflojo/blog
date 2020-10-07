---
authors:
- Benjamin Cane
categories:
- Administration
- Best Practices
- Linux
- Linux Commands
- Security
- Unix
- Unix Commands
date: '2011-07-16T02:43:59'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: 'sudoers: Syntax Checking'
url: /2011/07/16/sudoers-syntax-checking-best-practices

---

As you may recall I posted recently about the [safest way to deploy a crontab](http://bencane.com/2011/06/28/the-safest-way-to-deploy-a-crontab/). One of my points was using certain commands you can perform syntax checking on the file. Well crontab isn't the only command that performs syntax checking.

When you edit your sudoers file it is best practice that you use visudo rather than editing the /etc/sudoers file directly. Visudo will perform syntax checking when you save the file.

The question is how do you get syntax checking when using version control? The answer is actually pretty easy, by using visudo; visudo has a flag that will perform a syntax check on the sudoers file.

    [root@bcane ~]# visudo -c  
    /etc/sudoers: parsed OK

You can run this after deployment to ensure the syntax is correct.

Another cool feature of visudo is you can tell it to check a specified file rather than the /etc/sudoers file. This means you can also perform the visudo check on your repository server before you even check it in.

    [root@bcane ~]# visudo -cf /var/tmp/sudoers.new   
    /var/tmp/sudoers.new: parsed OK
