#!/bin/bash

curl -H "{ Host: feed.bencane.com }" \
  http://127.0.0.1 | grep -q "rss"
if [ $? -ge 1 ]
then
  echo "RSS Keyword test failed"
  exit 1
fi
