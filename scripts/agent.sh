#!/usr/bin/env bash

set -e

print-usage() {
  printf '%s\n' 'Usage: agent.sh <repository> <output-directory>'
  printf '\n'
  printf '%s\n' 'Runs a Sema scan on the provided <repository>, and outputs a .zip file in '
  printf '%s\n' '<output-directory>. This .zip file must be sent to Sema for further analysis.'
  printf '\n'
  printf '%s\n' 'Options:'
  printf '%s\n' '  -h, --help        Print this message.'
}

check-usage() {
  if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    print-usage

    exit
  fi

  if [ "$#" != 2 ]; then
    printf '%s\n\n' "Expected 2 arguments but got $#."
    print-usage

    exit 1
  fi

  # check that arguments are valid directories
  for DIR in "$REPO" "$OUT"; do
    if [ ! -d "$DIR" ]; then
      printf '%s\n\n' "'$DIR' is not a directory."
      print-usage

      exit 1
    fi
  done
}

main() {
  REPO="$1"
  OUT="$2"

  check-usage "$@"

  docker build -t sema-agent -f ./docker/Dockerfile ./

  docker run \
    --mount type=bind,source="$(realpath $REPO)",target=/repo,readonly \
    --mount type=bind,source="$(realpath $OUT)",target=/out \
    sema-agent --repository /repo --output /out
}

main "$@"
