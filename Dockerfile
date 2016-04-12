## Dockerfile that generates an instance of http://bencane.com

FROM nginx:latest
MAINTAINER Benjamin Cane <ben@bencane.com>

## NGINX custom config
RUN mkdir -p /etc/nginx/globals && rm -vf /etc/nginx/sites-enabled/*
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/htmlglobal.conf /etc/nginx/globals/
COPY nginx/bencane.com.conf /etc/nginx/sites-enabled/

## Install python and pip
RUN apt-get update && apt-get install -y \ 
    python-dev \ 
    python-pip \ 
    sysstat \
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*

## Create a directory for required files
RUN mkdir -p /build/

## Add requirements file and run pip
COPY requirements.txt /build/
RUN pip install -r /build/requirements.txt

## Add blog code nd required files
COPY static /build/static
COPY templates /build/templates
COPY hamerkop.py /build/
COPY config.yml /build/
COPY articles /build/articles

## Run Generator
RUN /build/hamerkop.py -c /build/config.yml
