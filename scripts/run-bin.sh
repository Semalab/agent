#!/usr/bin/env bash

OS=$1
shift

case $OS in
linux)
  docker build -t agent-linux-runner -f ./docker/linux/Dockerfile.run ./
  docker run --mount type=bind,source=$PWD/dist,target=/dist agent-linux-runner \
    /dist/linux/main "$@"
  ;;

windows)
  docker build -t agent-py-windows-builder -f ./docker-build/Dockerfile.windows ./docker-build
  docker run --mount type=bind,source=$PWD,target=/code agent-py-windows-builder \
    /scripts/wine-do.sh /code/dist/windows/main.exe
  ;;

*)
  echo 'unknown os: "$OS"'
  exit 1
  ;;
esac
