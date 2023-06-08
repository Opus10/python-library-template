FROM mambaorg/micromamba:1.4.3 AS builder

ENV PYTHONDONTWRITEBYTECODE=1

RUN micromamba create -n essential postgresql git make curl -c conda-forge -y &&\
    micromamba create -n py37 python==3.7.* -c conda-forge -y &&\
    micromamba create -n py38 python==3.8.* -c conda-forge -y &&\
    micromamba create -n py39 python==3.9.* -c conda-forge -y &&\
    micromamba create -n py310 python==3.10.* -c conda-forge -y &&\
    micromamba create -n py311 python==3.11.* -c conda-forge -y

FROM cimg/base:2023.06

RUN sudo mkdir /opt/circleci && sudo chown circleci /opt/circleci && sudo chgrp circleci /opt/circleci && \
    sudo mkdir /code && sudo chown circleci /code && sudo chgrp circleci /code

COPY --from=builder --chown=circleci:circleci /opt/conda/envs /opt/conda/envs

ENV PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=/opt/circleci/.poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH=/code/.venv/bin:/opt/conda/envs/py311/bin:/opt/conda/envs/py310/bin:/opt/conda/envs/py39/bin:/opt/conda/envs/py38/bin:/opt/conda/envs/py37/bin:/opt/conda/envs/essential/bin:/opt/circleci/.poetry/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | /opt/conda/envs/py311/bin/python -

WORKDIR /code
