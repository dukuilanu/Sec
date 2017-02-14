import urllib2
import RPi.GPIO as GPIO
import time
from picamera import PiCamera


camera = PiCamera()
detectPin = 16
lightPin = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(detectPin, GPIO.IN)
GPIO.setup(lightPin, GPIO.OUT)
GPIO.output(lightPin, GPIO.LOW)
GPIO.setwarnings(False)

global enabled
state = 0
timeCounter = 0

class interact(object):
	def pull(self):
		response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&pulling=true')
		html = response.read()
		for line in html:
			if line.rstrip() == "2":
				global enabled
				enabled = 1
			if line.rstrip() == "3":
				global enabled
				enabled = 0
			if line.rstrip() == "1":
				return "picTime"
		print enabled

	def event(self, state):
		response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&event=' + state)

interact = interact()

while 1:
	if time.time() >= (timeCounter + 1):
		timeCounter = time.time()
		isPic = interact.pull()
		if isPic == "picTime":
			camera.capture('/root/temp/photo/' + str(time.time()).replace( '.', '' ) + '.jpg')

	input_value = GPIO.input(detectPin)
	if state == 0:
		if input_value == 1:
			state = 1
			if enabled == 1:
				print "motion detected!"
				GPIO.output(lightPin, GPIO.HIGH)
				camera.start_recording('/root/temp/video/video' + str(time.time()) + '.h264', bitrate=4000000)
				interact.event("started")
	else:
		if input_value == 0:
			state = 0
			if enabled == 1:
				print "motion stopped."
				GPIO.output(lightPin, GPIO.LOW)
				camera.stop_recording()
				interact.event("stopped")
