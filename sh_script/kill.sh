to_be_killed=$1
ps aux | grep -i $to_be_killed | grep -v grep | cut -c 9-15 | xargs kill -s 9
