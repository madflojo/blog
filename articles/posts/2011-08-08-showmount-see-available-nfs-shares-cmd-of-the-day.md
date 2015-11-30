
Showmount is a handy little command I've found out about in the recent few years. It allows you to see the available nfs shares on remote systems.

**Example:**

    $ showmount -e 192.168.0.110  
    Exports list on 192.168.0.110:  
    /volume1/music           192.168.0.1/24  
    /volume1/data            192.168.0.1/24
