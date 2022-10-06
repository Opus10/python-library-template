FROM cimg/base:2022.08

RUN sudo mkdir /opt/circleci && sudo chown circleci /opt/circleci && sudo chgrp circleci /opt/circleci && \
    sudo mkdir /code && sudo chown circleci /code && sudo chgrp circleci /code

ENV PYENV_ROOT=/opt/circleci/.pyenv \
    POETRY_HOME=/opt/circleci/.poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH=/code/.venv/bin:/opt/circleci/.pyenv/shims:/opt/circleci/.pyenv/bin:/opt/circleci/.poetry/bin:$PATH

RUN sudo apt-get update && sudo apt-get install -y \
        build-essential \
        ca-certificates \
        curl \
        git \
        libbz2-dev \
        liblzma-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxmlsec1-dev \
        llvm \
        make \
        python-openssl \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev && \
    curl https://pyenv.run | bash && \
    sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN env PYTHON_CONFIGURE_OPTS="--enable-shared --enable-optimizations" \
    pyenv install -v 3.7.13 && \
    pyenv install -v 3.8.13 && \
    pyenv install -v 3.9.13 && \
    pyenv install -v 3.10.6 && \
    pyenv global system 3.10.6 3.9.13 3.8.13 3.7.13

RUN curl -sSL https://install.python-poetry.org | python -  

RUN sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt focal-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - && \
    sudo apt -y update && \
    sudo apt-get install -y postgresql-client-14 && \
    sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /code
