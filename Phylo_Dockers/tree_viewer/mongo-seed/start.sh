#!/bin/sh

backups="/backups"
PREFIX="mongodb"
HOST="mongodb"
DBNAME="EOL_data"

echo "Importing seed data into MongoDB" 

sleep 10

mongorestore --host mongodb --db ${DBNAME} --drop /seed/

#set the INTERVAL value to change the periodicity of backup
INTERVAL=604800 #1 week = 604800 seconds, 1 day = 86400 seconds, 

sleep 20

echo "Backup Directory: "$backups
echo "Backups: host=${HOST} prefix=${PREFIX}, interval=${INTERVAL}"

while true; do
  ts=$(date -Iseconds)
  archive="${backups}/${PREFIX}-${ts}"

  if mongodump --host=${HOST} --db=${DBNAME} --out "${archive}" "$@"; then
    if [ -d ${archive} ]; then
      tar -C ${archive} -c -f ${archive}.tgz . && rm -rf ${archive}
      echo "Created backup: ${archive}.tgz"
    else
      echo "ERROR: failed to create backup $archive"
    fi
  else
    echo "ERROR ($?) : failed to create backup"
  fi
 
  if [ ${INTERVAL} -gt 0 ]; then
    sleep ${INTERVAL}
  else
    break
  fi
done
