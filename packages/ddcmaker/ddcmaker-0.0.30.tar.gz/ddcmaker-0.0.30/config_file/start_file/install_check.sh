#!/bin/bash
last_version=$(curl https://mirrors.aliyun.com/pypi/simple/ddcmaker/ | grep -P 'ddcmaker-[\d\.]+' -o | grep -P '[\d\.]+' -o | sort -r -u -n -k 3 -t '.' | head -1)
for i in `seq 60`
do
  local_version=`python3 -c "import ddcmaker; print(ddcmaker.__version__)"`
  if [ $local_version \> $last_version ]; then
    sudo reboot
  elif [ $local_version \= $last_version ]; then
    sudo reboot
  fi
  sleep 10
  
done
