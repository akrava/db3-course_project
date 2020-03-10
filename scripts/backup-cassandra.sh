#!/bin/sh

if [ $# -eq 1 ]; then
    COUNT=$1
    for x in $(seq 1 $1); do
        docker exec "cassandra-n$x" nodetool cleanup db3_course_project
    done
    mkdir "$(dirname "$0")/../backups" 2>/dev/null
    for x in $(seq 1 $1); do
        SNAPSHOT_NAME="db3_course_project_$(date +%s)"
        docker exec "cassandra-n$x" nodetool snapshot -t ${SNAPSHOT_NAME} db3_course_project
        rm -rf "$(dirname "$0")/../backups/cassandra-n$x" 2>/dev/null
        mkdir "$(dirname "$0")/../backups/cassandra-n$x"
        docker cp "cassandra-n$x":"/opt/cassandra/data/data/db3_course_project/" "$(dirname "$0")/../backups/cassandra-n$x"
        find "$(dirname "$0")/../backups/cassandra-n$x/db3_course_project" -mindepth 2 -maxdepth 2 -not -name snapshots -exec rm -rf '{}' \;
    done
else
    echo "No arguments supplied. Need count of cassandra"
    exit 1
fi

