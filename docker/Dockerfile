FROM python:3.11-bookworm

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        curl \
        unzip \
        subversion \
        git-svn \
        ruby-dev \
        cmake \
        openjdk-17-jre-headless \
        cppcheck \
    ; \
    rm -rf /var/lib/apt/lists/*

# ---------- oss dependencies ----------
WORKDIR /dependencies

# scancode: https://github.com/nexB/scancode-toolkit
ARG SCANCODE_VERSION=32.0.8
RUN set -eux; \
    curl -fsSL \
        https://github.com/nexB/scancode-toolkit/releases/download/v${SCANCODE_VERSION}/scancode-toolkit-v${SCANCODE_VERSION}_py3.11-linux.tar.gz \
        --output scancode.tar.gz \
    ; \
    mkdir scancode; \
    tar -xf scancode.tar.gz -C scancode --strip-components=1; \
    ln -s /dependencies/scancode/scancode /usr/local/bin/scancode; \
    rm scancode.tar.gz; \
    cd scancode; \
    ./configure

# linguist: https://github.com/github-linguist/linguist
ARG LINGUIST_VERSION=7.28
RUN set -eux; \
    gem install github-linguist:${LINGUIST_VERSION}; \
    # Remove MAX_TREE_SIZE check from linguist - https://github.com/github-linguist/linguist/issues/6550
    find /var/lib/gems -path '*/lib/linguist/repository.rb' \
        -exec sed -ie 's/return {*} if current_tree.count_recursive(MAX_TREE_SIZE) >= MAX_TREE_SIZE/#/g' {} ';' \
        # print and grep just to make sure that some files were found - otherwise, find happily returns 0
        -print | grep -q .

# ---------- linters ----------
RUN python -m pip install --no-cache-dir flawfinder

COPY cache/ cache/

# dependency_check: https://github.com/jeremylong/DependencyCheck
ARG DEPENDENCY_CHECK_VERSION=9.0.7
RUN set -eux; \
    curl -fsSL \
        https://github.com/jeremylong/DependencyCheck/releases/download/v${DEPENDENCY_CHECK_VERSION}/dependency-check-${DEPENDENCY_CHECK_VERSION}-release.zip \
        --output dependency-check.zip \
    ; \
    unzip dependency-check.zip; \
    printf '%s\n%s\n%s' \
        '#!/bin/bash' \
        'cd /dependencies/dependency-check/bin/' \
        './dependency-check.sh "$@"' \
        > /usr/local/bin/dependency-check \
    ; \
    chmod +x /usr/local/bin/dependency-check; \
    rm dependency-check.zip; \
    (if [ -d cache/dependency-check ]; then cp -r cache/dependency-check/ dependency-check/data/; fi); \
    dependency-check --updateonly

# backend services
COPY out/backend-*/*-jar-with-dependencies.jar /dependencies/

WORKDIR /src

RUN python -m pip install --no-cache-dir poetry==1.7.1
COPY main.py readme.md pyproject.toml poetry.lock ./
COPY agent/ agent/

# install agent and python dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run", "cli"]
