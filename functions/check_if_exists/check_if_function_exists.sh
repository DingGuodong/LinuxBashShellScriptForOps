#!/usr/bin/env bash
# Check if a function already exists
function function_exists {
    declare -f -F $1 > /dev/null
}
