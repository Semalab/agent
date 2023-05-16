#!/bin/sh
# Run a command under wine and wait for it to terminate
set -e

wine "$@"
wineserver -w
