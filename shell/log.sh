#!/usr/bin/expect -f
set user wydev
set target [lindex $argv 0]
set target_head 10.0.2.
set remoteport 22

set bindport [lindex $argv 0]
set host 112.21.188.132
set password Wy1qaz@123
set timeout -1

spawn ssh -L $bindport:$target_head$target:$remoteport -p 3202 $user@$host
expect {
    "yes/no" { send "yes\r";exp_continue }
    "password:" { send "$password\r" }
}
interact
