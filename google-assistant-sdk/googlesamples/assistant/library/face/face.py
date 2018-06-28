from multiprocessing import Process, Queue
import time
import cv2
import os
import random
import sys
import _thread

class Face:
        def __init__(self, main):
                print("hi")
                self.main = main
                # Upper limit
                self._Servo1UL = 250
                self._Servo0UL = 230

                # Lower Limit
                self._Servo1LL = 75
                self._Servo0LL = 70


                self.ServoBlaster = open('/dev/servoblaster', 'w')		# ServoBlaster is what we use to control the servo motors
                print("hi")
                self.Servo0CP = Queue()	# Servo zero current position, sent by subprocess and read by main process
                self.Servo1CP = Queue()	# Servo one current position, sent by subprocess and read by main process
                self.Servo0DP = Queue()	# Servo zero desired position, sent by main and read by subprocess
                self.Servo1DP = Queue()	# Servo one desired position, sent by main and read by subprocess
                self.Servo0S = Queue()	# Servo zero speed, sent by main and read by subprocess
                self.Servo1S = Queue()	# Servo one speed, sent by main and read by subprocess
                
                Process(target=self.P0, args=()).start()	# Start the subprocesses
                Process(target=self.P1, args=()).start()	#
                time.sleep(1)				# Wait for them to start
        

        def P0(self):	# Process 0 controlles servo0
                self.speed = .1		# Here we set some defaults:
                self._Servo0CP = 99		# by making the current position and desired position unequal,-
                self._Servo0DP = 100		# 	we can be sure we know where the servo really is. (or will be soon)
                while True:
                        try:
                                time.sleep(self.speed)
                                if self.Servo0CP.empty():			# Constantly update Servo0CP in case the main process needs-
                                        self.Servo0CP.put(self._Servo0CP)		# 	to read it
                                if not self.Servo0DP.empty():		# Constantly read read Servo0DP in case the main process-
                                        self._Servo0DP = self.Servo0DP.get()	#	has updated it
                                if not self.Servo0S.empty():			# Constantly read read Servo0S in case the main process-
                                        self._Servo0S = self.Servo0S.get()	# 	has updated it, the higher the speed value, the shorter-
                                        self.speed = .1 / self._Servo0S		# 	the wait between loops will be, so the servo moves faster
                                if self._Servo0CP < self._Servo0DP:					# if Servo0CP less than Servo0DP
                                        self._Servo0CP += 1						# incriment Servo0CP up by one
                                        self.Servo0CP.put(self._Servo0CP)					# move the servo that little bit
                                        self.ServoBlaster.write('0=' + str(self._Servo0CP) + '\n')	#
                                        self.ServoBlaster.flush()					#
                                        if not self.Servo0CP.empty():				# throw away the old Servo0CP value,-
                                                trash = self.Servo0CP.get()				# 	it's no longer relevent
                                if self._Servo0CP > self._Servo0DP:					# if Servo0CP greater than Servo0DP
                                        self._Servo0CP -= 1						# incriment Servo0CP down by one
                                        self.Servo0CP.put(self._Servo0CP)					# move the servo that little bit
                                        self.ServoBlaster.write('0=' + str(self._Servo0CP) + '\n')	#
                                        self.ServoBlaster.flush()					#
                                        if not self.Servo0CP.empty():				# throw away the old Servo0CP value,-
                                                trash = self.Servo0CP.get()				# 	it's no longer relevent
                                if self._Servo0CP == self._Servo0DP:	        # if all is good,-
                                        self._Servo0S = 1		        # slow the speed; no need to eat CPU just waiting
                        except KeyboardInterrupt:
                                pass

        def P1(self):	# Process 1 controlles servo 1 using same logic as above
                self.speed = .1
                self._Servo1CP = 69
                self._Servo1DP = 70
                x = 1
                while x:
                        try:
                                time.sleep(self.speed)
                                if self.Servo1CP.empty():
                                        self.Servo1CP.put(self._Servo1CP)
                                if not self.Servo1DP.empty():
                                        self._Servo1DP = self.Servo1DP.get()
                                if not self.Servo1S.empty():
                                        self._Servo1S = self.Servo1S.get()
                                        self.speed = .1 / self._Servo1S
                                if self._Servo1CP < self._Servo1DP:
                                        self._Servo1CP += 1
                                        self.Servo1CP.put(self._Servo1CP)
                                        self.ServoBlaster.write('1=' + str(self._Servo1CP) + '\n')
                                        self.ServoBlaster.flush()
                                        if not self.Servo1CP.empty():
                                                trash = self.Servo1CP.get()
                                if self._Servo1CP > self._Servo1DP:
                                        self._Servo1CP -= 1
                                        self.Servo1CP.put(self._Servo1CP)
                                        self.ServoBlaster.write('1=' + str(self._Servo1CP) + '\n')
                                        self.ServoBlaster.flush()
                                        if not self.Servo1CP.empty():
                                                trash = self.Servo1CP.get()
                                if self._Servo1CP == self._Servo1DP:
                                        self._Servo1S = 1
                        except KeyboardInterrupt:
                                self.sleep()


        #====================================================================================================
                
        def CamRight(self, distance, speed ):		# To move right, we are provided a distance to move and a speed to move.
                global _Servo0CP			# We Global it so  everyone is on the same page about where the servo is...
                if not self.Servo0CP.empty():		# Read it's current position given by the subprocess(if it's avalible)-
                        self._Servo0CP = self.Servo0CP.get()	# 	and set the main process global variable.
                self._Servo0DP = self._Servo0CP + distance	# The desired position is the current position + the distance to move.
                if self._Servo0DP > self._Servo0UL:		# But if you are told to move further than the servo is built go...
                        self._Servo0DP = self._Servo0UL		# Only move AS far as the servo is built to go.
                self.Servo0DP.put(self._Servo0DP)			# Send the new desired position to the subprocess
                self.Servo0S.put(speed)			# Send the new speed to the subprocess
                return;

        def CamLeft(self,distance, speed):			# Same logic as above
                global _Servo0CP
                if not self.Servo0CP.empty():
                        self._Servo0CP = self.Servo0CP.get()
                self._Servo0DP = self._Servo0CP - distance
                if self._Servo0DP < self._Servo0LL:
                        self._Servo0DP = self._Servo0LL
                self.Servo0DP.put(self._Servo0DP)
                self.Servo0S.put(speed)
                return;


        def CamDown(self,distance, speed):			# Same logic as above
                global _Servo1CP
                if not self.Servo1CP.empty():
                        self._Servo1CP = self.Servo1CP.get()
                self._Servo1DP = self._Servo1CP + distance
                if self._Servo1DP > self._Servo1UL:
                        self._Servo1DP = self._Servo1UL
                self.Servo1DP.put(self._Servo1DP)
                self.Servo1S.put(speed)
                return;


        def CamUp(self,distance, speed):			# Same logic as above
                global _Servo1CP
                if not self.Servo1CP.empty():
                        self._Servo1CP = self.Servo1CP.get()
                self._Servo1DP = self._Servo1CP - distance
                print(self._Servo1DP)
                if self._Servo1DP < self._Servo1LL:
                        self._Servo1DP = self._Servo1LL
                self.Servo1DP.put(self._Servo1DP)
                self.Servo1S.put(speed)
                return;


        def changePos(self, command):			# Same logic as above
                
                if command == "sleep":
                        value = 70
                elif command == "wake":
                        value = 100
                        
                global _Servo1CP
                if not self.Servo1CP.empty():
                        self._Servo1CP = self.Servo1CP.get()
                self._Servo1DP = value
                if self._Servo1DP > self._Servo1UL:
                        self._Servo1DP = self._Servo1UL
                self.Servo1DP.put(self._Servo1DP)
                self.Servo1S.put(1.5)

                global _Servo0CP
                if not self.Servo0CP.empty():
                        self._Servo0CP = self.Servo0CP.get()
                self._Servo0DP = 100
                if self._Servo0DP < self._Servo0LL:
                        self._Servo0DP = self._Servo0LL
                self.Servo0DP.put(self._Servo0DP)
                self.Servo0S.put(1.5)
                return;
        
        
        #============================================================================================================
        def speak(self,m):
                if self.main.speakingMode == 0:
                        self.main.jasper.mic.say(m)

        def change(self):
                if self.main.speakingMode == 0:
                        self.main.colourMode = 4
                        time.sleep(3)
                        self.main.colourMode = 0

        def timer(self):
                while True:
                        if(self.main.sleepMode == 0):
                                if(self.main.wakeTime == 0):
                                        self.wake()
                                        self.main.wakeTime = 1
                                        time.sleep(5)
                                else:
                                        self.main.timer = self.main.timer + 1
                                        time.sleep(1)
                                        print(self.main.timer)
                                        if self.main.timer == 10:
                                                self.sleep()
                                                self.main.sleepMode = 1
                        elif(self.main.sleepMode == 1):
                                self.main.wakeTime = 0
                                

        def sleep(self):
                print("SLEEPING")
                self.main.colourMode = 5
                self.changePos("sleep")
                time.sleep(1)

        def wake(self):
                print("WAKING")
                self.changePos("wake")
                self.main.colourMode = 7
                time.sleep(2)
                self.main.wakeEyes
                
        def setup(self):
                self.webcam = cv2.VideoCapture(0)				# Get ready to start getting images from the self.webcam
                self.webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)		# I have found this to be about the highest-
                self.webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)	# 	resolution you'll want to attempt on the pi
                
        def start(self):
                self.changePos("wake")
                print("hi")
                fe = 0;
                fs = 0;
                messages = ["hi there","How are you today?", "How can I help?", "Hello"];
                _thread.start_new_thread(self.timer,())
                self.setup()

                frontalface = cv2.CascadeClassifier("/home/pi/Robot/face/haarcascade_frontalface_alt2.xml")		# frontal face pattern detection
                profileface = cv2.CascadeClassifier("/home/pi/Robot/face/haarcascade_profileface.xml")		# side face pattern detection

                face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
                Cface = [0,0]		# Center of the face: a point calculated from the above variable
                lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-
                                        # 	a left profile face, or a frontal face; rather than searching for all three every time,-
                                        # 	it uses this variable to remember which is last saw: and looks for that again. If it-
                                        # 	doesn't find it, it's set back to zero and on the next loop it will search for all three.-
                                        # 	This basically tripples the detect time so long as the face hasn't moved much.
                while self.main.trackMode == "auto":
                        faceFound = False	# This variable is set to true if, on THIS loop a face has already been found			# We search for a face three diffrent ways, and if we have found one already-
                                                # there is no reason to keep looking.
                        if not faceFound:
                                fe = 0
                                if lastface == 0 or lastface == 1:
                                        aframe = self.webcam.read()[1]	# there seems to be an issue in OpenCV or V4L or my self.webcam-
                                        aframe = self.webcam.read()[1]	# 	driver, I'm not sure which, but if you wait too long,
                                        aframe = self.webcam.read()[1]	#	the self.webcam consistantly gets exactly five frames behind-
                                        aframe = self.webcam.read()[1]	#	realtime. So we just grab a frame five times to ensure-
                                        aframe = self.webcam.read()[1]	#	we have the most up-to-date image.
                                        fface = frontalface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(60,60))
                                        if fface != ():			# if we found a frontal face...
                                                lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
                                                for f in fface:		# f in fface is an array with a rectangle representing a face
                                                        faceFound = True
                                                        face = f
                                                        fe = 1

                        if not faceFound:
                                fe = 0				# if we didnt find a face yet...
                                if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
                                        aframe = self.webcam.read()[1]	# 	THIS method was the one who found it last loop
                                        aframe = self.webcam.read()[1]
                                        aframe = self.webcam.read()[1]	# again we grab some frames, things may have gotten stale-
                                        aframe = self.webcam.read()[1]	# since the frontalface search above
                                        aframe = self.webcam.read()[1]
                                        pfacer = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
                                        if pfacer != ():		# if we found a profile face...
                                                lastface = 2
                                                for f in pfacer:
                                                        faceFound = True
                                                        face = f
                                                        fe = 1

                        if not faceFound:
                                fe = 0				# a final attempt
                                if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
                                        aframe = self.webcam.read()[1]	#	detect right profile faces, if the cam is looking at-
                                        aframe = self.webcam.read()[1]	#	someone from the left, it won't see them. So we just...
                                        aframe = self.webcam.read()[1]
                                        aframe = self.webcam.read()[1]
                                        aframe = self.webcam.read()[1]
                                        cv2.flip(aframe,1,aframe)	#	flip the image
                                        pfacel = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
                                        if pfacel != ():
                                                lastface = 3
                                                for f in pfacel:
                                                        faceFound = True
                                                        face = f
                                                        fe = 1

                        if not faceFound:
                                fe = 0		# if no face was found...-
                                lastface = 0		# 	the next loop needs to know
                                face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop
                        if fe == 1:
                                self.main.timer = 0
                                if fs == 0:
                                        m = random.choice(messages);
                                        _thread.start_new_thread(self.change,())
                                        _thread.start_new_thread(self.speak,(m,))
                                                
                                        fs = 1 
                        else:
                                fs = 0
                                

                        x,y,w,h = face
                        Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center
                        

                        if Cface[0] != 0:		# if the Center of the face is not zero (meaning no face was found)

                                if Cface[0] > 180:	# The camera is moved diffrent distances and speeds depending on how far away-
                                        self.CamLeft(5,1)	#	from the center of that axis it detects a face
                                if Cface[0] > 190:	#
                                        self.CamLeft(7,2)	#
                                if Cface[0] > 200:	#
                                        self.CamLeft(9,3)	#

                                if Cface[0] < 140:	# and diffrent dirrections depending on what side of center if finds a face.
                                        self.CamRight(5,1)
                                if Cface[0] < 130:
                                        self.CamRight(7,2)
                                if Cface[0] < 120:
                                        self.CamRight(9,3)

                                if Cface[1] > 140:	# and moves diffrent servos depending on what axis we are talking about.
                                        self.CamUp(5,1)
                                if Cface[1] > 150:
                                        self.CamUp(7,2)
                                if Cface[1] > 160:
                                        self.CamUp(9,3)

                                if Cface[1] < 100:
                                        self.CamDown(5,1)
                                if Cface[1] < 90:
                                        self.CamDown(7,2)
                                if Cface[1] < 80:
                                        self.CamDown(9,3)
                                        
        def servoTest(self):
                self.changePos("wake")
                time.sleep(5)
                self.changePos("sleep")

class Main:
    def __init__(self):
        self.colourMode = 5
        self.speakingMode = 0
        self.sleepMode = 0
        self.timer = 0

if __name__=="__main__":
        m = Main()
        f = Face(m)
        f.servoTest()
