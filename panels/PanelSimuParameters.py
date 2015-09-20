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

import wx
import wx.lib.newevent
from utils import ToDegrees, ToRadians

_MyEventSimuParameters, MY_EVT_PARAMETERS = wx.lib.newevent.NewEvent()

class PanelSimuParameters(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimuParameters, self).__init__(parent, **kargs)

        self.tc_angle = wx.TextCtrl(self)
        self.tc_v0 = wx.TextCtrl(self)
        self.curRange = wx.TextCtrl(self)
        self.maxRange = wx.TextCtrl(self)
        self.maxRange.SetEditable(False)
        self._angle_radians = 0
        self._v0 = 0

        self.tc_angle.Bind(wx.EVT_TEXT, self.OnAngleParameter)
        self.tc_v0.Bind(wx.EVT_TEXT, self.OnVelocityParameter)

        # Table sizer
        ts = wx.GridSizer(rows=4, cols=3)
        ts.Add(wx.StaticText(self, label="angolo"))
        ts.Add(self.tc_angle)
        ts.Add(wx.StaticText(self, label="gradi"))
        ts.Add(wx.StaticText(self, label="velocità"))
        ts.Add(self.tc_v0)
        ts.Add(wx.StaticText(self, label="u/s"))
        ts.Add(wx.StaticText(self, label="gittata corrente"))
        ts.Add(self.curRange)
        ts.Add(wx.StaticText(self, label="u"))
        ts.Add(wx.StaticText(self, label="gittata massima"))
        ts.Add(self.maxRange)
        ts.Add(wx.StaticText(self, label="u"))

        # Outer box
        box = wx.StaticBox(self, label="Parametri di simulazione")
        bs = wx.StaticBoxSizer(box)
        bs.Add(ts)

        self.SetSizer(bs)

    """angle: radians"""
    def SetVelocityAndAngle(self, v0, angle):
        self._angle_radians = angle
        self._v0 = v0
        self.tc_v0.SetValue("%.1f" % v0)
        self.tc_angle.SetValue("%.2f" % ToDegrees(angle))

    def GetVelocityAndAngle(self):
        return (self._v0, self._angle_radians)

    def _NotifyParametersChange(self):
        evt = _MyEventSimuParameters(angle=self._angle_radians, velocity=self._v0)
        wx.PostEvent(self, evt)

    def OnAngleParameter(self, event):
        try:
            angle = float(self.tc_angle.GetValue())
        except ValueError:
            pass
        else:
            self._angle_radians = ToRadians(angle)
            self._NotifyParametersChange()

    def OnVelocityParameter(self, event):
        try:
            velocity = float(self.tc_v0.GetValue())
        except ValueError:
            pass
        else:
            self._v0 = velocity
            self._NotifyParametersChange()

__all__ = ["PanelSimuParameters", "MY_EVT_PARAMETERS"]
