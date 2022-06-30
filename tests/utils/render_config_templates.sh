#!/usr/bin/env bash

SRC_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]:-$0}")")
TESTS_DIR="${SRC_DIR}/.."
TEMPLATE_FILES=($(find ${TESTS_DIR} -name '*.template' -type f))

for template in "${TEMPLATE_FILES[@]}"; do
    file=${template%.*}
    content="$(cat "$template")"
    eval "echo \"$content\"" > $file
done
