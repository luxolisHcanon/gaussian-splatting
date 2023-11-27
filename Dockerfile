FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# FROM python:3
# FROM linuxserver/blender:3.5.0
# FROM linuxserver/blender:3.5.1

# install essentials
RUN apt install build-essential -y

# Python install
RUN apt-get update && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install -y python3.8 && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
