ps aux | grep -i WXWork.exe | grep -v grep | cut -c 9-15 | xargs kill -s 9
