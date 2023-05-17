#!/usr/bin/env bash

OS=$1
shift

case $OS in
linux)
  docker build -t agent-linux-runner -f ./docker/linux/Dockerfile.run ./
  docker run \
    --mount type=bind,source=$PWD/dist,target=/dist \
    --mount type=bind,source=$PWD,target=/src \
    agent-linux-runner \
    /dist/linux/main "$@"
  ;;

windows)
  docker build -t agent-windows-base -f ./docker/windows/Dockerfile.base ./
  docker build -t agent-windows-runner -f ./docker/windows/Dockerfile.run ./
  docker run --mount type=bind,source=$PWD/dist,target=/dist agent-windows-runner \
    /scripts/wine-do.sh /dist/windows/main.exe "$@"
  ;;

*)
  echo 'unknown os: "$OS"'
  exit 1
  ;;
esac
