# Imports
import webiopi
import sys,os
import subprocess
import time 

import RPi.GPIO as GPIO


os.system("sudo echo -n 0 > trigger.txt")
proc_start = 0

led = 26 #gpio 7

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set up GPIO output channel for pin 11 GPIO 17
GPIO.setup(led, GPIO.OUT)


def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return


while True:
      try:
 	   #open armed.txt and check current status
           with open("armed.txt", "r") as fo:
              fo.seek(0, 0) 
              armed_status = fo.read(1)
           fo.closed
           print "Armed status: " + str(armed_status)
           time.sleep(1)

           #if armed, start RF sniffer process if not already started. Check for trigger to sound alarm.
           if (armed_status == "1"):
              if (proc_start == 0):
                p = subprocess.Popen(["sudo","/home/pi/trush_workdir/rf_xmit/433Utils/RPi_utils/RFSniffer"])
                proc_start = 1
              time.sleep(10)
             
              with open("trigger.txt", "r") as fo1:
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
               os.system("sudo echo -n 0 > trigger.txt")
               if (proc_start == 1):
                    p.kill()
                    proc_start = 0

      except KeyboardInterrupt:
        print "Proram ended by user\n"
        break
         
p.kill()
GPIO.cleanup()


