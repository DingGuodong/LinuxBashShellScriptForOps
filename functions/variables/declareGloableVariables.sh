#!/usr/bin/env bash
# ensure we don't re-source this in the same environment
[[ -z "$_FUNCTIONS_COMMON" ]] || return 0
declare -r _FUNCTIONS_COMMON=1

# Global Config Variables
declare -A VAR1
declare -A VAR2
declare -A VAR3
