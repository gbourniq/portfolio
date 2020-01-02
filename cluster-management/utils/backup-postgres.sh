#!/bin/bash

if [ "$1" = "" ] || [ "$2" = "" ]
then
    echo "Usage: $0 <service_name> <database>..."
    echo "Example: $0 yourapp_service_name_postgres dbname"
    exit 1
fi

# set -euxo pipefail

# export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin

service_name=$1
database_name=$2
date=$(date +%Y-%m-%d"_"%H_%M_%S)
backup_filename="${database_name}_${date}.sql"
backup_filename_zipped="${backup_filename}.gz"
s3_location="s3://guillaume.bournique/myportfolio-postgres-backup/"

container_id=$(docker ps | grep $service_name | awk '{print $1}')

# Create pg backup file inside the container"
sudo docker exec $container_id pg_dump -U postgres -f /tmp/$backup_filename $database_name

# copy file inside contaienr to host
sudo docker cp $container_id:/tmp/$backup_filename .

# remove file in container
sudo docker exec $container_id rm /tmp/$backup_filename

# compress
sudo gzip $backup_filename

# upload to s3
sudo aws s3 cp $backup_filename_zipped $s3_location

sudo rm $backup_filename_zipped