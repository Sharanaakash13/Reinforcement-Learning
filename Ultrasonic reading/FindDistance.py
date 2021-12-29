import numpy as np
import Jetson.GPIO as gpio
import time
from time import sleep


class FindDistance(object):
    
    
    def __init__(self):
        gpio.setmode(gpio.BOARD)

        # set up  and init 
        self.trigger = 11
        self.echo = 12

        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

        self.pulse_start = 0.
        self.pulse_end = 0.
        self.speed_of_sound = 343 * 100
        self.max_distance = 400
        self.min_distance = 2
    

    def get_distance(self):
        
        # clear trigger
        gpio.output(self.trigger, False)
        time.sleep(0.1)
    
        # send pulse from trigger
        gpio.output(self.trigger, True)
        time.sleep(0.00001)
        gpio.output(self.trigger, False)
    
    
        # check echo for return signal
        while gpio.input(self.echo) == 0:
            self.pulse_start = time.time()
    
        while gpio.input(self.echo) == 1:
            self.pulse_end = time.time()
		#print("Got the signal back!")
        
        pulse_duration = self.pulse_end - self.pulse_start
        distance = self.speed_of_sound / 2. * pulse_duration
        distance = round(distance, 2)
        #distance /= 2.54    # inches
	#print("distance:{}".format(distance))
    
        # filter out things far away
        if distance > self.max_distance:
            distance = self.max_distance
        
        # filter out shit
        if distance < self.min_distance:
            disance = self.min_distance
    
        return distance


