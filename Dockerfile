## Dockerfile that generates an instance of http://bencane.com

FROM nginx:latest
MAINTAINER Benjamin Cane <ben@bencane.com>

## Create a directory for required files
RUN mkdir -p /build/
## Install python and pip
RUN apt-get update
RUN apt-get install -y python-dev python-pip

## Add requirements file and run pip
COPY requirements.txt /build/
RUN pip install -r /build/requirements.txt

## Add blog code nd required files
COPY config.yml /build/
COPY templates /build/templates
COPY static /build/static
COPY hamerkop /build/
COPY articles /build/articles

## Run Generator
RUN /build/hamerkop -c /build/config.yml
