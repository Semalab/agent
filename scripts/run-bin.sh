#!/usr/bin/env bash

OS=$1
SRC=$2
shift
shift

case $OS in
linux)
  docker build -t agent-linux-runner -f ./docker/linux/Dockerfile.run ./
  docker run \
    --mount type=bind,source="$PWD"/dist,target=/dist,readonly \
    --mount type=bind,source="$PWD"/out,target=/out \
    --mount type=bind,source="$PWD/$SRC",target=/src,readonly \
    agent-linux-runner \
    /dist/linux/main /src --output /out/test.zip "$@"
  ;;

windows)
  docker build -t agent-windows-base -f ./docker/windows/Dockerfile.base ./
  docker build -t agent-windows-runner -f ./docker/windows/Dockerfile.run ./
  docker run \
    --mount type=bind,source="$PWD"/dist,target=/dist \
    --mount type=bind,source="$PWD"/out,target=/out,readonly \
    --mount type=bind,source="$PWD",target=/src \
    agent-windows-runner \
    /scripts/wine-do.sh /dist/windows/main.exe "$@"
  ;;

*)
  echo "unknown os: '$OS'"
  exit 1
  ;;
esac
