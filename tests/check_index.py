#!/usr/bin/env python

import requests
import sys

headers = { 'host' : sys.argv[1] }
r = requests.get("http://127.0.0.1", headers=headers)
if r.status_code != 200:
    print("GET Request returned invalid status code {}".format(r.status_code))
    sys.exit(1)

if "Benjamin Cane" in r.text:
    print("GET Request returned invalid HTML {}".format(r.status_code))
    sys.exit(1)

print("All checks pass")
sys.exit(0)
