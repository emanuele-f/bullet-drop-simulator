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

class PanelSimuStatus(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimuStatus, self).__init__(parent, **kargs)
        
        self.startBt = wx.Button(self, label="Start")
        self.vx = wx.StaticText(self)
        self.vy = wx.StaticText(self)
        self.x = wx.StaticText(self)
        self.y = wx.StaticText(self)
        self.t = wx.StaticText(self)
        
        # Table sizer
        ts = wx.GridSizer(rows=5, cols=2)
        ts.Add(wx.StaticText(self, label="Velocità x"))
        ts.Add(self.vx)
        ts.Add(wx.StaticText(self, label="Velocità y"))
        ts.Add(self.vy)
        ts.Add(wx.StaticText(self, label="X"))
        ts.Add(self.x)
        ts.Add(wx.StaticText(self, label="Y"))
        ts.Add(self.y)
        ts.Add(wx.StaticText(self, label="Tempo"))
        ts.Add(self.t)

        # Main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.startBt)
        sizer.Add(ts)
        
        # Outer box
        box = wx.StaticBox(self, label="Stato simulazione")
        bs = wx.StaticBoxSizer(box)
        bs.Add(sizer)
        
        self.SetSizer(bs)

__all__ = ["PanelSimuStatus"]