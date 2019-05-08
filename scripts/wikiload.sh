#!/bin/bash
# Script requires: httpie (https://httpie.org/) and jq
# (https://stedolan.github.io/jq/)
set -e -o xtrace
index_url="http://localhost:9200/data"
wiki_dump="enwikiquote-20190422-cirrussearch-content"

# Delete index
http DELETE $index_url

# Create the index and mappings.
http PUT $index_url < index.json

# Delete the old dump, download the new and gunzip.
rm -f ${wiki_dump}.json.gz
wget https://dumps.wikimedia.org/other/cirrussearch/20190422/${wiki_dump}.json.gz

gunzip ${wiki_dump}.json.gz

# delete the chunks dir
rm -rf chunks

# Remove something ES whines about
jq -c '. |= del(.defaultsort)' enwikiquote-20190422-cirrussearch-content.json > fixed.json

# Split into chunks
mkdir -p chunks
cd chunks
split -a 10 -l 500 ../fixed.json

# Load all chunks
for file in *; do
    http POST $index_url/_bulk < $file
done
cd ..
rm fixed.json
rm ${wiki_dump}.json
