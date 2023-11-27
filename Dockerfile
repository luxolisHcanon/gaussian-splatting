FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# FROM python:3
# FROM linuxserver/blender:3.5.0
# FROM linuxserver/blender:3.5.1

# Python install
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install AWS Cli and config
RUN pip3 install awscli && \
    aws configure set aws_access_key_id $AK && \
    aws configure set aws_secret_access_key $SK

WORKDIR /workdir
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod u+x ./docker_start.sh

ENV PORT=8080

EXPOSE ${PORT}

# DEVELOPMENT=False uvicorn main:app --host 0.0.0.0 --port 8090 --reload --log-level debug
# ENTRYPOINT /bin/bash
ENTRYPOINT /workdir/docker_start.sh
# ENTRYPOINT /bin/sh
# CMD uvicorn main:app --host 0.0.0.0 --port 8080 --log-level debug --reload
