#!/usr/bin/env bash
# Check if a command already exists
function command_exists() {
    # which "$@" >/dev/null 2>&1
    command -v "$@" >/dev/null 2>&1
}
