#!/bin/sh

if [ $# -eq 1 ] && [ $1 = "1" ]; then
    docker volume create db-vol
    docker network create -d bridge cassandra-network
    docker run --name cassandra-n1 -v db-vol:/var/lib/cassandra-n1 --network cassandra-network -p 9042:9042 -p 9160:9160 -p 7199:7199 -p 7000:7000 -p 7001:7001 --env HEAP_NEWSIZE=128M --env MAX_HEAP_SIZE=256M -d cassandra:latest
elif [ $# -eq 1 ]; then
    docker run --name "cassandra-n$(($1))" -v db-vol:"/var/lib/cassandra-n$(($1))"  -d --network cassandra-network -p "9$(($1))42:9042" -p "9$(($1+1))60:9160" -p "7$(($1+1))99:7199" -p "7$(($1))00:7000" -p "7$(($1))01:7001" -e CASSANDRA_SEEDS=cassandra-n1 --env HEAP_NEWSIZE=128M --env MAX_HEAP_SIZE=256M cassandra:latest
else
    echo "No arguments supplied. Need number of cassandra"
    exit 1
fi
