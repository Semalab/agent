FROM buildpack-deps:bookworm as build-cppcheck

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        libpcre3-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

ARG CPPCHECK_VERSION=2.7
WORKDIR /root/cppcheck
RUN set -eux; \
    curl -fsSL \
        https://github.com/danmar/cppcheck/archive/refs/tags/${CPPCHECK_VERSION}.tar.gz \
        --output cppcheck.tar.gz \
    ; \
    tar -xf cppcheck.tar.gz --strip-components=1; \
    rm cppcheck.tar.gz; \
    mkdir -p /opt/cppcheck; \
    make \
        FILESDIR=/dependencies/cppcheck \
        DESTDIR=/opt/cppcheck/ \
        PREFIX="" \
        MATCHCOMPILER=yes \
        HAVE_RULES=yes \
        CXXFLAGS="-O2 -DNDEBUG" \
        install


# Build OpenSSL 1.1 for .NET Core 3.1 -- remove when upgrading .NET
FROM buildpack-deps:bookworm as build-openssl

WORKDIR /root/openssl
RUN set -eux; \
    curl -fsSL https://github.com/openssl/openssl/releases/download/OpenSSL_1_1_1w/openssl-1.1.1w.tar.gz \
        --output openssl.tar.gz \
    ; \
    tar -xf openssl.tar.gz --strip-components=1; \
    rm openssl.tar.gz; \
    ./config --prefix=/opt/openssl --openssldir=/usr/lib/ssl shared zlib; \
    make install_sw


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
        libpcre3 \
        # dotnet-sdk-8.0 \
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

# ---------- linters ----------

COPY --from=build-cppcheck /opt/cppcheck/bin/ /dependencies/cppcheck/
COPY --from=build-cppcheck /opt/cppcheck/dependencies/cppcheck/ /dependencies/cppcheck/
ENV PATH /dependencies/cppcheck:$PATH

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

RUN python -m pip install --no-cache-dir \
        flawfinder==2.0.19 \
        pylint==2.15.7

RUN gem install \
        rubocop:0.67.2

# Node.js tools are not installed globally since it's either recommended to install locally,
# or will only work with peer dependencies which are installed locally.
WORKDIR /dependencies/js
RUN npm install \
        eslint@6.7.2 \
        jshint@2.11.0-rc1 \
        tslint@5.20.1 \
        typescript@3.7.3
        # Required for newer versions of eslint with support for TS linting via plugins
        # typescript-eslint \
        # @typescript-eslint/eslint-plugin
ENV JSTOOLS_HOME /dependencies/js
ENV PATH /dependencies/js/node_modules/.bin:$PATH
COPY lib/js/ .

# .NET Core 3.1 is required for the version of Roslynator we are using
# Remove this install script and use the apt install command on upgrade
WORKDIR /dependencies
COPY --from=build-openssl /opt/openssl/ /opt/openssl/
ENV LD_LIBRARY_PATH /opt/openssl/lib:$LD_LIBRARY_PATH
RUN set -eux; \
    curl -fsSL https://dotnet.microsoft.com/download/dotnet/scripts/v1/dotnet-install.sh \
        --output dotnet-install.sh \
    ; \
    chmod +x dotnet-install.sh; \
    ./dotnet-install.sh --version 3.1.426
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT 1
ENV DOTNET_ROOT /root/.dotnet
ENV PATH $PATH:/root/.dotnet:/root/.dotnet/tools
RUN dotnet tool install --global Roslynator.DotNet.Cli --version 0.1.0

# Required for newer versions of Roslynator
# WORKDIR /dependencies/roslynator
# RUN set -eux; \
#     dotnet new console; \
#     dotnet add package Roslynator.Analyzers; \
#     dotnet add package Roslynator.CodeAnalysis.Analyzers

WORKDIR /dependencies

# PMD: https://pmd.github.io/
ARG PMD_VERSION=6.50.0
RUN set -eux; \
    curl -fsSL \
        https://github.com/pmd/pmd/releases/download/pmd_releases%2F${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip \
        --output pmd.zip \
    ; \
    unzip pmd.zip; \
    mv pmd-* pmd; \
    ln -s /dependencies/pmd/bin/run.sh /usr/local/bin/run-pmd; \
    rm pmd.zip

COPY cache/ cache/
# Tailor for Swift linting
RUN set -eux; \
    curl -fsSL \
        https://github.com/sleekbyte/tailor/releases/download/v0.12.0/tailor-0.12.0.zip \
        --output tailor.zip \
    ; \
    unzip tailor.zip; \
    mv tailor-* tailor; \
    ln -s /dependencies/tailor/bin/tailor /usr/local/bin/tailor; \
    rm tailor.zip

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
