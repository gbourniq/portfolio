#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ]
then
    echo "Usage: $0 <service_name> <database>..."
    echo "Example: $0 yourapp_service_name_postgres dbname"
    exit 1
fi

# set -euxo pipefail

# export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin

# Retrieve arguments
service_name=$1
database_name=$2
s3_location_base=$3

# Define backup file names
postgres_backup="${database_name}.sql"
postgres_backup_dated_zipped="${database_name}_$(date +%Y-%m-%d"_"%H_%M_%S).sql.gz"
postgres_backup_latest_zipped="${database_name}_latest.sql.gz"

# Define S3 locations
s3_postgres_latest=${s3_location_base}/latest/
s3_postgres_all=${s3_location_base}/all/

# Get Postgres container id
container_id=$(docker ps | grep $service_name | awk '{print $1}')

# Create pg backup file inside the container"
docker exec ${container_id} pg_dump -U postgres -f /tmp/${postgres_backup} ${database_name}

# copy file inside container to host
docker cp ${container_id}:/tmp/${postgres_backup} .

# remove file in container
docker exec ${container_id} rm /tmp/${postgres_backup}

# compress
gzip ${postgres_backup}

# create two copies of backup on host
cp ${postgres_backup}.gz ${postgres_backup_latest_zipped}
cp ${postgres_backup}.gz ${postgres_backup_dated_zipped}

# upload copies to s3
aws s3 cp ${postgres_backup_latest_zipped} ${s3_postgres_latest}
aws s3 cp ${postgres_backup_dated_zipped} ${s3_postgres_all}

# cleanup
rm ${postgres_backup}.gz
rm ${postgres_backup_latest_zipped}
rm ${postgres_backup_dated_zipped}
