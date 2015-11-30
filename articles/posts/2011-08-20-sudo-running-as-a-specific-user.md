
Sudo is usually used to allow a user to run commands as root, but what happens if you want a user to run a command as another user?

You can use the example below to configure your sudo rule.

**Example:**

    [bcane@bcane ~]$ sudo -u sudoguy whoami  
    sudoguy

**The rule from /etc/sudoers:**

    bcane ALL=(sudoguy) /usr/bin/whoami, NOPASSWD: ALL

Same thing but instead of bcane the users group:

    %users ALL=(sudoguy) /usr/bin/whoami, NOPASSWD: ALL
