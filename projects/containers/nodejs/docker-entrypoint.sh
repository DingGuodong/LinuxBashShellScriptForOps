#!/usr/bin/env bash
# Usage: bash $0
# Author: dgden
# Create Date: 2020/12/29
# Create Time: 11:30
# Description:
#!/bin/sh
set -e

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- node "$@"
fi

exec "$@"
