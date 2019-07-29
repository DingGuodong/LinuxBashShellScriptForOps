#!/bin/bash
set -e

branch=""
tag=""

while getopts 'b:h:t:' opt; do
    case ${opt}$OPTARG in
        b*)
            branch="$OPTARG"
            ;;
        t*)
            tag="$OPTARG"
            ;;
        h|?|*)
            echo "$0 -b <branch name> -t <tag name> <parameter>..."
            echo "$0 -b <branch name> <parameter>..."
            echo "$0 -t <tag name> <parameter>..."
            exit 1
            ;;
    esac
done
shift "$((OPTIND - 1))"

echo "position parameter is $*."
echo "branch is $branch."
echo "tag is $tag."