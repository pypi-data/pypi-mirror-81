#!/bin/bash

sleep 20
last_version=`curl https://mirrors.aliyun.com/pypi/simple/ddcmaker/ |grep -P 'ddcmaker-[\d\.]+' -o|grep -P '[\d\.]+' -o|sort -r -u -n -k 3 -t '.' |head -1`
local_version=`pip3 list|grep ddcmaker|grep -P '[\d\.]+' -o`
if [ "$local_version" = "" ]; then
  sudo pip3 install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple ddcmaker >> /home/pi/system_start.log 2>&1
  if [ $? -eq 0 ]; then
      echo $(date "+%Y-%m-%d %H:%M:%S") ': upgrade_check success' >> /home/pi/system_start.log
  else
      echo $(date "+%Y-%m-%d %H:%M:%S") ': upgrade_check failed' >> /home/pi/system_start.log
  fi
  exit 0
  sudo reboot
elif [ $local_version \< $last_version ];then
  sudo pip3 install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple ddcmaker >> /home/pi/system_start.log 2>&1
  if [ $? -eq 0 ]; then
      echo $(date "+%Y-%m-%d %H:%M:%S") ': upgrade_check success' >> /home/pi/system_start.log
  else
      echo $(date "+%Y-%m-%d %H:%M:%S") ': upgrade_check failed' >> /home/pi/system_start.log
  fi
  exit 0
  sudo reboot
else
  echo $(date "+%Y-%m-%d %H:%M:%S") ': ddcmake don`t need to update' >> /home/pi/system_start.log
fi
