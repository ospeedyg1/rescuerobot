#!/usr/bin/env python
# RADAR DISPLAY GUI/widget

# Created By: Jeovanny Reyes
# Created on: November 8, 2017
# Updated on: November

# Description: Taking Sensor information and outputing to
#              a radar sweep

# Raytheon Radar Guided Rescue Robot

# todo: Import data into Gui
#       Create line that follows sweep of Radar
#       Import to ROS' rqt as plugin (may or may not need)

import rospy
from std_msgs.msg import String # std_msgs could be sensor_msgs or range_msg or pub_range

import sys, random, time, threading, Queue
from PyQt4 import QtGui, QtCore


class RadarDisplay(QtGui.QMainWindow):

    def __init__(self):
        super(RadarDisplay, self).__init__()
        self.setGeometry( 50, 50, 1100, 750) # Sets dimension of GUI window
        self.setWindowTitle("Radar Display")
        self.emerg()
        self.setStyleSheet("background-color: black;")

    def paintEvent(self,event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawArc(qp)
        self.drawText(qp)
        self.robotshape(qp)
        qp.end()

    def emerg(self): # Emergency Stop Button
        btn = QtGui.QPushButton("STOP",self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.setFont(QtGui.QFont('Decorative',24))
        btn.setStyleSheet("QPushButton {background-color: red; color:black;}")
        btn.resize(150, 70)
        btn.move(100,640)

        # Insert function to stop robot from moving

        self.show()

    def drawLines(self, qp):
        linepen = QtGui.QPen(QtCore.Qt.green, 6, QtCore.Qt.SolidLine)
        qp.setPen(linepen)

        qp.drawLine(100, 599, 1010, 599) # Draws X-Axis First (Horizontal), then:

        qp.drawLine(555, 79, 555, 599) # 90 degree line: (X1,Y1) and (X2,Y2)
        qp.drawLine(555, 599, 959, 375) # 30 degree line
        qp.drawLine(555, 599, 815, 175) # 60 degree line
        qp.drawLine(555, 599, 293, 179) # 120 degree line
        qp.drawLine(555, 599, 149, 365 ) # 150 degree line

    def robotshape(self,qp):
        linepen = QtGui.QPen(QtCore.Qt.yellow, 6, QtCore.Qt.SolidLine)
        qp.setPen(linepen)

        qp.drawLine(505, 620, 505, 720) # Left side of Robot
        qp.drawLine(605, 620, 605, 720) # Right side of Robot

        qp.drawLine(505,720, 605, 720) # Back of Robot

        #qp.drawEllipse(527, 610, 30, 30) # Transmitter (Left circle)
        qp.drawRect(530, 610, 20, 15)
        #qp.drawEllipse(557, 610, 30, 30) # Receiver (Right circle)
        qp.drawRect(560, 610, 20, 15)

        qp.drawRect(480, 625, 25, 35) # Front Left Wheel
        qp.drawRect(605, 625, 25, 35) # Front Right Wheel

        qp.drawRect(480, 680, 25, 35) # Back Left Wheel
        qp.drawRect(605, 680, 25, 35) # Back Right Wheel

        qp.drawLine(505, 620, 530, 620) # Left top
        qp.drawLine(585, 620, 605, 620) # Right top

    def drawArc(self,qp):
        arcpen = QtGui.QPen(QtCore.Qt.green, 4, QtCore.Qt.SolidLine)
        qp.setPen(arcpen)

        rect1 = QtCore.QRect(7, 50, 900, 1100)
        rect2 = QtCore.QRect(56,45, 345, 867)

        startAngle = 0;
        spandAngle = 180*16;

        qp.drawArc(99, 80, 911, 1030, startAngle, spandAngle) # Outside Arc
        qp.drawArc(190, 165, 726, 880, startAngle, spandAngle)
        qp.drawArc(285, 280 , 537, 630, startAngle, spandAngle)
        qp.drawArc(380, 405, 360, 380 ,startAngle, spandAngle) # Inside Arc

    def drawText(self, qp):
        textpen = QtGui.QPen(QtCore.Qt.yellow, 10, QtCore.Qt.SolidLine)
        qp.setPen(textpen)
        qp.setFont(QtGui.QFont('Decorative',17))

        qp.drawText(682, 623, "25 cm") # Right Side of Graph
        qp.drawText(782, 623, "50 cm")
        qp.drawText(882, 623, "75 cm")
        qp.drawText(982, 623, "100 cm")

        qp.drawText(352, 623, "25 cm") # Left Side of Graph
        qp.drawText(252, 623, "50 cm")
        qp.drawText(152, 623, "75 cm")
        qp.drawText(52, 623, "100 cm")

        qp.drawText(979, 385, "60 deg") # Was originally 30 degrees
        qp.drawText(820, 155, "30 deg") # Was originally 60 degrees
        qp.drawText(518, 50, "0 deg") # Was originally 90 degrees
        qp.drawText(198, 145, "-30 deg") # Was originally 120 degrees
        qp.drawText(42 , 375, "-60 deg") # Was originally 150 degrees

        qp.drawText(692,680,"Object Distance:")
        #qp.drawText(692,680,"Object Distance:") # Displays the distance calculated

# Setting the listener node up
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("HerculesUltrasound", String, callback) # topic pubslishes numbers not strings
    # spin () simply keeps python from exiting until this node is stopped
    rospy.spin()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = RadarDisplay()
    app.exec_()

run()
