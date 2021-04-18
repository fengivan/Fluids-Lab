from time import sleep
from time import sleep
from widgetlords.pi_spi import *
import numpy as np
from widgetlords import *

from pynput import mouse
import pandas
import time
import sys
import threading
import RPi.GPIO as GPIO

init()
output = Mod2AO(False)
output2=Mod2AO(True)
minSpeed=745
maxSpeed=(int)((3723+745)/2)
inputs=Mod8AI()


def addWater(time):  #opens water valve for time seconds
    stopAdd = threading.Timer(time, stopWater)
    output2.write_single(0,1750)
    print("Adding water for "+ str(time)+ " seconds.")
    stopAdd.start()
    
def stopWater():
    output2.write_single(0,0)
    print("Done")


def dumpMud(time):  #opens water valve for time seconds
    stopAdd = threading.Timer(time, stopDump)
    output2.write_single(1,1750)
    print("Dumping Mud for "+ str(time)+ " seconds.")
    stopAdd.start()
    
def stopDump():
    output2.write_single(1,0)
    print("Done")
    
def distancethread():
    GPIO.setmode(GPIO.BCM)
    trigger=23
    echo=24
    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trigger, True)
    time.sleep(.00001)
    GPIO.output(trigger, False)
    start=time.time()
    arrived=False
    while time.time()-start<5:
        if GPIO.input(echo)==0 and not arrived:
            start=time.time()
        elif GPIO.input(echo)==0:
            bouncetime=time.time()-start
            GPIO.cleanup()
            return bouncetime*34300/2
        if GPIO.input(echo)==1:
            arrived=True
            
def distance ():
    getdistance = threading.Timer(0, distancethread)
    getdistance.start()
    
def getpH(): #returns pH and temp
    return((counts_to_value(inputs.read_single(1), 745, 3723, 4, 20 )+.03)*.875-3.5, (counts_to_value(inputs.read_single(0), 745, 3723, 4, 20)+.03)*6.25-25)
    
