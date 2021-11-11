#!/usr/bin/expect -f

set password P1223o4d@123


spawn mount -t cifs -o uid=1000,gid=1000,dir_mode=0755,file_mode=0755,username=zhangyan //192.168.1.54/Microsoft/ /home/jerry/Microsoft/
expect {
    -re "Password for zhangyan@//192.168.1.54/Microsoft/:" { send "$password\r" }
}
interact

spawn mount -t cifs -o uid=1000,gid=1000,dir_mode=0755,file_mode=0755,username=zhangyan //192.168.1.54/UserHome/zhangyan/ /home/jerry/CifsDocuments/
expect {
    -re "Password for zhangyan@//192.168.1.54/UserHome/zhangyan/:" { send "$password\r" }
}
interact
