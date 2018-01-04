#!/bin/bash
## Redeploy the blog if necessary

NEW_IMAGE=$(docker pull madflojo/blog | grep -q Download && echo true || echo false)

if [ $NEW_IMAGE == "true" ]
then
  echo "Removing old container"
  docker rm -f blog
  echo "Starting new container"
  docker run -d --restart=always -p 80:80 --name blog madflojo/blog
fi
