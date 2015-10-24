
This is something I ran into recently over the weekend. I made modifications to the DNS of a domain and I couldn't get my mac to recognize the change.

The culprit was DNS caching, after flushing my DNS cache all was well.

    # dscacheutil -flushcache
