#!/bin/bash

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo -e "You must be root"
    exit 1
fi

function usage() {
    exit 1;
}

# see more about "args", long args(--option)?
while getopts ":d:b:" opts; do
    case "${opts}" in
        d)
            BACKUPPED_DIR_ROOT=${OPTARG}
        ;;
        b)
            BACKUP_DAEMON=${OPTARG}
        ;;
        *)
            echo "see $0 usage"
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${BACKUPPED_DIR_ROOT}" ] || [ -z "${BACKUP_DAEMON}" ]; then
    echo "see $0 usage"
else
    echo "opts are $BACKUPPED_DIR_ROOT, $BACKUP_DAEMON"
fi

