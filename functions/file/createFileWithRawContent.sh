#!/usr/bin/env bash
# this is an example use for create a file with keep special character themselves
# we called RAW contents, using this method to skip expand variable
cat >/path/to/filename <<'eof'
$
eof
