to_be_watched=$1
ps aux | grep -i $to_be_watched | grep -v grep
