import time
import random
import sys
sys.path.insert(0,"/home/pi/voice-recognizer-raspi/src/rgbled/")
import rgb

class Eyes():
        def __init__(self,main):
                rgb.setup(11,9,10,100)
                self.main = main
                print(main.colourMode)
                self.modes = {
                        0:self.default,
                        1:self.speaking,
                        2:self.listening,
                        3:self.loading,
                        4:self.face,
                        5:self.sleeping,
                        6:self.off
                }

        def default(self):
                rgb.changeto(0,100,100,0.005)

        def speaking(self):
                rgb.changeto(255,20,0,0.008)
                time.sleep(0.2)
                rgb.changeto(255,120,0,0.008)
                time.sleep(0.2)

        def listening(self):
                rgb.changeto(255,0,255,0.007)
                time.sleep(0.6)
                rgb.changeto(255,180,255,0.004)
                time.sleep(0.1)

        def loading(self):
                rgb.changeto(255,255,0,0.002)
                time.sleep(0.2)
                rgb.changeto(0,0,0,0.004)
                time.sleep(0.008)

        def face(self):
                global x
                x = 2
                rgb.changeto(0,255,0,0.008)
                time.sleep(0.001)
                rgb.changeto(0,255,255,0.008)

        def sleeping(self):
                rgb.changeto(0,0,0,0.006)
                time.sleep(3)
                rgb.RED.stop()
                rgb.BLUE.stop()
                rgb.GREEN.stop()
                

        def off(self):
               rgb.changeto(0,0,0,0.006) 


        def start(self):
                try:
                    while True:
                            if self.main.colourMode == 7 and self.main.wakeEyes == 0:
                                    rgb.RED.start(0)
                                    rgb.BLUE.start(0)
                                    rgb.GREEN.start(0)
                                    self.main.colourMode = 0
                            self.modes[self.main.colourMode]()
                            print(self.main.colourMode)
                        # If CTRL+C is pressed the main loop is broken
                except KeyboardInterrupt:       
                            self.modes[5]()
                            time.sleep(1)
                            print("/Quitting")
                         
                        # Actions under 'finally' will always be called
                finally:
                            # Stop and finish cleanly so the pins
                            # are available to be used again
                            rgb.RED.stop()
                            rgb.BLUE.stop()
                            rgb.GREEN.stop()
                            rgb.GPIO.cleanup()

