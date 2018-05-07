#!/usr/bin/env bash

function create() {
    curl -XPUT -H 'Content-Type: application/json' 'http://localhost:9200/flightdb/' -d '{
        "settings" : {
            "index" : {
                "number_of_shards" : 1,
                "number_of_replicas" : 1
            }
        }
    }'
}

function delete() {
    curl -XDELETE 'http://localhost:9200/flightdb/'
}

function detail() {
    curl 'http://localhost:9200/flightdb/'
}

function verify() {
    curl 'http://localhost:9200/_cat/indices?v'
}


case $1 in
create)
    create
    ;;
detail)
    detail
    ;;
verify)
    verify
    ;;
delete)
    delete
    ;;
*)
    echo "$0 create|delete|detail|verify"
    ;;
esac

echo