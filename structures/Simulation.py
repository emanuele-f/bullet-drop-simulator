#!/bin/env python2
# -*- coding: utf-8 -*-
#
# Emanuele Faranda                         <black.silver@hotmail.it>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import math

class Simulation(object):
    def __init__(self):
        self._reset()
        
    def _reset(self):
        self.v0 = 0
        self.teta0 = 0
        self.vx0 = 0
        self.vy0 = 0
        self.t0 = 0
        self.tf = 0
        self.x0 = 0
        self.y0 = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self._running = False
        self._initialized = False
        
    def InitFromVelocityAndAngle(self, vmod, teta):
        self._reset()
        self.vx0 = vmod * math.cos(teta)
        self.vy0 = vmod * math.sin(teta)
        self.vx = self.vx0
        self.vy = self.vy0
        self._initialized = True

    def IsRunning(self):
        return self._running

    def Start(self, t0):
        assert self._initialized, "Not initialized"
        self.t0 = t0
        self._running = True
        
    def Stop(self, tf):
        self.tf = tf
        self._running = False
        
    def GetElapsed(self):
        assert not self._running, "Still running"
        assert self.tf > 0, "Not started"
        return self.tf - self.t0

__all__ = ["Simulation"]
