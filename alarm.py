# Imports
import webiopi
import sys,os
import subprocess
import time 

# Retrieve GPIO lib
GPIO = webiopi.GPIO

os.system("sudo echo -n 0 > codematch.txt")
proc_start = 0

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
#todays_date = datetime.datetime.today()
#try:
#  api.update_status_with_media(status = ("Intruder alert: " + todays_date.strftime('%m-%d-%y-%H%M')), media= image_path)
#except tweetpony.APIError as err:
#  print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)


p.kill()
