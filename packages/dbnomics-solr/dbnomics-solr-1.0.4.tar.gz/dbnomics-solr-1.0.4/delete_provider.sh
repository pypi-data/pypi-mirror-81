#! /bin/sh

# Delete in Solr all documents having the given provider code.

if [ -z "$1" ]; then
    echo "usage: $0 <provider_code>"
    echo "examples:"
    echo "  $0 WTO"
    echo "  $0 *  # WARNING This deletes the entire index!"
    exit 1
fi

PROVIDER_CODE="$1"
SOLR_POST=${SOLR_POST:-~solr/bin/post}
SOLR_CORE_NAME="${SOLR_CORE_NAME:-dbnomics}"

command -v ${SOLR_POST} > /dev/null 2>&1 || { echo >&2 "Solr ${SOLR_POST} command was not found in PATH. Use 'SOLR_POST' environment variable. Aborting."; exit 1; }

"${SOLR_POST}" -c "${SOLR_CORE_NAME}" -type application/json -d "{delete: {query: \"(type:provider AND id:${PROVIDER_CODE}) OR (type:(dataset OR series) AND provider_code:${PROVIDER_CODE})\"}}"
