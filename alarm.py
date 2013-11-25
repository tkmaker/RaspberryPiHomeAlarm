# Imports
import webiopi
import sys,os
import subprocess
import time 
import signal

import RPi.GPIO as GPIO


os.system("sudo echo -n 0 > /home/pi/trush_workdir/scripts/homealarm/trigger.txt")
proc_start = 0

led = 26 #gpio 7

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# set up GPIO output channel for pin 11 GPIO 17
GPIO.setup(led, GPIO.OUT)
GPIO.output(led,GPIO.LOW)

def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return

def kill_child_process():
          print "Killing RFSniffer process pid %s"%p0.pid
          os.killpg(p0.pid,signal.SIGTERM)
          print "Killing Motion process  pid %s"%p1.pid
          os.killpg(p1.pid,signal.SIGTERM)

while True:
      try:
 	   #open armed.txt and check current status
           with open("/home/pi/trush_workdir/scripts/homealarm/armed.txt", "r") as fo:
              fo.seek(0, 0) 
              armed_status = fo.read(1)
           fo.closed
           print "Armed status: " + str(armed_status)
           time.sleep(1)

           #if armed, start RF sniffer process if not already started. Check for trigger to sound alarm.
           if (armed_status == "1"):
              if (proc_start == 0):
                p0 = subprocess.Popen(["sudo","/home/pi/trush_workdir/rf_xmit/433Utils/RPi_utils/RFSniffer"],preexec_fn=os.setsid)
                p1 = subprocess.Popen(["sudo","motion","-n"],preexec_fn=os.setsid)
                proc_start = 1
              time.sleep(1)
             
              with open("/home/pi/trush_workdir/scripts/homealarm/trigger.txt", "r") as fo1:
                fo1.seek(0, 0)
                trigger_status = fo1.read(1)
              fo1.closed 
              if (trigger_status == "1"):
                print "Trigger recvd. Sound the alarm!!!"
                subprocess.call(["bash","intruder_mail.sh"]) 
                for i in range(0,20):
                   blink(led)

           #Else if system is disarmed - Clear trigger status for next run                     
           elif (armed_status == "0"): 
               os.system("sudo echo -n 0 > /home/pi/trush_workdir/scripts/homealarm/trigger.txt")
               if (proc_start == 1):
                    kill_child_process()
                    proc_start = 0

      except KeyboardInterrupt:
        print "Program ended by user\n"
        kill_child_process()
        break
         
GPIO.cleanup()


