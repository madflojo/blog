---
date: 2011-06-25 01:24:54+00:00
slug: setfacl-invalid-argument-near-character
title: 'setfacl: Invalid argument near character'
post_id: 2
categories:
- Administration
- Command Line
- Linux
- Linux Commands
tags:
- acl
- linux
- tech
popularity: None
---

Found out today that sometimes setfacl doesn't return an informative error.

**Example:**

    # setfacl -m u:someguy:rx test2  
    setfacl: Option -m: Invalid argument near character 3

The reason you get this error is because the **someguy** user does not exist. Setfacl will give the same error for groups that do not exist as well.
