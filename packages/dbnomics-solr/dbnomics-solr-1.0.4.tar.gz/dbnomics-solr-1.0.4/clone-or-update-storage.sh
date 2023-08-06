#! /bin/bash

# Clone or update a DBnomics storage directory if it is a Git repository.
#
# If it is a "bare" repository and a series.jsonl file is detected, transform it in a normal repository,
# because series.jsonl purpose is to be used with "fseek", which is not feasible with Git blobs.

set -e

JSON_DATA_BASE_DIR="$1"
PROVIDER_SLUG="$2"

if [ -z "${PROVIDER_SLUG}" -o -z "${JSON_DATA_BASE_DIR}" ]; then
    echo "usage: $0 <json_data_dir> <provider_slug>"
    exit -1
fi

if [ ! -d "${JSON_DATA_BASE_DIR}" ]; then
    echo "${JSON_DATA_BASE_DIR} is not a directory"
    exit -1
fi

JSON_DATA_BASE_DIR=$(realpath "$1")

REPO_DIR="${JSON_DATA_BASE_DIR}/${PROVIDER_SLUG}-json-data"
BARE_REPO_DIR="${REPO_DIR}.git"

# By default prefer a bare repository than a normal one.
if [ ! -d ${REPO_DIR} -a ! -d ${BARE_REPO_DIR} ]; then
    cd $JSON_DATA_BASE_DIR
    git clone --bare --quiet https://git.nomics.world/dbnomics-json-data/${PROVIDER_SLUG}-json-data.git
fi

if [ -d ${REPO_DIR} -a -d ${REPO_DIR}/.git ]; then
    cd $REPO_DIR
    time git pull --quiet
elif [ -d ${BARE_REPO_DIR} ]; then
    cd $BARE_REPO_DIR
    time git fetch origin master:master
fi

if [ -d ${BARE_REPO_DIR} ]; then
    # Detect if repository has at least one JSON lines file. In this case, re-clone it in normal (non-bare) mode.
    cd $BARE_REPO_DIR
    if $(git ls-tree master -r | grep --max-count=1 --quiet series.jsonl); then
        echo "Bare repository with series.jsonl detected: transforming bare repository into normal one..."
        cd $JSON_DATA_BASE_DIR
        git clone ${PROVIDER_SLUG}-json-data.git
        cd ${PROVIDER_SLUG}-json-data.git
        ORIGIN_URL=$(git remote get-url origin)
        cd ../${PROVIDER_SLUG}-json-data
        git remote set-url origin $ORIGIN_URL
        cd ..
        rm -rf ${PROVIDER_SLUG}-json-data.git
        echo "Repository is now normal: ${REPO_DIR}, bare repository (${BARE_REPO_DIR}) is deleted."
    fi
fi
