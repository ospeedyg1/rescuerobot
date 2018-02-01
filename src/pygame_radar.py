#!/usr/bin/env python
# pygame_radar.py takes in information from ultrasound sensor and graphs it
# to a radar display

# Original Source Code:
# https://www.youtube.com/redirect?q=http%3A%2F%2Farkouji.cocolog-nifty.com%2Fblog%2F2016%2F02%2Fraspberry-pi360.html&event=video_description&v=Hqkki-Jl4Y0&redir_token=Mpq6_On6NVQa4GJB1g0-_uQ2zn98MTUxNTYzNDM4MUAxNTE1NTQ3OTgx

# Modified By: Jeovanny Reyes
# Modified On: January 22, 2018

# Raytheon Radar Guided Rescue Robot
# Cal State LA Senior Design

import math
from sys import exit
import time
#import subprocess
import pygame
import numpy as np

import rospy
from sensor_msgs.msg import Range #as Float32 # Importing from ultrasound information
#import sensor_msgs.msg

# class RadarDisplay(object):
#     def __init__(self): rg
#         #self.x = 1
#         #rospy.init_node("radar_display", anonymous=True)
#         self.rada_dispa = rospy.Subscriber("HerculesUltrasound",Range, self.callback) #Used to be Float32. [Float 32, callback]
#
def callback(range): # Takes in message "range" as input
    #rospy.loginfo(rospy.get_caller_id() + "I heard %f", range.range)
    #self.dist = range.range
    dist = 3.05
    return dist

# def dista(call):
#     dist = callback(range)
#     return dist

def main():

    rospy.init_node("radar_display", anonymous=True)
    rospy.Subscriber("HerculesUltrasound",Range, callback) #Used to be Float32. [Float 32, callback]
    pygame.init() # Initializing pygame

    # Adjusting window
    sx = 1000 # Width
    sy = 1000 # Height
    depth_bits = 32 # Number of bits to use for color.

    # Initializing screen for display. Creates a display surface.
    init_screen = pygame.display.set_mode((sx, sy), 0, depth_bits) # Initializing screen for display
    title = pygame.display.set_caption('RGRR Display')
    screen = pygame.display.get_surface() # Returns a reference to the current dusplay.

    # Loop until the user clicks the close button.
    done = False

    # Initialize variables
    StepCounter = 0
    Rrx = [0] *512 # Creates an array of 512 zeros
    Rry = [0] *512 # Creates an array of 512 zeros
    pos = 2
    circ_rad = 4

    #dist = callback(range)

    while (True):

      angle = 0

      # For loop always starts with zero. in this case we have 0, 1 ,2 ...., 2047
      # If we had for i in range(1,2018), we get 1 ,2,  3, .., 2047
      for i in range(2048): # 4096 covers entire circle and is how many times radius line is drawn
    # motor angle (From Arduino)
        #angle = i * 5.625/64 #Part of original code. It increments by 5 degrees (0.087890625)
        angle = i * 6.283/72 #  Line is incremented by 5 degrees (6.283 is 2 pi)
          #angle = 15 # My code
        #
        # for pin in range(0, 4):
        #       xpin = StepPins[pin]
        #       if Seq[StepCounter][pin]!=0:
        #           GPIO.output(xpin, True)
        # else:
        #     GPIO.output(xpin, False)
        #
        # StepCounter += StepDir
        #
        # if (StepCounter>=StepCount):
        #         StepCounter = 0
        # if (StepCounter<0):
        #         StepCounter = StepCount+StepDir
        dist = 3
        #radar_display = RadarDisplay()
        #dist = radar_display(i)
        #print(dist)

        if i%8==0: # Drawing radar arcs and axis. sx and sy originally divided by 2. 8 is the 8 figures drawn
            # Color green: (0,255,0). Color blue: (0,0,255)
           #pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), sx/2, 1) # Outer circle
           # Radius is 1000*(4/5) = 800 cm [400 cm]
           pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), 400, 1) # Outer circle
           #Radius is 1000/5 = 200 cm [100 cm] [100 cm translates to distance of 2]
           pygame.draw.circle(screen, (0, 200,0), (sx/pos, sy/pos), 100, 1) #Inner circle. radius was sx/pos/5*1
           # Radius is 1000*(2/5) = 400 cm [200 cm] [200 transaltes to distance of 3]
           pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), 200, 1) # 2nd Inner circle. radius was sx/pos/5*2
           # Radius is 1000*(3/5) = 600 cm [300 cm]
           pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), 300, 1) # 3rd Inner Circle. radius was sx/pos/5*3
           #pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), sx/pos/5*4, 1) # 4th Inner Circle
           #pygame.draw.circle(screen, (0, 200, 0), (sx/pos, sy/pos), sx/pos/6*5, 1) # 5th Inner circle
           pygame.draw.line(screen, (0, 200, 0), (100, sy/pos), (900, sy/pos)) # Horizontal Line. Origianlly from (0, sy/pos) to (sx,sy/pos)
           pygame.draw.line(screen, (0, 200, 0), (sx/pos, 100), (sx/pos, 900)) # Vertical Line

           text_col = pygame.font.SysFont('Arial',25)
           text_col.render('|_| Circle Increment of 20 cm',True,(0, 200, 0))
           #distance = 2# Create for loop or while loop to continously get values from US.
           #dist = 3

    # Radar Point

           for j in range(512): # 512 is the number of points drawn for entire circle.
    #           col = 255 # 255 is brightest and 0 is darkest
               deg = j * 5.625 / 8 # Increments by 40 degrees
               radar_deg = deg - angle # For first iteration we have 40 - 5 = 35 degrees
               #distance = 2
               if radar_deg <=0 :
                  col = int(255*((360+radar_deg)/360)**1.3) # col is color
                  pygame.draw.circle(screen, (0,col,0),(Rrx[j-1],Rry[j-1]),5)
               else:
                  col = int(255*(radar_deg/360)**1.3)
                  pygame.draw.circle(screen, (0,col,0),(Rrx[j-1],Rry[j-1]),5)

    # IR_sensor value to distance (m)
        #    resp = spi.xfer2([0x68, 0x00])
        #    value = (resp[0] * 256 + resp[1]) & 0x3ff
           if dist < 0: # was originally called distance
               dist = math.fabs(dist) # Returns the absolute value of distance

           dx = sx/2 + sx/2 * math.cos(math.radians(angle))
           dy = sy/2 + sx/2 * math.sin(math.radians(angle))
           # anti aliasing line: To make line smooth
           pygame.draw.aaline(screen, (0, 200, 0), (sx/2, sy/2), (dx, dy),5)

           rx = int(sx/2 + 50 * dist * math.cos(math.radians(angle)))
           ry = int(sy/2 + 50 * dist * math.sin(math.radians(angle)))

           Rrx[i/8] = rx
           Rry[i/8] = ry

           pygame.display.update()
           pygame.time.wait(30) # Sleeps the gui for 30 milliseonds to share CPU. Share with ROS
           # Could also use pygame.time.delay() instead of time.wait
           screen.fill((0, 20, 0, 0))

           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   exit()

        else:
           #time.sleep(0.001) # Suspending current thread so that
           rate = rospy.Rate(10) # Using instead of time.sleep
           for event in pygame.event.get(): # Closes the gui when we press x red button
               if event.type == pygame.QUIT:
                   pygame.quit()
                   exit()

    rospy.spin()

if __name__ == '__main__':
    main()
