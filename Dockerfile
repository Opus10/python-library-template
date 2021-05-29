FROM circleci/python:3.9.4

# Install git 2.22 from source
RUN sudo apt-get update
RUN sudo apt-get install gettext
RUN cd /usr/src/ && \
    sudo wget https://github.com/git/git/archive/v2.23.0.tar.gz -O git.tar.gz && \
    sudo tar -xf git.tar.gz && \
    cd /usr/src/git-* && \
    sudo make prefix=/usr/local all && \
    sudo make prefix=/usr/local install && \
    sudo make clean && \
    sudo rm -r /usr/src/git*

# Pipx
ENV PATH=/home/circleci/.local/bin:$PATH
RUN pip install --user pipx
RUN pipx install poetry

# Python 3.6.13
RUN sudo curl -O https://www.python.org/ftp/python/3.6.13/Python-3.6.13.tgz
RUN sudo tar -xvzf Python-3.6.13.tgz
RUN cd Python-3.6.13 && sudo ./configure --prefix=/usr/
RUN cd Python-3.6.13 && sudo make
RUN cd Python-3.6.13 && sudo make install

# Python 3.7.10
RUN sudo curl -O https://www.python.org/ftp/python/3.7.10/Python-3.7.10.tgz
RUN sudo tar -xvzf Python-3.7.10.tgz
RUN cd Python-3.7.10 && sudo ./configure --prefix=/usr/
RUN cd Python-3.7.10 && sudo make
RUN cd Python-3.7.10 && sudo make install

# Python 3.8.10
RUN sudo curl -O https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
RUN sudo tar -xvzf Python-3.8.10.tgz
RUN cd Python-3.8.10 && sudo ./configure --prefix=/usr/
RUN cd Python-3.8.10 && sudo make
RUN cd Python-3.8.10 && sudo make install

RUN sudo apt-get install postgresql-client
# Solves issues with pip
# https://github.com/pypa/pip/issues/4924
RUN sudo rm /usr/bin/lsb_release

# Upgrade pip
RUN pip install -U pip

