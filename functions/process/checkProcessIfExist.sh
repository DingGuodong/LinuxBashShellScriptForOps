#!/usr/bin/env bash
PIDFILE=""
if ! kill -0 $(cat ${PIDFILE}) >/dev/null 2>&1; then
    echo xxx
fi

