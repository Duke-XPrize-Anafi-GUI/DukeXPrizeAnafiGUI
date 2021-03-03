FROM ubuntu:18.04

LABEL maintainer="baran.yildirim@outlook.com"
# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y  \
    apt-utils \
    sudo \
    gnupg2 \
    python \ 
	git \
    curl \
    lsb-release \
    locales \ 
	sqlite3 && \
    rm -rf /var/lib/apt/lists/*


# Set Locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL en_US.UTF-8 
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en     

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
#RUN sudo echo "deb http://plf.parrot.com/sphinx/binary `lsb_release -cs`/" | sudo tee /etc/apt/sources.list.d/sphinx.list > /dev/null
#RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 508B1AE5
#RUN sudo apt update
#RUN echo "parrot-sphinx sphinx/firmwared_users string toto" | sudo debconf-set-selections
#RUN echo "parrot-sphinx sphinx/license_approval boolean true" | sudo debconf-set-selections
#RUN DEBIAN_FRONTEND=noninteractive sudo apt-get install -q -y \
		#parrot-sphinx
#RUN sudo usermod -a -G firmwared docker

# Install olympe dependencies
RUN mkdir -p /home/docker/code/parrot-groundsdk && \
    cd /home/docker/code/parrot-groundsdk && \
    repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git && \
    repo sync

RUN cd /home/docker/code/parrot-groundsdk && \
    echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections && \
    ./products/olympe/linux/env/postinst

# Build olympe-linux
RUN cd /home/docker/code/parrot-groundsdk && \
    yes 'y' | ./build.sh -p olympe-linux -A all final -j


RUN cd && \
    git clone https://github.com/Duke-XPrize-Anafi-GUI/DukeXPrizeAnafiGUI


# Need to change the version for aenum
# Otherwise olympe will error (olympe.messages not found)
RUN source ~/code/parrot-groundsdk/./products/olympe/linux/env/shell && \
    pip install --upgrade aenum==2.2.5 && \
    pip install image

CMD  /bin/bash && cd
