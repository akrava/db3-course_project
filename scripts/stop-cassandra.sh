#!/bin/sh

if [ $# -eq 1 ]; then
     docker stop "cassandra-n$1"
else
    echo "No arguments supplied. Need number of cassandra"
    exit 1
fi
