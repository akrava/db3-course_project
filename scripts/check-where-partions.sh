#!/bin/sh

if [ $# -eq 1 ]; then
    docker exec cassandra-n1 nodetool getendpoints db3_course_project vehicle_position $1
else
    echo "No arguments supplied. Need number of cassandra"
    exit 1
fi
