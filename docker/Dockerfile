FROM python:3.11-bookworm

RUN set -eux; \
    curl -fsSL \
        https://packages.microsoft.com/config/debian/$(. /etc/os-release; echo $VERSION_ID)/packages-microsoft-prod.deb \
        --output packages-microsoft-prod.deb; \
    dpkg -i packages-microsoft-prod.deb; \
    rm packages-microsoft-prod.deb

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        subversion \
        git-svn \
        ruby-dev \
        cmake \
        openjdk-17-jre-headless \
        cppcheck \
        dotnet-sdk-8.0 \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN echo 'gem: --no-document' >> ~/.gemrc

RUN python -m pip install --no-cache-dir poetry==1.7.1

# Node.js LTS
ARG NODE_VERSION=20.12.0
ENV NODE_HOME=/opt/node
RUN set -eux; \
    ARCH= ; \
    case "$(dpkg-architecture --query DEB_BUILD_ARCH_CPU)" in \
        amd64) ARCH='x64';; \
        arm64) ARCH='arm64';; \
        *) exit 1 ;; \
    esac; \
    mkdir -p ${NODE_HOME}; \
    curl -fsSL \
        https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-$ARCH.tar.xz | \
        tar -xJC ${NODE_HOME} --strip-components=1
ENV PATH ${NODE_HOME}/bin:$PATH

ARG SWIFT_VERSION=5.10
ENV SWIFT_HOME=/opt/swift
RUN set -eux; \
    ARCH= ; \
    case "$(dpkg-architecture --query DEB_BUILD_GNU_CPU)" in \
        x86_64) ARCH='';; \
        aarch64) ARCH='-aarch64';; \
        *) exit 1 ;; \
    esac; \
    mkdir -p ${SWIFT_HOME}; \
    curl -fsSL \
        https://download.swift.org/swift-${SWIFT_VERSION}-release/ubuntu2204/swift-${SWIFT_VERSION}-RELEASE/swift-${SWIFT_VERSION}-RELEASE-ubuntu22.04$ARCH.tar.gz | \
        tar -xzC ${NODE_HOME} --strip-components=2
ENV PATH ${SWIFT_HOME}/bin:$PATH

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

ARG SWIFTLINT_VERSION=0.54.0
RUN set -eux; \
    curl -fsSL \
        https://github.com/realm/SwiftLint/releases/download/${SWIFTLINT_VERSION}/swiftlint_linux.zip \
        --output swiftlint.zip \
    ; \
    mkdir swiftlint; \
    unzip swiftlint.zip -d swiftlint; \
    ln -s /dependencies/swiftlint/swiftlint /usr/local/bin/swiftlint; \
    rm swiftlint.zip

# ---------- linters ----------
RUN python -m pip install --no-cache-dir \
        flawfinder \
        pylint

RUN gem install \
        rubocop

# Node.js tools are not installed globally since it's either recommended to install locally,
# or will only work with peer dependencies which are installed locally.
WORKDIR /dependencies/js
RUN npm install \
        jshint \
        eslint \
        typescript \
        typescript-eslint \
        @typescript-eslint/eslint-plugin
ENV ESLINT_HOME /dependencies/js
ENV PATH /dependencies/js/node_modules/.bin:$PATH

RUN dotnet tool install --global \
    roslynator.dotnet.cli
ENV PATH $PATH:/root/.dotnet/tools

WORKDIR /dependencies/roslynator
RUN set -eux; \
    dotnet new console; \
    dotnet add package Roslynator.Analyzers; \
    dotnet add package Roslynator.CodeAnalysis.Analyzers

WORKDIR /dependencies

# PMD: https://pmd.github.io/
ARG PMD_VERSION=7.0.0
RUN set -eux; \
    curl -fsSL \
        https://github.com/pmd/pmd/releases/download/pmd_releases%2F${PMD_VERSION}/pmd-dist-${PMD_VERSION}-bin.zip \
        --output pmd.zip \
    ; \
    unzip pmd.zip; \
    mv pmd-* pmd ; \
    ln -s /dependencies/pmd/bin/pmd /usr/local/bin/pmd; \
    rm pmd.zip

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
COPY main.py readme.md pyproject.toml poetry.lock ./
COPY agent/ agent/

# install agent and python dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run", "cli"]
