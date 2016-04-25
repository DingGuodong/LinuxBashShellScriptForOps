#!/usr/bin/env bash
# Print the commands being run so that we can see the command that triggers
# an error.  It is also useful for following along as the install occurs.
# same as set -u
# Save trace setting
_XTRACE_FUNCTIONS=$(set +o | grep xtrace)
set -o xtrace
