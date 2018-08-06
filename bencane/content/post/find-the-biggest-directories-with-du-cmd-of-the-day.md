---
authors:
- Benjamin Cane
categories:
- Administration
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2011-08-14T20:30:05'
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- tech
- unix
title: Find the biggest directories with du
url: /2011/08/14/find-the-biggest-directories-with-du-cmd-of-the-day

---

If you ever need to find what directory is using up all of your filesystem space du is here to save the day.

**Example:**

    [bcane@bcane ~]$ du -k  
    148 ./.pulse  
    4 ./.mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}  
    8 ./.mozilla/extensions  
    4 ./.mozilla/firefox/lbtgx82r.default/extensions  
    44 ./.mozilla/firefox/lbtgx82r.default/bookmarkbackups  
    4 ./.mozilla/firefox/lbtgx82r.default/minidumps  
    288 ./.mozilla/firefox/lbtgx82r.default/Cache  
    12 ./.mozilla/firefox/lbtgx82r.default/chrome  
    46776 ./.mozilla/firefox/lbtgx82r.default  
    8 ./.mozilla/firefox/Crash Reports

As you can see by the output du is ordered by filename, if you want to order it by size of the file you can use sort.

**Example:**

    [bcane@bcane ~]$ du -k | sort -nrk 1  
    58864 .  
    46808 ./.mozilla  
    46792 ./.mozilla/firefox  
    46776 ./.mozilla/firefox/lbtgx82r.default  
    5920 ./Downloads  
    516 ./.gstreamer-0.10  
    320 ./.gconf  
    288 ./.mozilla/firefox/lbtgx82r.default/Cache  
    256 ./.gconf/apps  
    168 ./.local  
    164 ./.local/share  
