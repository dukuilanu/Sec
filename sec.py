#!/usr/bin/python
import urllib2
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

enabled = 0
state = 0
timeCounter = 0
detectPin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(detectPin, GPIO.IN)
GPIO.setwarnings(False)

class interact(object):
        def pull(self):
                global enabled
				try:
                    response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&pulling=true')
				except:
					true
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
					true
interact = interact()
first_time = time.time()
while 1:
        isPic = interact.pull()
        if isPic == "picTime":
                print "ispic"
                camera = PiCamera()
                timeStamp = str(time.time()).replace( '.', '' )
                camera.capture('/home/pi/www/photo/' + timeStamp + '.jpg')
                response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&newPic=true&picTime=' + timeStamp)
                camera.close()

        if enabled == 1:
                inputValue = GPIO.input(detectPin)
                if inputValue == 1:
                        state = 1
                        camera = PiCamera()
                        last_start_time = time.time()
                        print "motion detected after: " + str(last_start_time - first_time)
                        first_time = last_start_time
                        camera.start_recording('/home/pi/www/video/sec_' + str(time.time()) + '.h264', bitrate=4000000)
                        interact.event("started")
                        while state == 1:
                                inputValue = GPIO.input(detectPin)
                                if inputValue == 0:
                                         state = 0
                        elapsed_time = time.time() - last_start_time
                        print "motion stopped after " + str(elapsed_time)
                        camera.stop_recording()
                        camera.close()
                        interact.event("stopped")
