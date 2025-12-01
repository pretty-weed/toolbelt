#!/usr/bin/env bash
set -x
SOURCE="${1}"
DEST="${2}"
# I am of two minds on whether to exclude .git
#  --exclude='.git' 
rsync -avz "${SOURCE}/" "${DEST}" > "${DEST}/preload.log"
