FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
# FROM python:3

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Remove questions from the installs
ENV DEBIAN_FRONTEND=noninteractive

# install essentials
RUN apt-get update -y && \
    apt-get install software-properties-common -y && \
    apt install build-essential -y

# Python install
RUN apt-get update && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install -y python3.8 && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Pre-install conda
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Install conda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    mkdir /root/.conda && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda --version

# Create conda env
RUN conda env create --file environment.yml && \
    conda activate gaussian_splatting

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
