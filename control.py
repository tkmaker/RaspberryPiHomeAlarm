# Imports
import webiopi
import sys,os
import subprocess
import time 
import signal
from config import config

# Retrieve GPIO lib
GPIO = webiopi.GPIO

tx_pin = 17 #gpio 17
GPIO.setFunction(tx_pin, GPIO.OUT)

armed_file = config['home_alarm_git_dir'] + "/armed.txt"
send_script = config['rf433_dir'] + "/send "

os.system("sudo echo -n 0 > " +armed_file)

def arm():
  os.system("sudo echo -n 1 > " + armed_file)

def disarm():
  os.system("sudo echo -n 0 > " + armed_file)


def sw1_toggle():
  os.system("sudo "+ send_script + config ['switch1'])

def sw2_toggle():
 os.system("sudo " + send_script + config ['switch2'])


def sw3_toggle():
 os.system("sudo " + send_script + config ['switch3'])


# Instantiate the server on the port 8085, it starts immediately in its own thread
server = webiopi.Server(port=config['port'], login=config['browser_username'], password=config['browser_passwd'])

server.addMacro(arm)
server.addMacro(disarm)
server.addMacro(sw2_toggle)
server.addMacro(sw1_toggle)
server.addMacro(sw3_toggle)

#start keypad.py and alarm.py process
p0 = subprocess.Popen(["sudo","python","keypad.py"],preexec_fn=os.setsid)
p1 = subprocess.Popen(["sudo","python","alarm.py"],preexec_fn=os.setsid)

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

os.killpg(p0.pid,signal.SIGTERM)
os.killpg(p1.pid,signal.SIGTERM)

# Stop the server
server.stop()


