#!/usr/bin/env bash

HOST="192.168.88.18"
SRC="/root/.acme.sh"
DEST="/root/.acme.sh"
USER="root"
SSH_OPTION="-p 22 -oStrictHostKeyChecking=no"
RSYNC_LOG_FILE="/tmp/rsync.log"

/usr/bin/rsync -azurR \
    -e "ssh ${SSH_OPTION}" \
    --delete --delete-excluded \
    --log-file=${RSYNC_LOG_FILE} \
    ${USER}@${HOST}:${SRC} "${DEST}"
