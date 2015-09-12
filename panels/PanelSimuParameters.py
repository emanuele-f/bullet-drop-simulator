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
        ts = wx.GridSizer(rows=4, cols=2)
        ts.Add(wx.StaticText(self, label="angolo"))
        ts.Add(self.angle)
        ts.Add(wx.StaticText(self, label="velocità"))
        ts.Add(self.v0)
        ts.Add(wx.StaticText(self, label="gittata corrente"))
        ts.Add(self.curRange)
        ts.Add(wx.StaticText(self, label="gittata massima"))
        ts.Add(self.maxRange)
        
        # Outer box
        box = wx.StaticBox(self, label="Parametri di simulazione")
        bs = wx.StaticBoxSizer(box)
        bs.Add(ts)
        
        self.SetSizer(bs)

__all__ = ["PanelSimuParameters"]
