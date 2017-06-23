#!/usr/bin/env bash

# Validate a text if is json format using jsonlint(bin from package 'python-demjson')
# Example cat a json file pipe to jsonlint
curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5' | jsonlint

# jq is like sed for JSON data - you can use it to slice and filter and map and transform structured data with the same ease that sed, awk, grep and friends let you play with text.
curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5' | jq '.'