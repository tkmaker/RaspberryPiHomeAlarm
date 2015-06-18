#!/bin/bash

############ Parameters ############
dest="username@gmail.com"
############ End Parameters ############


 subject="Home Alarm Motion Detect!"
 message="WARNING! Motion detected on home alarm system"
 echo $message | mail -s "$subject" $dest
exit


