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

class PanelSimuParameters(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimuParameters, self).__init__(parent, **kargs)
        
        self.angle = wx.TextCtrl(self)
        self.v0 = wx.TextCtrl(self)
        self.curRange = wx.TextCtrl(self)
        self.maxRange = wx.TextCtrl(self)
        self.maxRange.SetEditable(False)
        
        # Table sizer
        ts = wx.GridSizer(rows=4, cols=3)
        ts.Add(wx.StaticText(self, label="angolo"))
        ts.Add(self.angle)
        ts.Add(wx.StaticText(self, label="gradi"))
        ts.Add(wx.StaticText(self, label="velocità"))
        ts.Add(self.v0)
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
        
    def SetVelocityAndAngle(self, v0, angle):
        self.v0.SetValue("%.1f" % v0)
        self.angle.SetValue("%.2f" % angle)
        
    def GetVelocityAndAngle(self):
        v0 = float(self.v0.GetValue())
        teta = float(self.angle.GetValue())
        return (v0, teta)
        
    def BindAngle(self, func):
        self.angle.Bind(wx.EVT_TEXT, func)

__all__ = ["PanelSimuParameters"]
