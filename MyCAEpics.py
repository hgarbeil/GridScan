from epics import caput, caget, cainfo
from PyQt4 import QThread

class MyCAEpics (Thread):


    def __init__(self):
        Thread.__init__(self)
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
        self.y_stop = 2. * self.y_stop - self.y_stop


    def