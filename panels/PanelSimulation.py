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

class PanelSimulation(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimulation, self).__init__(parent, **kargs)
        
        self._simulating = False
        
        self.SetSizeHints(600,400,600,400)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(0, 0, 505, 505)
        
    def SetIsSimulating(self, simulating):
        if simulating:
            self._simulating = True
            self.Refresh()
        else:
            self._simulating = False
            self.Refresh()

__all__ = ["PanelSimulation"]
