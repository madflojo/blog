
I figured I would start a new category for command line quickies. Here is one that I have found very useful.

    # find ./ -type f -daystart -ctime -1

This is a very nice way of finding files created today. Now this command differs from the command below.

    # find ./ -type f -ctime -1

The `-daystart` flag will tell find to use the beginning of the day when searching for files created today. Without daystart the `ctime -1` flag will tell find to find files created in the last 24 hours.
