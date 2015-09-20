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

# TODO
#   - beautify and order GUI
#   - Modify unit scale from UI

import time
import wx

from panels import PanelObstaclesCtrl
from panels import PanelSimuParameters
from panels import PanelSimuStatus
from panels import PanelSimulation
from structures import Simulation

from panels.PanelObstaclesCtrl import MY_EVT_OBSTACLES
from panels.PanelSimuParameters import MY_EVT_PARAMETERS, MY_EVT_TARGET

from utils import *
from constraints import *
from formula import *

SIMULATION_TIMER_ID = 1

SIMULATION_STATE_READY = 1
SIMULATION_STATE_RUNNING = 2
SIMULATION_STATE_FINISHED = 3

SIMULATION_ACCELL_ID_ESCAPE = wx.NewId()
SIMULATION_ACCELL_ID_SPACEBAR = wx.NewId()

class BulletSimu(wx.App):
    def __init__(self, **kargs):
        super(BulletSimu, self).__init__(**kargs)
        self.simulation = Simulation()
        self.state = SIMULATION_STATE_READY
        self.obstacles = []

    def OnInit(self):
        self.frame = BulletSimuFrame()

        self.frame.panelStatus.BindStart(self.OnSimulationButton)
        self.frame.panelParams.SetVelocityAndAngle(INITIAL_VELOCITY, ToRadians(INITIAL_ANGLE))
        self.frame.panelSimulation.SetGroundHeight(GROUND_HEIGHT)
        self.frame.panelSimulation.SetComputeMaxRange(INITIAL_VELOCITY)
        self.timer = wx.Timer(self, SIMULATION_TIMER_ID)

        self.Bind(wx.EVT_TIMER, self.OnSimuTick, self.timer)
        self.frame.panelObstacles.Bind(MY_EVT_OBSTACLES, self.OnObstaclesChange)
        self.frame.panelSimulation.Bind(wx.EVT_LEFT_DOWN, self.OnSimuClick)
        self.frame.panelParams.Bind(MY_EVT_PARAMETERS, self.OnSimuParameters)
        self.frame.panelParams.Bind(MY_EVT_TARGET, self.OnSimuTarget)

        # keybinding stuff
        self.Bind(wx.EVT_MENU, self.OnAccelleratorKey, id=SIMULATION_ACCELL_ID_ESCAPE)
        self.Bind(wx.EVT_MENU, self.OnAccelleratorKey, id=SIMULATION_ACCELL_ID_SPACEBAR)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE, SIMULATION_ACCELL_ID_ESCAPE ),
            (wx.ACCEL_NORMAL, wx.WXK_SPACE, SIMULATION_ACCELL_ID_SPACEBAR )
        ])
        self.frame.SetAcceleratorTable(accel_tbl)
        self.LoadInitialObstacles()

        self.frame.Center()
        self.frame.Show()
        return True

    """Read INITIAL_OBSTACLES from constraints.py"""
    def LoadInitialObstacles(self):
        obstacles = []
        for ob in INITIAL_OBSTACLES:
            assert len(ob) == 4, "Obstacle descriptor must be like (x, y, w, h)"
            assert ob[1] == 0, "Only '0' is supported yet"
            for dim in ob:
                assert isinstance(dim, float) or isinstance(dim, int), "A numeric value is required, not %s" % str(dim)
            obstacles.append(ob)
        self.frame.panelObstacles.FromList(obstacles)

    def OnAccelleratorKey(self, event):
        eid = event.GetId()
        if eid == SIMULATION_ACCELL_ID_ESCAPE:
            self.Exit()
        elif eid == SIMULATION_ACCELL_ID_SPACEBAR:
            self._StartButtonLogic()
        else:
            return False
        return True

    def _StartButtonLogic(self):
        curtime = time.time()

        if self.state == SIMULATION_STATE_READY:
            v0_angle = self.frame.panelParams.GetVelocityAndAngle()
            self.simulation.InitFromVelocityAndAngle(v0_angle[0], v0_angle[1])
            self.simulation.Start(curtime)
            self.frame.panelParams.Disable()
            self.frame.panelObstacles.Disable()
            self.frame.panelSimulation.SetSimulation(self.simulation)
            self.timer.Start(1000./SIMULATION_FPS)
            self.frame.panelStatus.SetStatus("Stop")
            self.state = SIMULATION_STATE_RUNNING
        else: # SIMULATION_STATE_RUNNING | SIMULATION_STATE_FINISHED
            self.simulation.Stop(curtime)
            self.frame.panelParams.Enable()
            self.frame.panelObstacles.Enable()
            self.frame.panelSimulation.SetSimulation(False)
            self.timer.Stop()
            self.frame.panelStatus.SetStatus("Start")
            self.state = SIMULATION_STATE_READY

    def OnSimulationButton(self, event):
        self._StartButtonLogic()

    def OnSimuParameters(self, event):
        angle = event.angle
        v0 = event.velocity
        self.frame.panelSimulation.SetAngle(angle)
        self.frame.panelSimulation.SetComputeMaxRange(v0)

    def OnSimuTick(self, event):
        t = time.time() - self.simulation.t0

        x = UniformMotion.x(self.simulation.vx0, t)
        y = UniformAccelleration.x(self.simulation.y0, self.simulation.vy0, GRAVITY_ACCELERATION, t)
        vy = UniformAccelleration.vx(self.simulation.vy0, GRAVITY_ACCELERATION, t)

        # Check bounds
        if x >= (self.frame.panelSimulation.real_width/UNITSIZE):
            finished = True
        elif y <= 0 and vy <= 0:
            finished = True
        elif self.CheckObstaclesCollision(x, y):
            # Collision detected
            finished = True
        else:
            finished = False

        self.simulation.x = x
        self.simulation.y = y
        self.simulation.vy = vy
        self.simulation.track.append((x, y))

        if finished:
            self.simulation.Stop(t)
            self.timer.Stop()
            self.frame.panelStatus.SetStatus("Reset")
            self.state = SIMULATION_STATE_FINISHED

        self.frame.panelSimulation.Refresh()
        self.frame.panelStatus.UpdateData(
            self.simulation.x,
            self.simulation.y,
            self.simulation.vx,
            self.simulation.vy,
            t)

    def OnObstaclesChange(self, event):
        self.obstacles = self.frame.panelObstacles.GetObstaclesRects()
        self.frame.panelSimulation.SetObstacles(self.obstacles)

    def OnSimuClick(self, event):
        if self.state != SIMULATION_STATE_READY:
            return

        virtpoint = self.frame.panelSimulation.PixelsToCoords(event.GetPosition())
        ob = self.CheckObstaclesCollision(*virtpoint)
        if ob:
            # an obstacle was clicked
            self.frame.panelObstacles.SelectByRect(ob)
            return

        if self.frame.panelSimulation.IsTargetLocked():
            self.frame.panelSimulation.SetTargetLocked(False)
        else:
            xtarget = self.frame.panelSimulation.GetTarget()
            if xtarget:
                self._AutoCalculateParamsMedium(xtarget)

    def OnSimuTarget(self, event):
        self.frame.panelSimulation.SetTarget(event.target)
        self.frame.panelSimulation.SetTargetLocked(True)
        self._AutoCalculateParamsSimple(event.target)

    """Determina angolo, mantenendo la velocità inoistata, per arrivare al
       punto stabilito, senza considerare ventuali ostacoli.
    """
    def _AutoCalculateParamsSimple(self, xtarget):
        v0 = self.frame.panelParams.GetVelocityAndAngle()[0]
        teta = BulletDrop.teta_by_v0_xf(v0, xtarget)
        if not teta:
            # Not enough power
            return

        self.frame.panelParams.SetVelocityAndAngle(v0, teta)
        self.frame.panelSimulation.SetAngle(teta)
        self.frame.panelSimulation.SetTargetLocked(True)

    """Determina velocità e angolo per arrivare al punto stabilito evitando
       eventuali ostacoli.

       NB. non supporta coordinate y degli ostacoli diverse da 0
    """
    def _AutoCalculateParamsMedium(self, xtarget):
        result = None
        maxy = None
        y0 = 0

        for ob in self.obstacles:
            # only need to check top left and top right points
            y = ob[3]
            # get [0] and [2]
            for i in range(2):
                x = ob[i*2]

                if x < xtarget:
                    v0_teta = BulletDrop.v0_teta_pass_by(x, y, y0, xtarget)
                    nymax = BulletDrop.max_height(*v0_teta)
                    # higher wins
                    if not maxy or nymax > maxy:
                        result = v0_teta
                        maxy = nymax

        if not result:
            # no influent obstacles where found
            self._AutoCalculateParamsSimple(xtarget)
        else:
            self.frame.panelParams.SetVelocityAndAngle(result[0], result[1])
            self.frame.panelSimulation.SetAngle(result[1])
            self.frame.panelSimulation.SetComputeMaxRange(result[0])
            self.frame.panelSimulation.SetTargetLocked(True)

    def CheckObstaclesCollision(self, x, y):
        for ob in self.obstacles:
            if RectCollidePoint(ob, (x,y)):
                return ob
        return None

class BulletSimuFrame(wx.Frame):
    def __init__(self, **kargs):
        kargs.setdefault("name", "Bullet Drop Simulator")
        super(BulletSimuFrame, self).__init__(None, -1, **kargs)

        self.panelParams = PanelSimuParameters(self)
        self.panelObstacles = PanelObstaclesCtrl(self)
        self.panelStatus = PanelSimuStatus(self)
        self.panelSimulation = PanelSimulation(self, THEME, UNITSIZE)

        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsizer.Add(self.panelStatus, flag=wx.EXPAND)
        subsizer.AddStretchSpacer()
        subsizer.Add(self.panelParams, flag=wx.EXPAND)
        subsizer.AddStretchSpacer()
        subsizer.Add(self.panelObstacles, flag=wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panelSimulation, 1, flag=wx.EXPAND)
        sizer.Add(subsizer, flag=wx.EXPAND)

        self.SetSizerAndFit(sizer)

if __name__ == '__main__':
    simu = BulletSimu()
    simu.MainLoop()

__all__ = ["BulletSimu"]
