import time
from threading import Thread
from rgbled.eyes import Eyes
from face.face import Face
import os
from siricontrol import *

class Mode:
    def __init__(self, main):
        self.colourMode = 0
        self.speakingMode = 0
        self.sleepMode = 0
        self.timer = 0
        self.wakeTime = 1
        self.wakeEyes = 0
        self.trackMode = "auto"
        self.mode = "start"
	self.main = main
        self.modes = {   
            "EventType.ON_RESPONDING_STARTED": self.startSpeaking,
            "EventType.ON_RESPONDING_FINSIHED": self.stopSpeaking,
            "EventType.ON_CONVERSATION_TURN_STARTED": self.startListening,
            "EventType.ON_END_OF_UTTERANCE": self.stopListening,
            "EventType.ON_CONVERSATION_TURN_FINISHED": self.stopSpeaking
        }

        #check = Thread(target=self.checkMode)
        #check.daemon = True
        #check.start()

        self.face = Face(self)
        self.faceTracking = Thread(target=self.face.startup)
        self.faceTracking.daemon = True
        self.faceTracking.start()

        self.eyes = Eyes(self)
        ledEyes = Thread(target=self.eyes.start)
        ledEyes.daemon = True
        ledEyes.start()
	
	self.main.welcome()

        self.siri = Control(self)
        siricontrol = Thread(target=self.siri.handle)
        siricontrol.daemon = True
        siricontrol.start()
        
        #self.eyes = Eyes(self)
        #ledEyes = Thread(target=self.eyes.start)
        #ledEyes.daemon = True
        #ledEyes.start()
  
    def changeVoiceMode(self,event):
        try:
            self.mode = event.type
        except:
            self.mode = event
        try:
            print(self.modes[str(self.mode)]())
        except:
            print("PASSED")
            pass
        
    def start(self):
        while True:
            print(self.mode)
            time.sleep(1)

    def startListening(self):
        self.sleepMode = 0
        self.timer = 0
        self.colourMode = 2

    def stopListening(self):
        self.colourMode = 3

    def startSpeaking(self):
        self.sleepMode = 0
        self.timer = 0
        self.colourMode = 1
        self.speakingMode = 1

    def stopSpeaking(self):
        self.colourMode = 0
        self.speakingMode = 0
        self.sleepMode = 0
        self.timer = 0

    def checkMode(self):
        os.system("sudo python /var/www/html/changemode.py auto")
        while True:
            with open("/home/pi/Robot/data.json", "r") as datafile:
                data = json.load(datafile)
                if self.trackMode != data["trackmode"]:
                    self.changeMode(data["trackmode"])
            print(self.trackMode)
            time.sleep(1)

    def changeMode(self, mode):
        if mode == "manual":
            print("abcde")
            self.face.webcam.release()
            self.trackMode = mode
            os.system('/usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -y YUV" -o "/usr/local/lib/output_http.so -w /usr/local/www" &')
        else:
            print("abcde")
            os.system("ps -ef | grep mjpg_streamer | awk '{print $2}' | xargs kill -9")
            time.sleep(2)
            self.trackMode = mode
            #self.faceTracking = Thread(target=self.face.start)
            #self.faceTracking.start()
     
