# Imports
import webiopi
import sys,os
import subprocess
import time 

import RPi.GPIO as GPIO

# Retrieve GPIO lib
#GPIO = webiopi.GPIO

os.system("sudo echo -n 0 > codematch.txt")
proc_start = 0

led = 11 #gpio 17

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
           with open("/home/pi/trush_workdir/scripts/homealarm/armed.txt", "r") as fo:
              fo.seek(0, 0) 
              armed_status = fo.read(1)
           fo.closed
           print "Armed status: " + str(armed_status)
           
           if (armed_status == "1"):
              if (proc_start == 0):
                p = subprocess.Popen(["sudo","/home/pi/trush_workdir/rf_xmit/433Utils/RPi_utils/RFSniffer"], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
              proc_start = 1
              time.sleep(10)
             
              with open("/home/pi/trush_workdir/scripts/homealarm/codematch.txt", "r") as fo1:
                fo1.seek(0, 0)
                codematch_status = fo1.read(1)
              fo1.closed 
              if (codematch_status == "1"):
                print "RF code match recvd. Sound the alarm!!!"
                subprocess.call(["bash","intruder_mail.sh"]) 
                for i in range(0,5):
                   blink(led)
                                
                #todays_date = datetime.datetime.today()
                #try:
                #  api.update_status_with_media(status = ("Intruder alert: " + todays_date.strftime('%m-%d-%y-%H%M')), media= image_path)
                #except tweetpony.APIError as err:
                #  print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)
           elif (armed_status == "0"): 
               os.system("sudo echo -n 0 > /home/pi/trush_workdir/scripts/homealarm/codematch.txt")
               
p.kill()
GPIO.cleanup()


