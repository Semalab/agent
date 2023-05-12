#!/bin/bash
set -e

cd /code
ls

case "$1" in
windows)
  echo 'building for windows'
  ;;

linux)
  echo 'building for linux'
  ;;

*)
  echo "unknown system $1"
  exit
  ;;
esac
