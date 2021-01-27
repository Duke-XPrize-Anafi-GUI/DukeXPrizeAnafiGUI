FROM ubuntu:18.04

LABEL maintainer="baran.yildirim@outlook.com"
# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y  \
    apt-utils \
    sudo \
	git \
    curl \
    python \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
    python3-tk \
    lsb-release \
	sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Build script refuses to be run as root, so we need a user
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R docker /home/
USER docker

# Install repo
RUN mkdir /home/docker/bin
ENV PATH "/home/docker/bin:$PATH"
RUN curl https://storage.googleapis.com/git-repo-downloads/repo > /home/docker/bin/repo
RUN chmod a+x /home/docker/bin/repo

# Install Sphinx
RUN sudo echo "deb http://plf.parrot.com/sphinx/binary `lsb_release -cs`/" | sudo tee /etc/apt/sources.list.d/sphinx.list > /dev/null
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 508B1AE5
RUN sudo apt update
RUN echo "parrot-sphinx sphinx/firmwared_users string toto" | sudo debconf-set-selections
RUN echo "parrot-sphinx sphinx/license_approval boolean true" | sudo debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive sudo apt-get install -q -y \
		parrot-sphinx
 
# Install olympe dependencies
RUN sudo apt-get -y install build-essential yasm cmake libtool libc6 libc6-dev \
    unzip freeglut3-dev libglfw3 libglfw3-dev libsdl2-dev libjson-c-dev \
    libcurl4-gnutls-dev libavahi-client-dev libgles2-mesa-dev

RUN sudo apt-get -y install rsync

RUN sudo apt-get -y install cmake libbluetooth-dev libavahi-client-dev \
    libopencv-dev libswscale-dev libavformat-dev \
    libavcodec-dev libavutil-dev cython python-dev python-opencv

RUN pip3 install clang

RUN mkdir -p /home/docker/code/parrot-groundsdk && \
    cd /home/docker/code/parrot-groundsdk && \
    repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git && \
    repo sync

RUN pip3 install scikit-build
RUN pip3 install -r /home/docker/code/parrot-groundsdk/packages/olympe/requirements.txt
RUN echo "export PYTHONPATH=\$PYTHONPATH:/home/docker/code/parrot-groundsdk/out/olympe-linux/final/usr/lib/python/site-packages/" >> /home/docker/code/parrot-groundsdk/products/olympe/linux/env/setenv


# Build olympe-linux
RUN cd /home/docker/code/parrot-groundsdk && \
    yes 'y' | ./build.sh -p olympe-linux -A all final -j

RUN sudo usermod -a -G firmwared docker
RUN cd && \
    git clone https://github.com/Duke-XPrize-Anafi-GUI/DukeXPrizeAnafiGUI

CMD  /bin/bash && cd
