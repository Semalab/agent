FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        unzip \
        subversion \
        git-svn \
        ruby-dev \
        cmake \
        openjdk-17-jre-headless \
        cppcheck \
    && rm -rf /var/lib/apt/lists/*

# ---------- oss dependencies ----------
WORKDIR /dependencies

# dependency_check: https://github.com/jeremylong/DependencyCheck
ARG DEPENDENCY_CHECK_VERSION=9.0.7
RUN curl -Ls \
        https://github.com/jeremylong/DependencyCheck/releases/download/v${DEPENDENCY_CHECK_VERSION}/dependency-check-${DEPENDENCY_CHECK_VERSION}-release.zip \
        --output dependency-check.zip \
    && unzip dependency-check.zip \
    && echo -e '#!/bin/bash\n\
      cd /dependencies/dependency-check/bin/\n\
      ./dependency-check.sh "$@"\n\
    ' > /usr/local/bin/dependency-check \
    && chmod +x /usr/local/bin/dependency-check

# scancode: https://github.com/nexB/scancode-toolkit
ARG SCANCODE_VERSION=31.2.6
RUN pip install scancode-toolkit==${SCANCODE_VERSION}

# linguist: https://github.com/github-linguist/linguist
ARG LINGUIST_VERSION=7.28
RUN gem install github-linguist:${LINGUIST_VERSION}

# ---------- linters ----------
RUN pip install flawfinder

WORKDIR /src

RUN pip install poetry==1.4.2
COPY main.py readme.md pyproject.toml poetry.lock ./
COPY agent/ agent/

# install agent and python dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run", "cli"]
