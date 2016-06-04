#!/usr/bin/env bash
old_PS4=$PS4
export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    # do something
export PS4=${old_PS4}
