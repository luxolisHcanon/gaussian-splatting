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

# Install Colmap
RUN apt-get update && apt-get -y install colmap && \
    apt-get install -y \
        git \
        cmake \
        ninja-build \
        build-essential \
        libboost-program-options-dev \
        libboost-filesystem-dev \
        libboost-graph-dev \
        libboost-system-dev \
        libeigen3-dev \
        libflann-dev \
        libfreeimage-dev \
        libmetis-dev \
        libgoogle-glog-dev \
        libgtest-dev \
        libsqlite3-dev \
        libglew-dev \
        qtbase5-dev \
        libqt5opengl5-dev \
        libcgal-dev \
        libceres-dev

# Install Cuda toolkit and dependencies
RUN apt-get install -y \
        nvidia-cuda-toolkit \
        nvidia-cuda-toolkit-gcc && \
    apt-get install -y g++ freeglut3-dev build-essential libx11-dev \
        libxmu-dev libxi-dev libglu1-mesa-dev libfreeimage-dev libglfw3-dev && \
    apt-get install linux-headers-$(uname -r) && \
    sudo apt-get install gcc-10 g++-10  && \
    export CC=/usr/bin/gcc-10  && \
    export CXX=/usr/bin/g++-10  && \
    export CUDAHOSTCXX=/usr/bin/g++-10

# Install requirements
WORKDIR /workdir
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Create conda env
COPY . .
RUN conda env create --file environment.yml && \
    conda activate gaussian_splatting

RUN chmod u+x ./docker_start.sh

ENV PORT=8080

EXPOSE ${PORT}

# DEVELOPMENT=False uvicorn main:app --host 0.0.0.0 --port 8090 --reload --log-level debug
# ENTRYPOINT /bin/bash
ENTRYPOINT /workdir/docker_start.sh
# ENTRYPOINT /bin/sh
# CMD uvicorn main:app --host 0.0.0.0 --port 8080 --log-level debug --reload
