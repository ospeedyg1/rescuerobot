#!/usr/bin/env python
# pygame_radar.py takes in information from ultrasound sensor and graphs it
# to a radar display

# Original Source Code:
# https://www.youtube.com/redirect?q=http%3A%2F%2Farkouji.cocolog-nifty.com%2Fblog%2F2016%2F02%2Fraspberry-pi360.html&event=video_description&v=Hqkki-Jl4Y0&redir_token=Mpq6_On6NVQa4GJB1g0-_uQ2zn98MTUxNTYzNDM4MUAxNTE1NTQ3OTgx

# Modified By: Jeovanny Reyes
# Modified On: February 6, 2018

# Subscriber: "HerculesUltrasound_Range" message topic of float 32 data type
# Pubslisher: "" Hercules motor control to stop robot from moving

# Raytheon Radar Guided Rescue Robot
# Cal State LA Senior Design

import math
from sys import exit
import time
import pygame
import numpy as np

import rospy
from sensor_msgs.msg import Range

class RadarDisplay():
    def __init__(self):
        rospy.init_node("radar_display", anonymous=True)
        self.nodename = rospy.get_name()
        rospy.loginfo("%s started" % self.nodename)

        # Initializing and instantiating values
        self.dist = 0
        self.angle = 0
        self.pos = 2
        self.green = (0,200,0) # color
        self.red = (200,0,0) # color
        self.black = (0,0,0) # color
        self.brightred = (255,0,0)
        self.brightgreen = (0,255,0)
        self.smalltext = 0

        # Subscriber
        self.radsip = rospy.Subscriber("HerculesUltrasound_Range",Range, self.distcallback) #Used to be Float32. [Float 32, callback]
        self.plot()

        rospy.spin()

    def distcallback(self,range): # Takes in message "range" as input
        obj_dist = range.range
        self.dist = obj_dist

    def text_object_black(self,text, font):
        self.textSurface = font.render(text, True, self.black)
        return self.textSurface, self.textSurface.get_rect()

    def text_object_green(self,text, font):
        self.textSurface = font.render(text, True, self.green)
        return self.textSurface, self.textSurface.get_rect()

    def arc_inc(self):
        x_pos = 328
        y_pos = 460
        x_length = 150
        y_width = 100
        self.smalltext = pygame.font.Font("freesansbold.ttf",15)

        textSurf1, textRect1 = self.text_object_green("25 cm", self.smalltext)
        textRect1.center = ( (x_pos +(x_length/2)), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf1, textRect1)

        textSurf2, textRect2 = self.text_object_green("50 cm", self.smalltext)
        textRect2.center = ( (x_pos +(x_length/2) - 100), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf2, textRect2)

        textSurf3, textRect3 = self.text_object_green("75 cm", self.smalltext)
        textRect3.center = ( (x_pos +(x_length/2) - 200), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf3, textRect3)

        textSurf4, textRect4 = self.text_object_green("100 cm", self.smalltext)
        textRect4.center = ( (x_pos +(x_length/2) - 300), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf4, textRect4)

        textSurf5, textRect5 = self.text_object_green("25 cm", self.smalltext)
        textRect5.center = ( (x_pos +(x_length/2) + 200), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf5, textRect5)

        textSurf6, textRect6 = self.text_object_green("50 cm", self.smalltext)
        textRect6.center = ( (x_pos +(x_length/2) + 300), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf6, textRect6)

        textSurf7, textRect7 = self.text_object_green("75 cm", self.smalltext)
        textRect7.center = ( (x_pos +(x_length/2) + 400), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf7, textRect7)

        textSurf8, textRect8 = self.text_object_green("100 cm", self.smalltext)
        textRect8.center = ( (x_pos +(x_length/2) + 500), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf8, textRect8)

    def detect_text(self):
        x_pos = 625
        y_pos = 5
        x_length = 150
        y_width = 100
        self.smalltext = pygame.font.Font("freesansbold.ttf",30)
        textSurfstop, textRectstop = self.text_object_green("Object Distance:", self.smalltext)
        textRectstop.center = ( (x_pos +(x_length/2)), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurfstop, textRectstop)

    def stop_button(self): # Function to stop robot from moving
        mouse = pygame.mouse.get_pos() # Movement of mouse.
        click = pygame.mouse.get_pressed() # For button clicked
        self.smalltext = pygame.font.Font("freesansbold.ttf",30)
        x_pos = 50
        y_pos = 35
        x_length = 150
        y_width = 50

        if x_pos+x_length > mouse[0] > x_pos and y_pos+y_width > mouse[1] > y_width: # Hovering over box
            pygame.draw.rect(pygame.display.get_surface(),self.brightred,(x_pos,y_pos,x_length,y_width))
            if click[0] == 1:
                print('Robot has stopped moving')
                # Inserting function that pubslishes command to motors to stop using rospy.Publisher
        else:
            pygame.draw.rect(pygame.display.get_surface(),self.red,(x_pos,y_pos,x_length,y_width))

        textSurf,textRect = self.text_object_black("STOP", self.smalltext) # Insert text on box
        textRect.center = ( (x_pos +(x_length/2)), y_pos+(y_width/2))
        pygame.display.get_surface().blit(textSurf, textRect)

    def plot(self):
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
        Rrx = [0] *512 # Creates an array of 512 zeros. 512 is number of points
        Rry = [0] *512 # Creates an array of 512 zeros

        while (True):
          for i in range(2048): # 4096 covers entire circle and is how many times radius line is drawn
            #angle = i * 5.625/64 #Part of original code. It increments by 5 degrees (0.087890625)
            self.angle = i * (2 * math.pi)/72 #  Line is incremented by 5 degrees (6.283 is 2 pi)

            if i%8==0:
               # Radius is 1000*(4/5) = 800 cm [400 cm]
               pygame.draw.circle(screen, self.green, (sx/self.pos, sy/self.pos), 400, 1) # Outer circle
               #Radius is 1000/5 = 200 cm [100 cm] [100 cm translates to distance of 2
               pygame.draw.circle(screen, self.green, (sx/self.pos, sy/self.pos), 100, 1) #Inner circle. radius was sx/pos/5*1
               # Radius is 1000*(2/5) = 400 cm [200 cm] [200 transaltes to distance of 3]
               pygame.draw.circle(screen, self.green, (sx/self.pos, sy/self.pos), 200, 1) # 2nd Inner circle. radius was sx/pos/5*2
               # Radius is 1000*(3/5) = 600 cm [300 cm]
               pygame.draw.circle(screen, self.green, (sx/self.pos, sy/self.pos), 300, 1) # 3rd Inner Circle. radius was sx/pos/5*3
               pygame.draw.line(screen, self.green, (100, sy/self.pos), (900, sy/self.pos)) # Horizontal Line. Origianlly from (0, sy/pos) to (sx,sy/pos)
               pygame.draw.line(screen, self.green, (sx/self.pos, 100), (sx/self.pos, 900)) # Vertical Line

               self.stop_button()
               self.detect_text()
               self.arc_inc()

               for j in range(512): # 512 is the number of points drawn for entire circle.
                   deg = j * 5.625 / 8 # Increments by 40 degrees
                   radar_deg = deg - self.angle # For first iteration we have 40 - 5 = 35 degrees
                   if radar_deg <=0 :
                      col = int(255*((360+radar_deg)/360)**1.3) # col is color
                      pygame.draw.circle(screen, (0,col,0),(Rrx[j-1],Rry[j-1]),5)
                   else:
                      col = int(255*(radar_deg/360)**1.3)
                      pygame.draw.circle(screen, (0,col,0),(Rrx[j-1],Rry[j-1]),5)

               if self.dist < 0:
                   self.dist = math.fabs(self.dist) # Returns the absolute value of distance

               dx = sx/2 + sx/2 * math.cos(math.radians(self.angle))
               dy = sy/2 + sx/2 * math.sin(math.radians(self.angle))
               # anti aliasing line: To make line smooth
               pygame.draw.aaline(screen, (0, 200, 0), (sx/2, sy/2), (dx, dy),5)

               rx = int(sx/2 + 50 * self.dist * math.cos(math.radians(self.angle)))
               ry = int(sy/2 + 50 * self.dist * math.sin(math.radians(self.angle)))

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


if __name__ == '__main__':
    RadarDisplay()
