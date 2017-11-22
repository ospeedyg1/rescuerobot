#!/usr/bin/env python
# RADAR DISPLAY GUI/widget

# Created By: Jeovanny Reyes
# Created on: November 8, 2017

# Description: Taking Sensor information and outputing to
#              a radar sweep

# Raytheon Radar Guided Rescue Robot

# todo: Import data into Gui
#       Create line that follows sweep of Radar
#       Import to ROS' rqt as plugin


import sys, random, time, threading, Queue
from PyQt4 import QtGui, QtCore

SERIALPORTLIN = '/dev/ttyACM0'

class RadarDisplay(QtGui.QMainWindow):

    def __init__(self):
        super(RadarDisplay, self).__init__()
        self.setGeometry( 50, 50, 1100, 750) # Sets dimension of GUI window
        self.setWindowTitle("Radar Display")
        self.show()
        self.setStyleSheet("background-color: black;")

    def paintEvent(self,event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawArc(qp)
        self.drawText(qp)
        qp.end()

    def drawLines(self, qp):
        linepen = QtGui.QPen(QtCore.Qt.green, 6, QtCore.Qt.SolidLine)
        qp.setPen(linepen)

        qp.drawLine(100, 599, 1010, 599) # Draws X-Axis First (Horizontal), then:

        qp.drawLine(555, 79, 555, 599) # 90 degree line: (X1,Y1) and (X2,Y2)
        qp.drawLine(555, 599, 959, 375) # 30 degree line
        qp.drawLine(555, 599, 815, 175) # 60 degree line
        qp.drawLine(555, 599, 293, 179) # 120 degree line
        qp.drawLine(555, 599, 149, 365 ) # 150 degree line

    def drawArc(self,qp):
        arcpen = QtGui.QPen(QtCore.Qt.green, 4, QtCore.Qt.SolidLine)
        qp.setPen(arcpen)

        rect1 = QtCore.QRect(7, 50, 900, 1100)
        rect2 = QtCore.QRect(56,45, 345, 867)

        startAngle = 0;
        spandAngle = 180*16;
        """
        Draws Arcs from outside to inside (4 arcs)
        """
        qp.drawArc(99, 80, 911, 1030, startAngle, spandAngle)
        qp.drawArc(190, 165, 726, 880, startAngle, spandAngle)
        qp.drawArc(285, 280 , 537, 630, startAngle, spandAngle)
        qp.drawArc(380, 405, 360, 380 ,startAngle, spandAngle)

    def drawText(self, qp):
        textpen = QtGui.QPen(QtCore.Qt.blue, 4, QtCore.Qt.SolidLine)
        qp.setPen(textpen)
        qp.setFont(QtGui.QFont('Decorative',17))

        qp.drawText(682, 623, "15 cm") # Right Side of Graph
        qp.drawText(782, 623, "30 cm")
        qp.drawText(882, 623, "45 cm")
        qp.drawText(982, 623, "60 cm")

        qp.drawText(352, 623, "15 cm") # Left Side of Graph
        qp.drawText(252, 623, "30 cm")
        qp.drawText(152, 623, "45 cm")
        qp.drawText(52, 623, "60 cm")

        qp.drawText(979, 385, "30 deg")
        qp.drawText(820, 155, "60 deg")
        qp.drawText(518, 50, "90 deg")
        qp.drawText(198, 145, "120 deg")
        qp.drawText(42, 375, "150 deg")

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = RadarDisplay()
    app.exec_()

run()
