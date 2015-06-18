# Imports
import webiopi
import sys,os
import subprocess
import time 
import signal

import RPi.GPIO as GPIO
from config import config

armed_file = config['home_alarm_git_dir'] + "/armed.txt"
trigger_file = config['home_alarm_git_dir'] + "/trigger.txt"
send_script = config['rf433_dir'] + "/send "
rf_sniffer_script = config['rf433_dir'] + "/RFSniffer"

print "Clearing trigger file"

os.system("sudo echo -n 0 > "+ trigger_file)

#initialize variables
proc_start = 0
mail_sent = 0
siren_triggered =0


#GPIO used in program 
led = 26 #gpio 7

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Setup GPIO Direction
GPIO.setup(led, GPIO.OUT)

GPIO.output(led,GPIO.LOW)

#Function to be used by LED
def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(1)
        return

def kill_child_process():
          print "Killing RFSniffer process pid %s"%p0.pid
          os.killpg(p0.pid,signal.SIGTERM)
          if (config['webcam_motion_enable']):
               print "Killing Motion process  pid %s"%p1.pid
               os.killpg(p1.pid,signal.SIGTERM)

while True:
      try:
 	   #open armed.txt and check current status
           with open(armed_file, "r") as fo:
              fo.seek(0, 0) 
              armed_status = fo.read(1)
           fo.closed
           #print "Armed status: " + str(armed_status)
           time.sleep(1)

           #if armed, start RF sniffer process if not already started. Check for trigger to sound alarm.
           if (armed_status == "1"):
              
              if (proc_start == 0):
                
                #Blink 2 times to indicate arm
                for i in range(0,2):
                   blink(led)
                #Start switch 3 - Webcam will be connected to this
                if (config['webcam_motion_enable']):
                    os.system("sudo "+ send_script + config['switch3'])
 
                #Allow some delay to leave home - 1 min here
                time.sleep(60)
                p0 = subprocess.Popen(["sudo",rf_sniffer_script],preexec_fn=os.setsid)
                if (config['webcam_motion_enable']):
                   p1 = subprocess.Popen(["sudo","motion","-n"],preexec_fn=os.setsid)
                proc_start = 1
             
              with open(trigger_file, "r") as fo1:
                fo1.seek(0, 0)
                trigger_status = fo1.read(1)
              fo1.closed 
            
              if (trigger_status == "1"):

                #Allow some time (45 sec) to disarm the system
                time.sleep(45)


                print "Trigger recvd. Sound the alarm!!!"

                #Trigger siren if not already done 
                if (siren_triggered == 0):
                   if (config['enable_gtalk_message']):
                       print("Sending gtalk message")
                       os.system("sudo python " + config ['send_gtalk_message'])
                   os.system("sudo " + send_script + config['siren_enable']) 
                   siren_triggered =1

                #Send an email if not already sent 
                if (mail_sent == 0):
                     subprocess.call(["bash","intruder_mail.sh"])
                     mail_sent = 1 
             
           #Else if system is disarmed                     
           elif (armed_status == "0"): 
               #Do below only if system was armed before
               if (proc_start == 1):
                    #Turn off siren
                    os.system("sudo " + send_script + config['siren_disable'])
                    #Clear trigger for next run
                    os.system("sudo echo -n 0 > " + trigger_file)
                    mail_sent = 0
                    kill_child_process()
                    #Stop switch 3 - Webcam will be connected to this
                    os.system("sudo " + send_script + config['switch3'])
                    proc_start = 0
                    #Blink 4 times to indicate disarm
                    for i in range(0,4):
                       blink(led)

      except KeyboardInterrupt:
        print "Program ended by user\n"
        kill_child_process()
        break
         
GPIO.cleanup()


