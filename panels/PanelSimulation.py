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
from formula import BulletDrop

class PanelSimulation(wx.Panel):
    def __init__(self, parent, theme, unitsize, **kargs):
        super(PanelSimulation, self).__init__(parent, **kargs)

        self._simu = None
        self._angle = math.pi/4
        self.real_height = 400
        self.real_width = 600
        self._ground_y = 0
        self._theme = theme
        self._units = unitsize
        self._obrects = []
        self._target_x = None
        self._target_locked = False
        self.SetBackgroundColour(self._theme['background'])
        self._max_range = 0

        # Set exactly this size
        self.SetSizeHints(self.real_width,self.real_height,self.real_width,self.real_height)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def CoordsToPixels(self, (x, y)):
        return (int(x * self._units), self.real_height - (self._ground_y + int(y * self._units)))

    def PixelsToCoords(self, (x, y)):
        return (x * 1. / self._units, (self.real_height - self._ground_y - y) * 1. / self._units)

    def OnPaint(self, event):
        if self._simu:
            self.OnPaintDuringSimulation()
        else:
            self.OnPaintDuringSetup()

    def OnMotion(self, event):
        if not self._target_locked:
            x = event.GetX()
            if x <= self._max_range:
                self._target_x = x
                self.Refresh()

    def OnLeaveWindow(self, event):
        if not self._target_locked:
            self._target_x = None
            self.Refresh()

    def GetTarget(self):
        if not self._target_x:
            return None
        return self.PixelsToCoords((self._target_x, 0))[0]

    def SetTargetLocked(self, locked):
        if locked:
            self._target_locked = True
        else:
            self._target_locked = False

    def IsTargetLocked(self):
        return self._target_locked

    def OnPaintDuringSimulation(self):
        dc = wx.PaintDC(self)
        dc.Clear()
        self._DrawGround(dc)
        self._DrawObstacles(dc)
        self._DrawMarker(dc, self._theme["maxrange"], self._max_range)
        self._DrawBall(dc)

    def OnPaintDuringSetup(self):
        dc = wx.PaintDC(self)
        dc.Clear()
        self._DrawGround(dc)
        self._DrawObstacles(dc)
        self._DrawRamp(dc)
        self._DrawMarker(dc, self._theme["maxrange"], self._max_range,)
        if self._target_x:
            self._DrawMarker(dc, self._theme["target"], self._target_x)

    def _DrawGround(self, dc):
        dc.SetPen(wx.Pen(self._theme["ground"], self._theme["line"]))
        dc.DrawLine(0, self.real_height-self._ground_y, self.real_width, self.real_height-self._ground_y)

        dc.SetPen(wx.Pen(self._theme["units"], self._theme["line"]))
        for i in range(0, self.real_width):
            dc.DrawLine(self._units*i, self.real_height-self._ground_y-10, self._units*i, self.real_height)

    def _DrawRamp(self, dc):
        w = (self.real_height-self._ground_y) / math.tan(self._angle)
        dc.SetPen(wx.Pen(self._theme["ramp"], self._theme["line"]))
        dc.DrawLine(0, self.real_height-self._ground_y, w, 0)

    def _DrawBall(self, dc):
        x,y = self.CoordsToPixels((self._simu.x, self._simu.y))

        dc.SetPen(wx.Pen(self._theme["ball"], self._theme["line"]))
        if len(self._simu.track) > 1:
            real_points = map(self.CoordsToPixels, self._simu.track)
            dc.DrawLines(real_points)
        dc.DrawCircle(x, y, self._theme["ball_ray"])

    def _DrawObstacles(self, dc):
        dc.SetPen(wx.Pen(self._theme["obstacles"], self._theme["line"]))

        for ob in self._obrects:
            xi, yi = self.CoordsToPixels((ob[0], ob[1]))
            xf, yf = self.CoordsToPixels((ob[2], ob[3]))
            dc.DrawRectangle(xi, yi, xf-xi, yf-yi)

    def _DrawMarker(self, dc, color, x):
        h = self.real_height - self._ground_y
        dc.SetPen(wx.Pen(color, self._theme["target_width"]))
        dc.DrawLine(x, h-self._theme["target_height"], x, h)

    def SetSimulation(self, simulation):
        if simulation:
            self._simu = simulation
        else:
            self._simu = None
        self.Refresh()

    def SetAngle(self, angle):
        assert not self._simu, "Cannot set angle during simulation"
        if angle > 0 and angle < math.pi/2.:
            self._angle = angle
            self.Refresh()

    def SetGroundHeight(self, height):
        self._ground_y = height

    def SetObstacles(self, obrects):
        self._obrects = obrects
        self.Refresh()

    def SetComputeMaxRange(self, v0, teta):
        mdist = BulletDrop.max_distance(v0, teta)
        self._max_range = self.CoordsToPixels((mdist, 0))[0]
        self.Refresh()

__all__ = ["PanelSimulation"]
