FROM python:3.11-buster

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl unzip subversion git-svn


# ---------- oss dependencies ----------
WORKDIR /dependencies

# dependency_check: https://github.com/jeremylong/DependencyCheck
ARG DEPENDENCY_CHECK_VERSION=8.2.1

RUN apt-get -y install openjdk-11-jre-headless

RUN curl -L \
    https://github.com/jeremylong/DependencyCheck/releases/download/v${DEPENDENCY_CHECK_VERSION}/dependency-check-${DEPENDENCY_CHECK_VERSION}-release.zip \
    --output dependency-check.zip \
    && unzip dependency-check.zip \
    && echo '#!/bin/bash\n\
      cd /dependencies/dependency-check/bin/\n\
      ./dependency-check.sh "$@"\n\
    ' > /usr/local/bin/dependency-check \
    && chmod +x /usr/local/bin/dependency-check

# scancode: https://github.com/nexB/scancode-toolkit
ARG SCANCODE_VERSION=31.2.6

RUN pip install scancode-toolkit==${SCANCODE_VERSION}

# ---------- linters ----------
RUN apt-get -y install cppcheck

WORKDIR /src

RUN pip install poetry==1.4.2
COPY main.py readme.md pyproject.toml poetry.lock ./
COPY agent/ agent/

# install agent and python dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run", "cli"]
