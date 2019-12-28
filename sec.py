#!/usr/bin/python
import smtplib
import urllib2
import time
import RPi.GPIO as GPIO
import os
from picamera import PiCamera
enabled = 0
state = 0
timeCounter = 0
detectPin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(detectPin, GPIO.IN)
GPIO.setwarnings(False)

print "starting mounts..."
time.sleep(5)
os.system('touch /home/pi/www/cameraStartTimestamp')
time.sleep(5)
os.system('touch /home/pi/sec_video/cameraStartTimestamp')
print "mounts complete."

class interact(object):
        def pull(self):
                global enabled
                html = ""
                e = 0
                try:
                        response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&pulling=true')
                except:
                        print "Web server not available."
                if e == 0:
                        html = response.read()
                for line in html:
                        if line.rstrip() == "2":
                                if enabled == 0:
                                        print "enabling motion sensor"
                                enabled = 1
                        if line.rstrip() == "3":
                                if enabled == 1:
                                        print "disabling sensor"
                                enabled = 0
                        if line.rstrip() == "1":
                                return "picTime"

        def event(self, state):
                try:
                        response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&event=' + state)
                except:
                        print "Web server not available."

        def smail(self,context):
                s = smtplib.SMTP('smtp.gmail.com', 587)
                username = 'pytheaserrans@gmail.com'
                password = 'WardatuAksu1'
                replyto = 'pytheaserrans@gmail.com'
                sendto = ['pytheaserrans@gmail.com']
                sendtoShow = 'pytheaserrans@gmail.com'
                subject = 'Security Camera Alert'
                content = "Action: " + context
                mailtext = 'From: ' + replyto + '\nTo: ' + sendtoShow + '\n'
                mailtext = mailtext + 'Subject:' + subject + '\n' + content
                s.starttls()
                s.ehlo()
                s.login(username,password)
                s.sendmail(replyto, sendto, mailtext)
                rslt=s.quit()

interact = interact()
first_time = time.time()
while 1:
        isPic = interact.pull()
        if isPic == "picTime":
                print "ispic"
                interact.smail("pic")
                camera = PiCamera()
                camera.rotation = 270
                timeStamp = str(time.time()).replace( '.', '' )
                camera.capture('/home/pi/www/photo/' + timeStamp + '.jpg')
                response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&newPic=true&picTime=' + timeStamp)
                camera.close()

        if enabled == 1:
                inputValue = GPIO.input(detectPin)
                if inputValue == 1:
                        state = 1
                        interact.smail("motion")
                        camera = PiCamera()
                        camera.rotation = 270
                        last_start_time = time.time()
                        print "motion detected after: " + str(last_start_time - first_time)
                        first_time = last_start_time
                        interact.event("started")
                        camera.start_recording('/home/pi/sec_video/sec_' + str(time.time()) + '.h264', bitrate=4000000)
                        while state == 1:
                                inputValue = GPIO.input(detectPin)
                                interact.pull()
                                if enabled == 0:
                                        state=0
                                if inputValue == 0:
                                        state = 0
                        elapsed_time = time.time() - last_start_time
                        print "motion stopped after " + str(elapsed_time)
                        camera.stop_recording()
                        camera.close()
                        interact.event("stopped")