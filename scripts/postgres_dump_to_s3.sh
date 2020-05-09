#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ] || [ "$3" = "" ]; then
    echo "Usage: $0 <service_name> <database> <s3_location>"
    echo "Example: $0 yourapp_service_name_postgres dbname s3://<bucket-name>/postgres_backup/"
    exit 1
fi

# Retrieve arguments
service_name=$1
database_name=$2
s3_postgres_base_location=$3
db_user=postgres

# Define backup file names
postgres_backup="${database_name}.tar"
postgres_backup_dated="${database_name}_$(date +%Y-%m-%d"_"%H_%M_%S).tar"
postgres_backup_latest="${database_name}_latest.tar"

# Define S3 locations
s3_postgres_latest=${s3_postgres_base_location}/latest/
s3_postgres_all=${s3_postgres_base_location}/all/

# Get Postgres container id
container_id=$(docker ps | grep $service_name | awk '{print $1}')

if [[ -z $container_id ]]; then
    echo "No container found with the name $service_name. Aborting database back up script."
    exit 1
fi

echo "Create pg backup file inside the container"
docker exec ${container_id} /bin/sh -c "pg_dump -U ${db_user} -F t ${database_name} > /tmp/${postgres_backup}"

echo "Copy file from inside the container to host"
docker cp ${container_id}:/tmp/${postgres_backup} .

# create two copies of backup on host
cp ${postgres_backup} ${postgres_backup_latest}
cp ${postgres_backup} ${postgres_backup_dated}

echo "Upload postgres dump to s3"
aws s3 cp ${postgres_backup_latest} ${s3_postgres_latest}
aws s3 cp ${postgres_backup_dated} ${s3_postgres_all}

# cleanup
rm ${postgres_backup}
rm ${postgres_backup_latest}
rm ${postgres_backup_dated}
docker exec ${container_id} rm /tmp/${postgres_backup}