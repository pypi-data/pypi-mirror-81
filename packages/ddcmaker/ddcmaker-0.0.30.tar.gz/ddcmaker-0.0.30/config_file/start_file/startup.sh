#!/bin/bash
echo $(date "+%Y-%m-%d %H:%M:%S") ': startserver file' $(sudo find /home/pi -name robotserver.py|sudo head -n 1) >> /home/pi/system_start.log
file_name=$(sudo find /home/pi -name robotserver.py|sudo head -n 1)
echo "file name " $file_name >> /home/pi/system_start.log

dir_name=$(dirname $file_name)
echo "dirname " $dir_name >> /home/pi/system_start.log

cd $dir_name
echo $(pwd) >> /home/pi/system_start.log
/usr/bin/python3  $file_name >> /home/pi/system_start.log 2>&1 &

if [ $? -eq 0 ]; then
    echo $(date "+%Y-%m-%d %H:%M:%S") ': startserver success' >> /home/pi/system_start.log
else
    echo $(date "+%Y-%m-%d %H:%M:%S") ': startserver failed' >> /home/pi/system_start.log
fi
exit 0
