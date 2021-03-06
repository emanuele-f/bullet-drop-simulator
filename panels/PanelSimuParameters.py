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
from formula import BulletDrop
from utils import ToDegrees, ToRadians
from constraints import Measures

_MyEventSimuParameters, MY_EVT_PARAMETERS = wx.lib.newevent.NewEvent()
_MyEventSimuSetTarget, MY_EVT_TARGET = wx.lib.newevent.NewEvent()

class PanelSimuParameters(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimuParameters, self).__init__(parent, **kargs)

        self.tc_angle = wx.TextCtrl(self)
        self.tc_v0 = wx.TextCtrl(self)
        self.tc_curRange = wx.TextCtrl(self)
        self.tc_maxRange = wx.TextCtrl(self)
        self._angle_radians = 0
        self._v0 = 0

        self.tc_angle.Bind(wx.EVT_TEXT, self.OnAngleParameter)
        self.tc_v0.Bind(wx.EVT_TEXT, self.OnVelocityParameter)
        self.tc_curRange.Bind(wx.EVT_TEXT, self.OnCurrentRange)
        self.tc_maxRange.Bind(wx.EVT_TEXT, self.OnMaxRange)

        # Table sizer
        ts = wx.GridSizer(rows=4, cols=3, hgap=Measures.PANEL_INNER_PADDING)
        ts.Add(wx.StaticText(self, label="angolo"))
        ts.Add(self.tc_angle)
        ts.Add(wx.StaticText(self, label="gradi"))
        ts.Add(wx.StaticText(self, label=u"velocità"))
        ts.Add(self.tc_v0)
        ts.Add(wx.StaticText(self, label="u/s"))
        ts.Add(wx.StaticText(self, label="gittata corrente"))
        ts.Add(self.tc_curRange)
        ts.Add(wx.StaticText(self, label="u"))
        ts.Add(wx.StaticText(self, label="gittata massima"))
        ts.Add(self.tc_maxRange)
        ts.Add(wx.StaticText(self, label="u"))

        # Outer box
        box = wx.StaticBox(self, label="Parametri di simulazione")
        bs = wx.StaticBoxSizer(box)
        bs.Add(ts, flag=wx.ALL, border=Measures.PANEL_BOX_PADDING)

        self.SetSizer(bs)

    def _SetVelocityAndAngleNotRange(self, v0, angle):
        self._angle_radians = angle
        self._v0 = v0
        self.tc_v0.ChangeValue("%.1f" % v0)
        self.tc_angle.ChangeValue("%.2f" % ToDegrees(angle))

    """avoids disturbing text changes"""
    def _ChangeTextIfDifferent(self, tc, fmt, newv):
        try:
            curval = fmt % float(tc.GetValue())
        except ValueError:
            curval = None

        newval = fmt % newv
        if curval != newval:
            tc.ChangeValue(newval)

    """angle: radians"""
    def SetVelocityAndAngle(self, v0, angle):
        self._SetVelocityAndAngleNotRange(v0, angle)
        self._ChangeTextIfDifferent(self.tc_maxRange, "%.1f", BulletDrop.max_distance(v0))
        self._ChangeTextIfDifferent(self.tc_curRange, "%.1f", BulletDrop.xf_by_v0_teta(v0, angle))

    def GetVelocityAndAngle(self):
        return (self._v0, self._angle_radians)

    def _NotifyParametersChange(self):
        evt = _MyEventSimuParameters(angle=self._angle_radians, velocity=self._v0)
        wx.PostEvent(self, evt)

    def OnAngleParameter(self, event):
        try:
            angle = float(self.tc_angle.GetValue())
        except ValueError:
            return

        self._angle_radians = ToRadians(angle)
        self._NotifyParametersChange()

    def OnVelocityParameter(self, event):
        try:
            velocity = float(self.tc_v0.GetValue())
        except ValueError:
            return

        self._v0 = velocity
        self._NotifyParametersChange()

    def OnCurrentRange(self, event):
        try:
            xt = float(self.tc_curRange.GetValue())
        except ValueError:
            return

        # not enough power
        if xt > BulletDrop.max_distance(self._v0):
            return

        evt = _MyEventSimuSetTarget(target=xt)
        wx.PostEvent(self, evt)

    def OnMaxRange(self, event):
        try:
            xf = float(self.tc_maxRange.GetValue())
        except ValueError:
            return

        v0 = BulletDrop.v0_by_distance(xf)
        self._SetVelocityAndAngleNotRange(v0, self._angle_radians)
        self._NotifyParametersChange()

__all__ = ["PanelSimuParameters", "MY_EVT_PARAMETERS"]
