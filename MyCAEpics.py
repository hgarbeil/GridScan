from epics import caput, caget, cainfo
from PyQt4 import QtCore
import numpy as np

class MyCAEpics (QtCore.QThread):

    update_position = QtCore.pyqtSignal (int, float)
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.x_start = 0.
        self.y_start = 0.
        self.x_stop = 0.
        self.y_stop = 0.

        self.x_cent = 0.
        self.y_cent =0.
        self.x_inc = 0.01
        self.y_inc = 0.01


    def set_params (self, x0, xcent, xinc, y0, ycent, yinc) :
        self.x_start = x0
        self.x_cent = xcent
        self.x_inc = xinc
        self.y_start = y0
        self.y_cent = ycent
        self.y_inc = yinc

        self.x_stop = 2. * self.x_cent - self.x_start
        self.y_stop = 2. * self.y_cent - self.y_start


    def run (self) :
        xval = caget ('Dera:m1.VAL')
        print xval

        yval = caget ('Dera:m2.VAL')
        print yval

        print self.y_start,self.y_stop, self.y_inc
        for iy in np.arange (self.y_start, self.y_stop, self.y_inc) :
            caput ('Dera:m2.VAL', iy)
            print iy
            self.update_position.emit (1, iy)
            QtCore.QThread.sleep (1)

            for ix in np.arange (self.x_start, self.x_stop, self.x_inc) :
                caput ('Dera:m1.VAL', ix)
                self.update_position.emit (0, ix)
                QtCore.QThread.sleep (1)

                # now do the scan
