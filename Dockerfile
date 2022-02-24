FROM circleci/python:3.10.1

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

# Poetry
RUN sudo curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Python 3.7.12
RUN sudo curl -O https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz && \
    sudo tar -xvzf Python-3.7.12.tgz && \
    cd Python-3.7.12 && \
    sudo ./configure --prefix=/usr/ && \
    sudo make && \
    sudo make install && \
    sudo make clean && \
    cd .. && \
    sudo rm -r Python-3.7.12

# Python 3.8.11
RUN sudo curl -O https://www.python.org/ftp/python/3.8.11/Python-3.8.11.tgz && \
    sudo tar -xvzf Python-3.8.11.tgz && \
    cd Python-3.8.11 && \
    sudo ./configure --prefix=/usr/ && \
    sudo make && \
    sudo make install && \
    sudo make clean && \
    cd .. && \
    sudo rm -r Python-3.8.11

# Python 3.9.10
RUN sudo curl -O https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz && \
    sudo tar -xvzf Python-3.9.10.tgz && \
    cd Python-3.9.10 && \
    sudo ./configure --prefix=/usr/ && \
    sudo make && \
    sudo make install && \
    sudo make clean && \
    cd .. && \
    sudo rm -r Python-3.9.10

RUN sudo apt-get install postgresql-client

RUN sudo mkdir /code
RUN sudo chmod 0777 /code
WORKDIR /code
ENV PATH=/code/.venv/bin:${PATH} \
    POETRY_VIRTUALENVS_IN_PROJECT=true
