#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ]
then
    echo "Usage: $0 <service_name> <database> <s3_location>"
    echo "Example: $0 yourapp_service_name_postgres dbname s3://<bucket-name>/postgres_backup/"
    exit 1
fi

# Retrieve arguments
service_name=$1
database_name=$2
s3_location_base=$3
db_user=postgres

# Define S3 location to download latest postgres dump
postgres_backup="${database_name}_latest.tar"
s3_path_postgres_dump_latest=${s3_location_base}/latest/${postgres_backup}

# Get Postgres container id
container_id=$(docker ps | grep $service_name | awk '{print $1}')
if [[ -z $container_id ]]; then
    echo "No container found with the name $service_name. Aborting database restore script."
    exit 1
fi

echo "Download postgres dump from S3 to host"
aws s3 cp ${s3_path_postgres_dump_latest} .

echo "Copy postgres dump to container"
docker cp ${postgres_backup} ${container_id}:/tmp/

echo "Restore postgres data using dump"
docker exec ${container_id} /bin/sh -c "pg_restore -d ${database_name} /tmp/${postgres_backup} -c -U ${db_user}"

# cleanup
rm ${postgres_backup}
docker exec ${container_id} rm /tmp/${postgres_backup}
