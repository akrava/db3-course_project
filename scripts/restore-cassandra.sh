#!/bin/sh


if [ $# -eq 2 ]; then
    COUNT=$1
    FOLDER_PATH=$2
    for x in $(seq 1 $1); do
        docker cp "$(dirname "$0")/../backups/cassandra-n$x/" "cassandra-n$x":"/var/lib/cassandra/data/data/"
        for dir in $(find "$(dirname "$0")/../backups/cassandra-n$x/db3_course_project/" -mindepth 1 -maxdepth 1 -type d); do
            dir=${dir%*/}
            dir=${dir##*/}
            docker exec "cassandra-n$x" cqlsh -e "CREATE KEYSPACE IF NOT EXISTS db3_course_project WITH replication = {'class': 'SimpleStrategy', 'replication_factor':2};"
            docker exec "cassandra-n$x" cp -rf "/var/lib/cassandra/data/data/db3_course_project/${dir}/snapshots/${FOLDER_PATH}/."  "/var/lib/cassandra/data/data/db3_course_project/${dir}/"
            docker exec "cassandra-n$x" chown -R cassandra:cassandra /var/lib/cassandra/data/
            docker exec "cassandra-n$x" cqlsh -f "/var/lib/cassandra/data/data/db3_course_project/${dir}/schema.cql"
            table_name=${dir::-33}
            docker exec "cassandra-n$x" cqlsh -e "truncate db3_course_project.${table_name};"
            docker exec "cassandra-n$x" nodetool refresh db3_course_project ${table_name}
            docker exec "cassandra-n$x" sstableloader -d 127.0.0.1 "/var/lib/cassandra/data/data/db3_course_project/${dir}"
        done
    done
else
    echo "No arguments supplied. Need count of cassandra and name of snapshot"
    exit 1
fi
