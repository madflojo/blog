---
authors:
- Benjamin Cane
categories:
- Bash Scripting
date: '2014-06-06T07:00:00'
description: This article covers some simple bash scripting best practices that can
  be used to improve the quality of your shell scripts.
draft: false
header:
  caption: ''
  image: ''
tags:
- linux
- unix
- bash
- bash scripts
- bash best practices
- shell scripting
- linux shell scripts
- linux scripting
title: 8 Tips for creating better bash scripts
url: /2014/06/06/8-tips-for-creating-better-bash-scripts

---

When I was first got started with administrating Linux and Unix servers I was working in an environment where there were tons of adhoc scripts that other admins wrote. From time to time I would find myself troubleshooting why one of those scripts suddenly stopped working. Sometimes the scripts would be well written and easy to understand, other times they were clunky and confusing. 

While troubleshooting the poorly written scripts was always a hassle at the time, it taught me an important lesson. It showed me that even if you don't think a script is going to be used beyond today, it is always best to write your scripts as if someone will be troubleshooting them 2 years later. Because, someone might be and sometimes that someone might even be yourself. 

For today's article I wanted to cover a few tips that will make your scripts better, not better for you but better for the next person who has to figure out why it isn't working anymore.

## Always start with a shebang

The first rule of shell scripting is that you always start your scripts with a shebang. While the name might sound funny the shebang line is very important, this line tells the system which binary to use as the interpreter for the script. Without the shebang line, the system doesn't know what language to use to process the script script.

A typical bash shebang line would look like the following:

    #!/bin/bash

I have seen many scripts were this line is missing, one would think if it wasn't there than the script wouldn't work but that's not necessarily true. If a script does not have an interpreter specified then some systems will default to `/bin/sh`. While defaulting to `/bin/sh` would be ok if the script is written for bourne shell, if the script is written for KSH or uses something specific to bash and not bourne than the script may produce unexpected results. 

Unlike some of the other tips in this article this one is not just a tip but rather a rule. You must always start your shell scripts with the interpreter line; without it your scripts will eventually fail.

## Put a description of the script in the header

Whenever I create a script or any program for that matter I always try to put a description of what the script will do in the beginning of the script. I also include my name and if I am writing these scripts for work, I will include my work email address as well as a date that the script was written. 

Here is an example header.

    #!/bin/bash
    #### Description: Adds users based on provided CSV file 
    #### CSV file must use : as separator
    #### uid:username:comment:group:addgroups:/home/dir:/usr/shell:passwdage:password
    #### Written by: Benjamin Cane - ben@example.com on 03-2012

Why do I put all of this? Well it's simple. The description is there to explain to anyone who is reading through the script what this script does and any information they need to know about it. I include my name and email on the chance that if someone was reading this script and they had a question for me they could reach out and ask. I include the date so that when they are reading the script they at least have some context as to how long ago the script was written. The date also adds a bit of nostalgia when you find a script you've written long ago and ask yourself "What was I thinking when I wrote this?".

A descriptive heading in your scripts can be as custom as you want it to be, there is no hard fast rule of what needs to be in there and what doesn't. In general, just keep it informative and make sure you put it at the top of the script.

## Indent your code

Making your code readable is very important, it's something that a lot of people seem to forget as well. Before we get too far into why indentation is important let's look at an example.

    NEW_UID=$(echo $x | cut -d: -f1)
    NEW_USER=$(echo $x | cut -d: -f2)
    NEW_COMMENT=$(echo $x | cut -d: -f3)
    NEW_GROUP=$(echo $x | cut -d: -f4)
    NEW_ADDGROUP=$(echo $x | cut -d: -f5)
    NEW_HOMEDIR=$(echo $x | cut -d: -f6)
    NEW_SHELL=$(echo $x | cut -d: -f7)
    NEW_CHAGE=$(echo $x | cut -d: -f8)
    NEW_PASS=$(echo $x | cut -d: -f9)    
    PASSCHK=$(grep -c ":$NEW_UID:" /etc/passwd)
    if [ $PASSCHK -ge 1 ]
    then
    echo "UID: $NEW_UID seems to exist check /etc/passwd"
    else
    useradd -u $NEW_UID -c "$NEW_COMMENT" -md $NEW_HOMEDIR -s $NEW_SHELL -g $NEW_GROUP -G $NEW_ADDGROUP $NEW_USER
    if [ ! -z $NEW_PASS ]
    then
    echo $NEW_PASS | passwd --stdin $NEW_USER
    chage -M $NEW_CHAGE $NEW_USER
    chage -d 0 $NEW_USER 
    fi
    fi

Does the above code work, yes but it's not very pretty and if this was a 500 line bash script without any indentation it would be pretty hard to understand what's going on. Now let's look at the same code with indentation.

    NEW_UID=$(echo $x | cut -d: -f1)
    NEW_USER=$(echo $x | cut -d: -f2)
    NEW_COMMENT=$(echo $x | cut -d: -f3)
    NEW_GROUP=$(echo $x | cut -d: -f4)
    NEW_ADDGROUP=$(echo $x | cut -d: -f5)
    NEW_HOMEDIR=$(echo $x | cut -d: -f6)
    NEW_SHELL=$(echo $x | cut -d: -f7)
    NEW_CHAGE=$(echo $x | cut -d: -f8)
    NEW_PASS=$(echo $x | cut -d: -f9)    
    PASSCHK=$(grep -c ":$NEW_UID:" /etc/passwd)
    if [ $PASSCHK -ge 1 ]
    then
      echo "UID: $NEW_UID seems to exist check /etc/passwd"
    else
      useradd -u $NEW_UID -c "$NEW_COMMENT" -md $NEW_HOMEDIR -s $NEW_SHELL -g $NEW_GROUP -G $NEW_ADDGROUP $NEW_USER
      if [ ! -z $NEW_PASS ]
      then
          echo $NEW_PASS | passwd --stdin $NEW_USER
          chage -M $NEW_CHAGE $NEW_USER
          chage -d 0 $NEW_USER 
      fi
    fi

With the indented version it is a lot more apparent that the second if statement is nested within the first, you may not catch that at first glance if you were looking at the un-indented code. 

The [style of indentation](http://en.wikipedia.org/wiki/Indent_style) is up to you, whether you want to use 2 spaces, 4 spaces or just a generic tab it doesn't really matter. What matters is that the code is consistently indented the same way every time.

## Add Spacing

Where indentation can help make code understandable, spacing helps make code readable. In general I like to space code out based on what the code is doing, again this is a preference and really the point is just make the code more readable and easy to understand.

Below is an example of spacing with the same code as above.

    NEW_UID=$(echo $x | cut -d: -f1)
    NEW_USER=$(echo $x | cut -d: -f2)
    NEW_COMMENT=$(echo $x | cut -d: -f3)
    NEW_GROUP=$(echo $x | cut -d: -f4)
    NEW_ADDGROUP=$(echo $x | cut -d: -f5)
    NEW_HOMEDIR=$(echo $x | cut -d: -f6)
    NEW_SHELL=$(echo $x | cut -d: -f7)
    NEW_CHAGE=$(echo $x | cut -d: -f8)
    NEW_PASS=$(echo $x | cut -d: -f9)    

    PASSCHK=$(grep -c ":$NEW_UID:" /etc/passwd)
    if [ $PASSCHK -ge 1 ]
    then
      echo "UID: $NEW_UID seems to exist check /etc/passwd"
    else
      useradd -u $NEW_UID -c "$NEW_COMMENT" -md $NEW_HOMEDIR -s $NEW_SHELL -g $NEW_GROUP -G $NEW_ADDGROUP $NEW_USER

      if [ ! -z $NEW_PASS ]
      then
          echo $NEW_PASS | passwd --stdin $NEW_USER
          chage -M $NEW_CHAGE $NEW_USER
          chage -d 0 $NEW_USER 
      fi
    fi

As you can see the spacing is subtle but every little bit of cleanliness can help make the code easier to troubleshoot later.

## Comment your code

Where the header is great for adding a description of the scripts function adding comments within the code is great for explaining whats going on within the code itself. Below I will show the same code snippet from above but this time I will add comments to the code that explains what it does.

    ## Parse $x (the csv data) and put the individual fields into variables
    NEW_UID=$(echo $x | cut -d: -f1)
    NEW_USER=$(echo $x | cut -d: -f2)
    NEW_COMMENT=$(echo $x | cut -d: -f3)
    NEW_GROUP=$(echo $x | cut -d: -f4)
    NEW_ADDGROUP=$(echo $x | cut -d: -f5)
    NEW_HOMEDIR=$(echo $x | cut -d: -f6)
    NEW_SHELL=$(echo $x | cut -d: -f7)
    NEW_CHAGE=$(echo $x | cut -d: -f8)
    NEW_PASS=$(echo $x | cut -d: -f9)    

    ## Check if the new userid already exists in /etc/passwd
    PASSCHK=$(grep -c ":$NEW_UID:" /etc/passwd)
    if [ $PASSCHK -ge 1 ]
    then
      ## If it does, skip
      echo "UID: $NEW_UID seems to exist check /etc/passwd"
    else
      ## If not add the user
      useradd -u $NEW_UID -c "$NEW_COMMENT" -md $NEW_HOMEDIR -s $NEW_SHELL -g $NEW_GROUP -G $NEW_ADDGROUP $NEW_USER

      ## Check if new_pass is empty or not
      if [ ! -z $NEW_PASS ]
      then
          ## If not empty set the password and pass expiry
          echo $NEW_PASS | passwd --stdin $NEW_USER
          chage -M $NEW_CHAGE $NEW_USER
          chage -d 0 $NEW_USER 
      fi
    fi

If you were to happen upon this snippet of bash code and didn't know what it did you could at least look at the comments and get a pretty good understand of what the goal is. Adding comments to your code will be extremely helpful to the next guy, and it might even help you out. I've found myself looking through a script I wrote maybe a month earlier wondering what I was doing. If you add comments religiously it can save you and others a lot of time later.

## Create descriptive variable names

Descriptive variable names might seem like an obvious thing but I find myself using generic variable names all the time. Most of the time these variables are temporary and never used outside of that single code block, but even with temporary variables it is always good to put an explanation of what values they contain. 

Below is an example of variable names that are mostly descriptive.

    for x in `cat $1`
    do
        NEW_UID=$(echo $x | cut -d: -f1)
        NEW_USER=$(echo $x | cut -d: -f2)

While it might be pretty obvious what goes into `$NEW_UID` and `$NEW_USER` it is not necessarily obvious what the value of `$1` is, or what is being set as `$x`. A more descriptive way of writing this same code can be seen below.

    INPUT_FILE=$1
    for CSV_LINE in `cat $INPUT_FILE`
    do
      NEW_UID=$(echo $CSV_LINE | cut -d: -f1)
      NEW_USER=$(echo $CSV_LINE | cut -d: -f2)

With the rewritten block of code it is very apparent that we are reading an input file and that file is a CSV file. It is also more apparent where we are getting the new UID and new USER information to store in the `$NEW_UID` and `$NEW_USER` variables.

The exmaple above might seem like a bit of overkill but someone may thank you later for taking a little extra time to be more descriptive with your variables.

## Use $(command) for command substitution

If you want to create a variable that's value is derived from another command there are two ways to do it in bash. The first is to wrap the command in back-ticks such as the example below.

    DATE=`date +%F`

The second method uses a different syntax.

    DATE=$(date +%F)

While both are technically correct, I personally prefer the second method. This is purely personal prefrence, but in general I think that the `$(command)` syntax is more obvious than using back-ticks. Let's say for example you are digging through hundreds of lines of bash code; you may find as you read and read that sometimes those back-ticks start looking like single quotes. On top of that, sometimes a single quote tends to look like a back-tick. At the end of the day, it all comes down to preference. So use what works best for you; just make sure you are being consistent with the method you choose to use. 

## Before you exit on error describe the problem

We have gone though several examples of items that make it easier to read and understand code, but this last one is useful before the troubleshooting process even gets to that point. By adding descriptive errors in your scripts you can save someone a lot troubleshooting time early on. Let's take a look at the following code and see how we can make it more descriptive.

    if [ -d $FILE_PATH ]
    then
      for FILE in $(ls $FILE_PATH/*)
      do
        echo "This is a file: $FILE"
      done
    else
      exit 1
    fi

The first thing this script does is check if the value of the `$FILE_PATH` variable is a directory, if it isn't it will exit with a code of 1 which denotes an error. While it's great that we used an exit code that will tell other scripts that this script was not successful, it doesn't explain that to the humans running this script.

Let's make the code a little more human friendly.

    if [ -d $FILE_PATH ]
    then
      for FILE in $(ls $FILE_PATH/*)
      do
        echo "This is a file: $FILE"
      done
    else
      echo "exiting... provided file path does not exist or is not a directory"
      exit 1
    fi

If you were to run the first snippet, you would expect a huge amount of output. If you didn't get that output you would have to open the script up to see what could have possibly gone wrong. If you were to run the second code snippet however, you would know instantly that the path you gave the script wasn't valid. Adding just one line of code can save a lot of troubleshooting later. 

The above examples are just a few things I try to use whenever I write scripts. I'm sure there are other great tips for writing clean and readable bash scripts, if you have any feel free to drop them in the comments box. It's always good to see what tricks others come up with.
