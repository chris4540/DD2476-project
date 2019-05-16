export es=localhost:9200
export site=sv.wikipedia.org
export index=svwiki
export dump=svwiki-20190429-cirrussearch-content.json.gz 

echo "Deleting index if it exists"
curl -XDELETE $es/$index?pretty

echo "Injecting settings into ElasticSearch"
cat svwiki_settings.json | curl -H 'Content-Type: application/json' -XPUT $es/$index?pretty -d -@

echo "Injecting mappings into ElasticSearch"
cat svwiki_mappings.json | curl -H 'Content-Type: application/json' -XPUT $es/$index/_mapping/page?pretty -d -@

curl -XPUT -H 'Content-Type: application/json' "$es/$index/_settings?pretty" -d '{
    "index" : {
        "refresh_interval" : -1
    }
}'

echo "Downloading swedish wikipedia dump"

wget https://ftp.acc.umu.se/mirror/wikimedia.org/other/cirrussearch/20190429/$dump

echo "Extracting wikipedia dump"
mkdir chunks
cd chunks
zcat ../$dump | split -a 10 -l 500 - $index

echo "Indexing..."
for file in *; do
  echo -n "${file}:  "
  took=$(curl -s -H 'Content-Type: application/x-ndjson' -XPOST $es/$index/_bulk?pretty --data-binary @$file |
    grep took | cut -d':' -f 2 | cut -d',' -f 1)
  printf '%7s\n' $took
  [ "x$took" = "x" ] || rm $file
done
