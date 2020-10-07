---
authors:
- Benjamin Cane
categories:
- All Articles
- Command Line
- Linux
- Linux Commands
- Unix
- Unix Commands
date: '2012-08-13T11:30:38'
draft: false
header:
  caption: ''
  image: ''
tags:
- bash
- chmod command
- examples of xargs
- exec
- find
- gnu
- gnu linux
- gnu xargs
- i/o
- linkedin
- linux
- process
- shell
- stdin
- unix
- xargs
- xargs examples
title: 'xargs: Build and Execute Commands with Arguments from Standard Input'
url: /2012/08/13/xargs-build-and-execute-commands-with-arguments-from-standard-input

---

For me when it comes to useful commands xargs ranks along side commands like find, top and df; xargs is a great time saver and incredibly useful. Today I will show a few examples of usage and some of the lesser known features.

## Basic Usage

The xargs command is used to take the output of one command and provide it as arguments to another.

**Example (xargs):**
     
     # ls [0-9]-test.xml | xargs chmod -v 644
      mode of `1-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `2-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `3-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `4-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `5-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `6-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `7-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `8-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)
      mode of `9-test.xml' changed from 0664 (rw-rw-r--) to 0644 (rw-r--r--)

As you can see from the above command we were able to use xargs to run the chmod command based on the[output of the ls command being redirected to stdin](http://bencane.com/2012/04/unix-shell-the-art-of-io-redirection/). One of the reasons I say xargs is a great time saver is because the above command is still possible using a for loop or other methods however these non xargs methods require more typing which means it takes more time to write. This is especially true when the commands you want to run are more complicated than a basic chmod.

Note: While the example is pretty basic and there are a million ways to do this; keep in mind I'm keeping the examples basic for newer readers.

**Example (for-loop):**

     # for x in `ls [0-9]-test.xml`
      > do
      > chmod -v 644 $x
      > done
      mode of `1-test.xml' retained as 0644 (rw-r--r--)
      mode of `2-test.xml' retained as 0644 (rw-r--r--)
      mode of `3-test.xml' retained as 0644 (rw-r--r--)
      mode of `4-test.xml' retained as 0644 (rw-r--r--)
      mode of `5-test.xml' retained as 0644 (rw-r--r--)
      mode of `6-test.xml' retained as 0644 (rw-r--r--)
      mode of `7-test.xml' retained as 0644 (rw-r--r--)
      mode of `8-test.xml' retained as 0644 (rw-r--r--)
      mode of `9-test.xml' retained as 0644 (rw-r--r--)

## Advanced Usage

### Grouping

One of the reasons xargs is helpful is because it will take the arguments and group them into one command line. In the above examples the for loop ran the chmod command 9 times where the xargs command simply ran one chmod command with 9 arguments.

We can use the -t argument of xargs to tell us what it is doing by printing it to stderr before executing the command.

**Example:**
     
     # ls [0-9]-test.xml | xargs -t echo
      echo 1-test.xml 2-test.xml 3-test.xml 4-test.xml 5-test.xml 6-test.xml 7-test.xml 8-test.xml 9-test.xml
      1-test.xml 2-test.xml 3-test.xml 4-test.xml 5-test.xml 6-test.xml 7-test.xml 8-test.xml 9-test.xml

As you can see there was only one echo command and 9 arguments given.

**--max-chars**

By default the xargs commands grouping is limited to 131072 characters however like most GNU tools you can configure that, with xargs the -s or `--max-chars` argument is used to change the character size limit.

**Example:**
     
     # ls [0-9]-test.xml | xargs -s 60 echo
      1-test.xml 2-test.xml 3-test.xml 4-test.xml 5-test.xml
      6-test.xml 7-test.xml 8-test.xml 9-test.xml

The above command can be useful if you wanted to limit or increase the number of arguments xargs can provide to your command, but figuring out how many characters are going to be in your output can be a bit annoying and time consuming.

**--max-args**

Since we are all about saving time, we can simply use the `-n` or `--max-args` option to specify the number of arguments rather than characters.

**Example:**
     
     # ls [0-9]-test.xml | xargs -n 5 echo
      1-test.xml 2-test.xml 3-test.xml 4-test.xml 5-test.xml
      6-test.xml 7-test.xml 8-test.xml 9-test.xml

If you wanted to increase the number of arguments past the default however you will need to use the `-s` or `--max-chars` as the `--max-args` argument still abides by the maximum characters limit.

### Multiple Processes

**--max-procs**

An option that works well with the `--max-args` feature is the -P or --max-procs option. By setting -P 0 this tells xargs to spawn as many commands as it needs to at once to execute the arguments. If you wanted to run the above example via two different echo commands at the same time you could do so with -P 0 or -P 2; however you would need to ensure that xargs splits the arguments to multiple commands with the -n option.

**Example:**
     
     # ls [0-9]-test.xml | xargs -n 5 -P 2 logger -s -i
      logger[1554]: 1-test.xml 2-test.xml 3-test.xml 4-test.xml 5-test.xml
      logger[1555]: 6-test.xml 7-test.xml 8-test.xml 9-test.xml

### Delimiters

As one reader pointed out in the [Cheat Sheet: 21 useful Find Commands](http://bencane.com/2012/07/cheat-sheet-21-useful-find-commands/) post that by default the delimiter for xargs is a space or newline, this can be a bit of a problem as output from commands can contain spaces or newlines or both. This is especially true as filenames in Unix & Linux can contain both spaces and newlines as well.

**Example:**
     
     # find ./ -type f | xargs -t chmod 644
      chmod 644 ./3 -test.xml ./2 -test.xml ./1 -test.xml ./4 -test.xml
      chmod: invalid mode: `-test.xml,-test.xml,-test.xml,-test.xml'
      Try `chmod --help' for more information.

As you can see xargs passed `3 -text.xml` as two arguments to the chmod command, which caused the chmod command to error.

**--null**

Since this error is most commonly seen with the find command the most common way around this is to make xargs use a null character as a seperator. This can be done with xargs by using the `-0` or `--null` argument, however you also need to insure that your first commands output also has the null character. For find you can use `-print0` to ensure find prints the null character.

**Example:**
     
     # find ./ -type f -print0 | xargs -t -0 chmod -v 644
      chmod -v 644 ./3 -test.xml ./2 -test.xml ./1 -test.xml ./4 -test.xml
      mode of `./3 -test.xml' retained as 0644 (rw-r--r--)
      mode of `./2 -test.xml' retained as 0644 (rw-r--r--)
      mode of `./1 -test.xml' retained as 0644 (rw-r--r--)
      mode of `./4 -test.xml' retained as 0644 (rw-r--r--)

**--delimiter**

Another way around this is to specify a delimiter with the `-d` or `--delimiter` flags.

**Example:**
     
     # cat input.file
      1 -test.xml:2 -test.xml:3 -test.xml:4 -test.xml:input.file
     
     # cat input.file | xargs -t -d: chmod -v 644
      chmod -v 644 1 -test.xml 2 -test.xml 3 -test.xml 4 -test.xml input.file
      mode of `1 -test.xml' retained as 0644 (rw-r--r--)
      mode of `2 -test.xml' retained as 0644 (rw-r--r--)
      mode of `3 -test.xml' retained as 0644 (rw-r--r--)
      mode of `4 -test.xml' retained as 0644 (rw-r--r--)
      mode of `input.file' retained as 0644 (rw-r--r--)

### Accept Input from file

**--arg-file**

Using the example above we can eliminate the cat command by simply providing xargs with the input file via the `-a` or `--arg-file` arguments.

**Example:**
     
     # xargs -a input.file -t -d: chmod -v 644
      chmod -v 644 1 -test.xml 2 -test.xml 3 -test.xml 4 -test.xml input.file
      mode of `1 -test.xml' retained as 0644 (rw-r--r--)
      mode of `2 -test.xml' retained as 0644 (rw-r--r--)
      mode of `3 -test.xml' retained as 0644 (rw-r--r--)
      mode of `4 -test.xml' retained as 0644 (rw-r--r--)
      mode of `input.file' retained as 0644 (rw-r--r--)

### Replacement Text

**-I**

When you are building a complicated command for xargs to run there are times where you may need to place the arguments in a specific order or multiple times. For this the -I flag can be used along with an arbitrary text to replace.

**Example:**
     
     $ ls [0-3]-test.xml | xargs -I replaceme find ./ -name <strong>replaceme</strong> -type f
      ./1-test.xml
      ./2-test.xml
      ./3-test.xml

There have been a few times in the past where I decided not to use xargs because I needed to specify arguments after the output from the first command. The -I flag takes care of all of those situations.

### Interactive Mode

**--interactive**

There are many times when using xargs where you may want to validate the command it is going to run before it runs the command. To do so you can simply put xargs into interactive mode with the -p flag.

**Example:**
     
     # ls [0-9]-test.xml | xargs -n 4 -p chmod 644
      chmod 644 1-test.xml 2-test.xml 3-test.xml 4-test.xml ?...y
      chmod 644 5-test.xml 6-test.xml 7-test.xml 8-test.xml ?...n
      chmod 644 9-test.xml ?...n

The xargs command will wait for either a `y|Y` or a `n|N` to either run the command or not.

As you can see the xargs command is very flexible and can be used to handle tons of situations without the need to write a bash for-loop or other lengthy commands. If you have any cool examples of xargs usage please add a comment and share them. Maybe next week I will make a Cheat Sheet post with the top examples.
