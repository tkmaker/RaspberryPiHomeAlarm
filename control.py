# Imports
import webiopi
import sys,os
import subprocess
import time 

# Retrieve GPIO lib
GPIO = webiopi.GPIO

os.system("sudo echo -n 0 > armed.txt")

def arm():
  os.system("sudo echo -n 1 > armed.txt")

def disarm():
  os.system("sudo echo -n 0 > armed.txt")

# Instantiate the server on the port 8085, it starts immediately in its own thread
server = webiopi.Server(port=8085, login="tk", password="tk")

server.addMacro(arm)
server.addMacro(disarm)

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()


# Stop the server
server.stop()


