## Dockerfile that generates an instance of http://bencane.com

FROM nginx:stable
MAINTAINER Benjamin Cane <ben@bencane.com>

## NGINX custom config
RUN mkdir -p /etc/nginx/globals && rm -vf /etc/nginx/sites-enabled/*
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/htmlglobal.conf /etc/nginx/globals/
COPY nginx/bencane.com.conf /etc/nginx/sites-enabled/

## Install python and pip
#RUN apt-get update && \
#    apt-get install -y curl && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

## Create a directory for required files
RUN mkdir -p /build/

## Install Hugo
RUN cd / && curl -L https://github.com/gohugoio/hugo/releases/download/v0.62.1/hugo_0.62.1_Linux-64bit.tar.gz | tar -xvzf-
RUN cd / && curl -L https://github.com/tdewolff/minify/releases/download/v2.7.6/minify_2.7.6_linux_amd64.tar.gz | tar -xvzf-

## Add blog code nd required files
ADD bencane /bencane

## Run Generator
RUN cd /bencane && /hugo -d /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html/feed && cp /usr/share/nginx/html/index.xml /usr/share/nginx/html/feed/

## Add Resume, Stories, and Index
ADD resume /usr/share/nginx/html/resume
ADD stories /usr/share/nginx/html/stories
ADD ads.txt /usr/share/nginx/html/
#RUN cp -r /usr/share/nginx/html/resume/* /usr/share/nginx/html/
#RUN rm -f /usr/share/nginx/html/images/icon*
#RUN mkdir /usr/share/nginx/heavy && mv /usr/share/nginx/html/* /usr/share/nginx/heavy/ && \
#/minify -rs -o /usr/share/nginx/html /usr/share/nginx/heavy
ADD resume/resume.html /usr/share/nginx/html/resume/index.html
ADD resume/resume.html /usr/share/nginx/html/index.html
