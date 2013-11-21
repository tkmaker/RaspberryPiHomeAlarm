#!/bin/bash

############ Parameters ############
user="pi"
mittente="<from_email>@gmail.com"
dest="<to_email>@gmail.com"
smtp="smtp.gmail.com:587"
username="<from_email>@gmail.com"
pass="<my password>"
############ End Parameters ############


 subject="Home Alarm Motion Detect!"
 message="WARNING! Motion detected on home alarm system"
 sendEmail -f $mittente -t $dest -u $subject -s $smtp -xu $username -xp $pass -m $message
exit


