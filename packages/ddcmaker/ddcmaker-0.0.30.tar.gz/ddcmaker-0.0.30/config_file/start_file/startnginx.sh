#!/bin/bash
sudo /usr/local/nginx/sbin/nginx
echo "start system" > /home/pi/system_start.log
if [ $? -eq 0 ]; then
    echo $(date "+%Y-%m-%d %H:%M:%S") ': startnginx success' >> /home/pi/system_start.log
else
    echo $(date "+%Y-%m-%d %H:%M:%S") ': startnginx failed' >> /home/pi/system_start.log
fi
exit 0
