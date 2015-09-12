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

from panels import PanelObstaclesCtrl
from panels import PanelSimuParameters
from panels import PanelSimuStatus
from panels import PanelSimulation

class BulletSimu(wx.App):
    def __init__(self, **kargs):
        super(BulletSimu, self).__init__(**kargs)
        self.simulating = False
        
    def OnInit(self):
        self.frame = BulletSimuFrame()
        
        self.frame.panelStatus.BindStart(self.OnSimulationButton)
        
        self.frame.Center()
        self.frame.Show()
        return True
        
    def OnSimulationButton(self, event):
        button = event.GetEventObject()
        if not self.simulating:
            self.simulating = True
            button.SetLabel("Stop")
        else:
            self.simulating = False
            button.SetLabel("Start")
        
class BulletSimuFrame(wx.Frame):
    def __init__(self, **kargs):
        kargs.setdefault("name", "Bullet Drop Simulator")
        super(BulletSimuFrame, self).__init__(None, -1, **kargs)
        
        self.panelParams = PanelSimuParameters(self)
        self.panelObstacles = PanelObstaclesCtrl(self)
        self.panelStatus = PanelSimuStatus(self)
        self.panelSimulation = PanelSimulation(self)
    
        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5)
        sizer.Add(self.panelSimulation)
        sizer.Add(self.panelStatus, flag=wx.EXPAND)
        sizer.Add(self.panelParams, flag=wx.EXPAND)
        sizer.Add(self.panelObstacles, flag=wx.EXPAND)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        self.SetSizerAndFit(sizer)

if __name__ == '__main__':
    simu = BulletSimu()
    simu.MainLoop()
