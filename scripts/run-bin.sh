#!/usr/bin/env bash

set -e

REPO=$(realpath "$1")
OUT=$(realpath "$2")
shift
shift

docker build -t sema-agent -f ./docker/Dockerfile ./

docker run \
  --mount type=bind,source="$REPO",target=/repo,readonly \
  --mount type=bind,source="$OUT",target=/out \
  sema-agent --repository /repo --output /out "$@"
