#!/bin/bash

cd "$(dirname "$0")"

echo Backing up influxdb...

if [ ! -d backup ]; then
    echo Creating backup folder
    mkdir backup
fi

if [ "$(ls -A backup)" ];then
    echo "Removing contents in backup folder"
    rm -rf backup/*
fi

influxd backup -database bocrate ./backup

DATE=$(date +%Y-%m-%d_%H%M%S)

echo comparess backup data...

tar cvfj backup-$DATE.tar.bz2

echo "Finished backup influxdb database to file backup-$DATE.tar.bz2"
