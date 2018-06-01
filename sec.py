import urllib2
import time
from picamera import PiCamera

enabled = 0
state = 0

class interact(object):
        def pull(self):
                global enabled
                response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&pulling=true')
                html = response.read()
                for line in html:
                        if line.rstrip() == "2":
                                enabled = 1
                        if line.rstrip() == "3":
                                enabled = 0
                        if line.rstrip() == "1":
                                return "picTime"

        def event(self, state):
                response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&event=' + state)

interact = interact()

while 1:
        isPic = interact.pull()
        if isPic == "picTime":
                print "ispic"
                camera = PiCamera()
                timeStamp = str(time.time()).replace( '.', '' )
                camera.capture('/home/pi/www/photo/' + timeStamp + '.jpg')
                response = urllib2.urlopen('http://192.168.1.143/api.php?sec=true&newPic=true&picTime=' + timeStamp)
                camera.close()

