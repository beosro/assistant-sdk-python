import random, time
import RPi.GPIO as GPIO
import math
from threading import Thread

def setup(rpin,gpin,bpin,freq):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rpin, GPIO.OUT)
        GPIO.setup(gpin, GPIO.OUT)
        GPIO.setup(bpin, GPIO.OUT)
        global RED
        RED = GPIO.PWM(rpin, freq)
        RED.start(0)
        global GREEN
        GREEN = GPIO.PWM(gpin, freq)
        GREEN.start(0)
        global BLUE
        BLUE = GPIO.PWM(bpin, freq)
        BLUE.start(0)
        global frequency
        frequency = freq
        global redprev
        redprev = 0
        global greenprev
        greenprev = 0
        global blueprev
        blueprev = 0



def changeto(redv,greenv,bluev,speed):
        global redprev
        global greenprev
        global blueprev
        GPIO.setwarnings(False)
        r = int(float(round(redv/2.55)))
        g = int(float(round(greenv/2.55)))
        b = int(float(round(bluev/2.55)))
        rt = Thread(target=changered,args=(r,speed))
        gt = Thread(target=changegreen,args=(g,speed))
        bt = Thread(target=changeblue,args=(b,speed))
        rt.start()
        gt.start()
        bt.start()
        time.sleep(speed + 0.7)

def changered(red,speed):
        global redprev
        if(red > redprev):
                for x in range (redprev,red):
                        try:
                            RED.ChangeDutyCycle(x)
                            time.sleep(speed)
                        except:
                                pass
        else:
                down = redprev - red
                for x in range (0,down):
                        try:
                            RED.ChangeDutyCycle(redprev - x )
                            time.sleep(speed)
                        except:
                                pass
        redprev = red

def changegreen(green,speed):
        global greenprev
        if(green > greenprev):
                for x in range (greenprev,green):
                        try:
                            GREEN.ChangeDutyCycle(x)
                            time.sleep(speed)
                        except:
                                pass
        else:
                down = greenprev - green
                for x in range (0,down):
                        try:
                            GREEN.ChangeDutyCycle(greenprev - x )
                            time.sleep(speed)
                        except:
                                pass
        greenprev = green

def changeblue(blue,speed):
        global blueprev
        if(blue > blueprev):
                for x in range (blueprev,blue):
                        try:
                            BLUE.ChangeDutyCycle(x)
                            time.sleep(speed)
                        except:
                                pass
        else:
                down = blueprev - blue
                for x in range (0,down):
                        try:
                            BLUE.ChangeDutyCycle(blueprev - x )
                            time.sleep(speed)
                        except:
                                pass
        blueprev = blue

