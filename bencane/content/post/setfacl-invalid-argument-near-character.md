---
authors:
- Benjamin Cane
categories:
- Administration
- Command Line
- Linux
- Linux Commands
date: '2011-06-25T01:24:54'
draft: false
header:
  caption: ''
  image: ''
tags:
- acl
- linux
- tech
title: 'setfacl: Invalid argument near character'
url: /2011/06/25/setfacl-invalid-argument-near-character

---

Found out today that sometimes setfacl doesn't return an informative error.

**Example:**

    # setfacl -m u:someguy:rx test2  
    setfacl: Option -m: Invalid argument near character 3

The reason you get this error is because the **someguy** user does not exist. Setfacl will give the same error for groups that do not exist as well.
