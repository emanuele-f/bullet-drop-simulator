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
import wx

class PanelSimulation(wx.Panel):
    def __init__(self, parent, theme, unitsize, **kargs):
        super(PanelSimulation, self).__init__(parent, **kargs)
        
        self._simu = None
        self._angle = math.pi/4
        self._height = 400
        self._width = 600
        self._ground_y = 0
        self._theme = theme
        self._units = unitsize
        
        # Set exactly this size
        self.SetSizeHints(self._width,self._height,self._width,self._height)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):
        if self._simu:
            self.OnPaintDuringSimulation()
        else:
            self.OnPaintDuringSetup()
            
    def OnPaintDuringSimulation(self):
        dc = wx.PaintDC(self)
        dc.Clear()
        self._DrawGround(dc)
        
    def OnPaintDuringSetup(self):
        dc = wx.PaintDC(self)
        dc.Clear()
        self._DrawGround(dc)
        self._DrawRamp(dc)
        
    def _DrawGround(self, dc):
        dc.SetPen(wx.Pen(self._theme["ground"], self._theme["line"]))
        dc.DrawLine(0, self._height-self._ground_y, self._width, self._height-self._ground_y)
        
        dc.SetPen(wx.Pen(self._theme["units"], self._theme["line"]))
        for i in range(0, self._width):
            dc.DrawLine(self._units*i, self._height-self._ground_y-10, self._units*i, self._height)
            
    def _DrawRamp(self, dc):
        w = (self._height-self._ground_y) / math.tan(self._angle)
        dc.SetPen(wx.Pen(self._theme["ramp"], self._theme["line"]))
        dc.DrawLine(0, self._height-self._ground_y, w, 0)
        
    def SetSimulation(self, simulation):
        if simulation:
            self._simu = simulation
        else:
            self._simu = None
            
    def SetAngle(self, angle):
        assert not self._simu, "Cannot set angle during simulation"
        if angle > 0 and angle < 90:
            self._angle = angle
            self.Refresh()
            
    def SetGroundHeight(self, height):
        self._ground_y = height

__all__ = ["PanelSimulation"]
