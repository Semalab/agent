#!/usr/bin/env bash

set -euo pipefail

REPO=
OUT=
TAG=latest

print-usage() {
  if [ "$#" != 0 ]; then
    printf '%s\n\n' "$@" >&2
  fi
  printf '%s\n' 'Usage: agent.sh <repository> <output-directory>' >&2
  printf '\n' >&2
  printf '%s\n' 'Runs a Sema scan on the provided <repository>, and outputs a .zip file in ' >&2
  printf '%s\n' '<output-directory>. This .zip file must be sent to Sema for further analysis.' >&2
  printf '\n' >&2
  printf '%s\n' 'Options:' >&2
  printf '%s\n' '  -h, --help        Print this message.' >&2
  printf '%s\n' '  -t, --tag <tag>   Use the specified Docker image tag. Defaults to "latest".' >&2
}

check-usage() {
  if [ "$#" -lt 2 ]; then
    print-usage "Expected at least 2 arguments but got $#."
    exit 1
  fi
  
  while :; do
    case $1 in
      -h|-\?|--help)
        print-usage
        exit
        ;;
      -t|--tag)
        if [ "$2" ]; then
          TAG=$2
          shift
        else
          print-usage 'ERROR: "--tag" requires a non-empty option argument.'
          exit 1
        fi
        ;;
      --)
        shift
        break
        ;;
      -?*)
        printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
        ;;
      *)
        break
    esac

    shift
  done

  REPO=$1
  OUT=$2

  # check that arguments are valid directories
  for DIR in "$REPO" "$OUT"; do
    if [ ! -d "$DIR" ]; then
      print-usage "'$DIR' is not a directory."
      exit 1
    fi
  done
}

abspath() {
  cd "$1"
  pwd -P
}

main() {
  check-usage "$@"

  docker pull ghcr.io/semalab/agent:$TAG

  docker run \
    --mount type=bind,source="$(abspath $REPO)",target=/repo,readonly \
    --mount type=bind,source="$(abspath $OUT)",target=/out \
    ghcr.io/semalab/agent:$TAG --repository /repo --output /out
}

main "$@"
