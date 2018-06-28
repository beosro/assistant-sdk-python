import rgb
import time
import random
import thread

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
                        5:self.shutdown
                }

        def default(self):
                rgb.changeto(0,255,255,0.005)

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

        def shutdown(self):
                rgb.changeto(0,0,0,0.006)

        def start(self):
                try:
                    while True:
                        self.modes[self.main.colourMode]()
                        # If CTRL+C is pressed the main loop is broken
                except KeyboardInterrupt:
                            self.modes[5]()
                            time.sleep(1)
                            print "/Quitting"
                         
                        # Actions under 'finally' will always be called
                finally:
                            # Stop and finish cleanly so the pins
                            # are available to be used again
                            rgb.RED.stop()
                            rgb.BLUE.stop()
                            rgb.GREEN.stop()
                            rgb.GPIO.cleanup()

