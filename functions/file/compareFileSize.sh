#!/usr/bin/env bash
FILES=
test "$(stat -c "%s" ${FILES})" = "0"