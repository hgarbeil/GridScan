from epics import caput, caget, cainfo
from PyQt4 import QtCore
import numpy as np
import os
import subprocess

class MyCAEpics (QtCore.QThread):

    update_position = QtCore.pyqtSignal (int, float)
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.x_start = 0.
        self.y_start = 0.
        self.y_nsteps = 10
        self.x_nsteps = 10
        self.x_inc = 0.01
        self.y_inc = 0.01


    def set_params (self, x0, xrange, xsteps, y0, yrange, ysteps) :
        self.x_start = x0 - xrange
        self.x_inc = xrange * 2 / xsteps
        self.x_nsteps = xsteps

        self.y_start = y0 - yrange
        self.y_inc = yrange * 2 / ysteps
        self.y_nsteps = ysteps

    def get_position (self, mot_num) :
        if (mot_num == 0) :
            return caget('Dera:m1.VAL')
        if (mot_num == 1) :
            return caget('Dera:m2.VAL')

    def move_motor (self, mot_num, loc) :
        if (mot_num == 0) :
            caput('Dera:m1.VAL',loc)
        if (mot_num == 1) :
            caput ('Dera:m2.VAL', loc)

    def set_acquisition_params (self, ofil, atime) :
        self.outpref = ofil
        self.acqtime = atime

    def run (self) :
        xval = caget ('Dera:m1.VAL')
        print xval

        yval = caget ('Dera:m2.VAL')
        print yval

        for i in range (self.y_nsteps) :
            yval = self.y_start + i * self.y_inc
            #caput ('Dera:m2.VAL', yval)
            self.move_motor (1, yval)
            self.update_position.emit (1, yval)
            QtCore.QThread.sleep (2)
            iy = int (yval * 1000)
            for j in range (self.x_nsteps) :
                xval = self.x_start + j * self.x_inc
                #caput ('Dera:m1.VAL', xval)
                self.update_position.emit (0, xval)
                QtCore.QThread.sleep (2)
                self.move_motor (0, xval)
                ix = int (xval * 1000)
                # now do the scan
                filstring = "%s_%05d_%05d.mca"%(self.outpref, ix, iy)
                cmdstring = "C:/Users/przem/workdir/X123/build-X123_cmd-Desktop_Qt_5_9_0_MinGW_32bit-Release/release/X123.exe"
                fullstring = "%s %s %d"%(cmdstring, filstring, self.acqtime)
                #os.system(fullstring)
                news = [cmdstring, filstring, "%d"%(self.acqtime)]
                p = subprocess.Popen (news)
                p.wait()
                print "Scanning... file will be : ", fullstring