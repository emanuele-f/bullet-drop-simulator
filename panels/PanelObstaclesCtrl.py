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

import collections
import wx

KEY_DELIMITER = "-"

class PanelObstaclesCtrl(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelObstaclesCtrl, self).__init__(parent, **kargs)

        self.selector = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.bt_delete = wx.Button(self, label="Elimina")
        self.bt_add = wx.Button(self, label="Aggiungi")
        self.x = wx.TextCtrl(self)
        self.y = wx.TextCtrl(self)
        self.width = wx.TextCtrl(self)
        self.height = wx.TextCtrl(self)
        self.obstacles = collections.OrderedDict()
        self._obi = 0

        self.bt_add.Bind(wx.EVT_BUTTON, self.OnObstacleAdd)
        self.bt_delete.Bind(wx.EVT_BUTTON, self.OnObstacleDelete)
        self.selector.Bind(wx.EVT_COMBOBOX, self.OnSelection)
        self._SetControlsEnabled(False)

        # Horizontal sizer
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(self.selector)
        hs.Add(self.bt_delete)
        hs.Add(self.bt_add)

        # Table sizer
        ts = wx.GridSizer(rows=4, cols=2)
        ts.Add(wx.StaticText(self, label="x"))
        ts.Add(self.x)
        ts.Add(wx.StaticText(self, label="y"))
        ts.Add(self.y)
        ts.Add(wx.StaticText(self, label="larghezza"))
        ts.Add(self.width)
        ts.Add(wx.StaticText(self, label="altezza"))
        ts.Add(self.height)

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
            self.x.Enable()
            self.y.Enable()
            self.width.Enable()
            self.height.Enable()
        else:
            self.bt_delete.Disable()
            self.x.Disable()
            self.y.Disable()
            self.width.Disable()
            self.height.Disable()

    def _GetSelectedObstacleId(self):
        val = self.selector.GetValue()
        i = val.find(KEY_DELIMITER)
        if i < 0:
            return -1
        oid = int(val[i+len(KEY_DELIMITER):])
        return oid

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
        for key, ob in self.obstacles.items():
            self.selector.Append("obstacle%s%d" % (KEY_DELIMITER, key))

        if restore and curval:
            if self.selector.FindString(curval) == -1:
                # it was deleted
                self._SelectorOn(-1)
            else:
                # restore selection
                self._SelectorOn(cursel)

    """Trigger information show for given obstacle."""
    def _ObstacleSelection(self, obi):
        if obi == -1:
            self._selection = -1
            self._SetControlsEnabled(False)
        else:
            self._selection = obi
            self._SetControlsEnabled(True)

    def OnObstacleAdd(self, event):
        obi = self._obi
        self._obi += 1

        self.obstacles[obi] = [0,0,0,0]
        self._UpdateSelector(restore=False)
        self._SelectorOn(obi)

    def OnObstacleDelete(self, event):
        sel = self._GetSelectedObstacleId()
        if sel != -1:
            self.obstacles.pop(sel)
            self._UpdateSelector()

    def OnSelection(self, event):
        self._ObstacleSelection(self._GetSelectedObstacleId())

__all__ = ["PanelObstaclesCtrl"]
