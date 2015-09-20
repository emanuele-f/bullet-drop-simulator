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

KEY_DELIMITER = "-"
_MyEventObstacles, MY_EVT_OBSTACLES = wx.lib.newevent.NewEvent()

class PanelObstaclesCtrl(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelObstaclesCtrl, self).__init__(parent, **kargs)

        self.selector = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.bt_delete = wx.Button(self, label="Elimina")
        self.bt_add = wx.Button(self, label="Aggiungi")
        self.tc_x = wx.TextCtrl(self)
        self.tc_y = wx.TextCtrl(self)
        self.tc_y.Disable()
        self.tc_width = wx.TextCtrl(self)
        self.tc_height = wx.TextCtrl(self)
        self._obstacles = {}
        self._obi = 0
        self._selection = -1

        self.bt_add.Bind(wx.EVT_BUTTON, self.OnObstacleAdd)
        self.bt_delete.Bind(wx.EVT_BUTTON, self.OnObstacleDelete)
        self.selector.Bind(wx.EVT_COMBOBOX, self.OnSelection)
        self.tc_x.Bind(wx.EVT_TEXT, lambda ev: self._ObPropSetter(0))
        self.tc_y.Bind(wx.EVT_TEXT, lambda ev: self._ObPropSetter(1))
        self.tc_width.Bind(wx.EVT_TEXT, lambda ev: self._ObPropSetter(2))
        self.tc_height.Bind(wx.EVT_TEXT, lambda ev: self._ObPropSetter(3))
        self._SetControlsEnabled(False)

        # Horizontal sizer
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(self.selector)
        hs.Add(self.bt_delete)
        hs.Add(self.bt_add)

        # Table sizer
        ts = wx.GridSizer(rows=4, cols=2)
        ts.Add(wx.StaticText(self, label="x"))
        ts.Add(self.tc_x)
        ts.Add(wx.StaticText(self, label="y"))
        ts.Add(self.tc_y)
        ts.Add(wx.StaticText(self, label="larghezza"))
        ts.Add(self.tc_width)
        ts.Add(wx.StaticText(self, label="altezza"))
        ts.Add(self.tc_height)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hs)
        sizer.Add(ts)

        # Outer box
        box = wx.StaticBox(self, label="Gestione ostacoli")
        bs = wx.StaticBoxSizer(box)
        bs.Add(sizer)

        self.SetSizer(bs)

    def _SetControlsEnabled(self, enabled):
        if enabled:
            self.bt_delete.Enable()
            self.tc_x.Enable()
            #~ self.tc_y.Enable()
            self.tc_width.Enable()
            self.tc_height.Enable()
        else:
            self.bt_delete.Disable()
            self.tc_x.Disable()
            self.tc_y.Disable()
            self.tc_width.Disable()
            self.tc_height.Disable()

    def _GetSelectedObstacleId(self):
        val = self.selector.GetValue()
        i = val.find(KEY_DELIMITER)
        if i < 0:
            return -1
        oid = int(val[i+len(KEY_DELIMITER):])
        return oid

    def _ObPropSetter(self, propid):
        assert self._selection != -1, "No selection!"
        ob = self._obstacles[self._selection]

        try:
            if propid == 0:
                ob[0] = float(self.tc_x.GetValue())
            elif propid == 1:
                ob[1] = float(self.tc_y.GetValue())
            elif propid == 2:
                ob[2] = float(self.tc_width.GetValue())
            elif propid == 3:
                ob[3] = float(self.tc_height.GetValue())
        except ValueError:
            pass
        else:
            self._NotifyObstaclesChange()

    def _NotifyObstaclesChange(self):
        evt = _MyEventObstacles()
        wx.PostEvent(self, evt)

    """Select an obstacle programmatically."""
    def _SelectorOn(self, oid):
        if oid == -1:
            self.selector.SetSelection(0)
        else:
            idx = self.selector.FindString("obstacle%s%d" % (KEY_DELIMITER, oid))
            if idx != -1:
                self.selector.SetSelection(idx)
        self._ObstacleSelection(oid)

    """Update combobox selection list."""
    def _UpdateSelector(self, restore=True):
        curval = self.selector.GetValue()
        cursel = self._GetSelectedObstacleId()

        self.selector.Clear()
        self.selector.Append("")
        for key, ob in self._obstacles.items():
            self.selector.Append("obstacle%s%d" % (KEY_DELIMITER, key))

        if restore and curval:
            if self.selector.FindString(curval) == -1:
                # it was deleted
                self._SelectorOn(-1)
            else:
                # restore selection
                self._SelectorOn(cursel)

        self._NotifyObstaclesChange()

    """Trigger information show for given obstacle."""
    def _ObstacleSelection(self, obi):
        if obi == -1:
            self._selection = -1
            self._SetControlsEnabled(False)
        else:
            self._selection = obi
            self._SetControlsEnabled(True)
            # show data set
            ob = self._obstacles[obi]
            self.tc_x.SetValue(str(ob[0]))
            self.tc_y.SetValue(str(ob[1]))
            self.tc_width.SetValue(str(ob[2]))
            self.tc_height.SetValue(str(ob[3]))

    def OnObstacleAdd(self, event):
        obi = self._obi
        self._obi += 1

        self._obstacles[obi] = [4,0,2,2]
        self._UpdateSelector(restore=False)
        self._SelectorOn(obi)

    def OnObstacleDelete(self, event):
        sel = self._GetSelectedObstacleId()
        if sel != -1:
            self._obstacles.pop(sel)
            self._UpdateSelector()

    def OnSelection(self, event):
        self._ObstacleSelection(self._GetSelectedObstacleId())

    """Builds rects like (xi, yi, xf, yi) from obstacles."""
    def GetObstaclesRects(self):
        l = []
        for ob in self._obstacles.values():
            l.append((ob[0], ob[1], ob[0]+ob[2], ob[1]+ob[3]))
        return l

    """Sets current selection by rect spec"""
    def SelectByRect(self, rect):
        rect = [rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1]]
        try:
            key = (key for key,value in self._obstacles.items() if value==rect).next()
        except StopIteration:
            print self._obstacles
            assert 0, "No obstacle found for rect %s" % str(rect)

        self._SelectorOn(key)

    """Load obstacles from the list"""
    def FromList(self, obs):
        self._obstacles = {}

        for ob in obs:
            self._obstacles[self._obi] = list(ob)
            self._obi += 1

        self._UpdateSelector(restore=False)

__all__ = ["PanelObstaclesCtrl", "MY_EVT_OBSTACLES"]
