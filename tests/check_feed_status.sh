#!/bin/bash

curl -I -H "{ Host: feed.bencane.com }" \
  http://127.0.0.1 | grep -q "200 OK"
if [ $? -ge 1 ]
then
  echo "Keyword test failed"
  exit 1
fi
