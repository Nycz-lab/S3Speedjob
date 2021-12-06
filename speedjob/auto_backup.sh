#!/bin/bash

CURRENT_DATE=`date +"%Y_%m_%d"`
/usr/bin/sqlite3 /home/pi/S3Speedjob/speedjob/db.sqlite3 ".backup /home/pi/backups/db_${CURRENT_DATE}.backup"
