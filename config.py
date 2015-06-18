from collections import defaultdict

config = defaultdict()

#Directory where git code is present
config['home_alarm_git_dir'] = "/home/pi/trush_workdir/scripts/homealarm_git"

#Dir where 433 MHz scripts are installed
config['rf433_dir'] = "/home/pi/trush_workdir/rf_xmit/433Utils/RPi_utils"

#Keypad arm/disarm code
config['keypad_code'] = 123

#Webserer port
config['port'] = 8085

#Webserver username
config['browser_username'] = "anyusername"

#Webserver password
config['browser_passwd'] = "anypassword"

#RF code for first switch outlet
config['switch1'] =  "1398209"

#RF code for second switch outlet
config['switch2'] = "1398065"

#RF code for third switch outlet
config['switch3'] = "1398029"

#RF code for enableing the RF Siren
config['siren_enable'] = "1568816"

#RF code for disabling the RF Siren
config['siren_disable'] = "1568771"

#Send gtalk message using a script
config['send_gtalk_message'] = "/home/pi/trush_workdir/raspi_gtalk_robot/tkgtalk.py"
config['enable_gtalk_message'] = 0

#Enable webcam motion tracking
config['webcam_motion_enable']=0
