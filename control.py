# Imports
import webiopi
import sys,os
import subprocess
import time 
import signal

# Retrieve GPIO lib
GPIO = webiopi.GPIO

os.system("sudo echo -n 0 > /home/pi/trush_workdir/scripts/homealarm/armed.txt")

def arm():
  os.system("sudo echo -n 1 > /home/pi/trush_workdir/scripts/homealarm/armed.txt")

def disarm():
  os.system("sudo echo -n 0 > /home/pi/trush_workdir/scripts/homealarm/armed.txt")

# Instantiate the server on the port 8085, it starts immediately in its own thread
server = webiopi.Server(port=8085, login="tk", password="tk")

server.addMacro(arm)
server.addMacro(disarm)

#start keypad.py and alarm.py process
p0 = subprocess.Popen(["sudo","python","keypad.py"],preexec_fn=os.setsid)
p1 = subprocess.Popen(["sudo","python","alarm.py"],preexec_fn=os.setsid)

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

os.killpg(p0.pid,signal.SIGTERM)
os.killpg(p1.pid,signal.SIGTERM)

# Stop the server
server.stop()


