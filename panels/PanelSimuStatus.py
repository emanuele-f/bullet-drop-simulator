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

import math
import wx
from constraints import Measures, THEME

class PanelSimuStatus(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelSimuStatus, self).__init__(parent, **kargs)

        self.startBt = wx.Button(self, label="Start")
        self.vx = wx.StaticText(self)
        self.vy = wx.StaticText(self)
        self.x = wx.StaticText(self)
        self.y = wx.StaticText(self)
        self.t = wx.StaticText(self)
        self._arrowdir = _PanelArrowDirection(self)

        # Table sizer
        ts = wx.GridSizer(rows=5, cols=3, hgap=Measures.PANEL_INNER_PADDING)
        ts.Add(wx.StaticText(self, label=u"Velocità x"))
        ts.Add(self.vx, flag=wx.ALIGN_CENTER_HORIZONTAL)
        ts.Add(wx.StaticText(self, label="u/s"))
        ts.Add(wx.StaticText(self, label=u"Velocità y"))
        ts.Add(self.vy, flag=wx.ALIGN_CENTER_HORIZONTAL)
        ts.Add(wx.StaticText(self, label="u/s"))
        ts.Add(wx.StaticText(self, label="X"))
        ts.Add(self.x, flag=wx.ALIGN_CENTER_HORIZONTAL)
        ts.Add(wx.StaticText(self, label="u"))
        ts.Add(wx.StaticText(self, label="Y"))
        ts.Add(self.y, flag=wx.ALIGN_CENTER_HORIZONTAL)
        ts.Add(wx.StaticText(self, label="u"))
        ts.Add(wx.StaticText(self, label="Tempo"))
        ts.Add(self.t, flag=wx.ALIGN_CENTER_HORIZONTAL)
        ts.Add(wx.StaticText(self, label="s"))
        
        # Vertical sizer / left
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self._arrowdir, 1, flag=wx.EXPAND)
        vsizer.Add(self.startBt, flag=wx.TOP, border=Measures.PANEL_INNER_PADDING)

        # Main sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(vsizer, flag=wx.EXPAND)
        sizer.Add(ts, flag=wx.LEFT|wx.EXPAND, border=Measures.PANEL_INNER_PADDING)

        # Outer box
        box = wx.StaticBox(self, label="Stato simulazione")
        bs = wx.StaticBoxSizer(box)
        bs.Add(sizer, flag=wx.ALL|wx.EXPAND, border=Measures.PANEL_BOX_PADDING)

        self.SetSizer(bs)
        self.startBt.Bind(wx.EVT_BUTTON, lambda ev: self._arrowdir.HideArrow() or ev.Skip())

    """Binds the start button to a callback. """
    def BindStart(self, func):
        self.startBt.Bind(wx.EVT_BUTTON, lambda ev: self._btcallback(ev, func))
    def _btcallback(self, ev, callback):
        # hide arrow, then execute given callback
        self._arrowdir.HideArrow()
        return callback(ev)

    def SetStatus(self, msg):
        self.startBt.SetLabel(msg)

    def UpdateData(self, x, y, vx, vy, t):
        self.x.SetLabel("%.1f" % x)
        self.y.SetLabel("%.1f" % y)
        self.vx.SetLabel("%.1f" % vx)
        self.vy.SetLabel("%.1f" % vy)
        self.t.SetLabel("%.2f" % t)
        
        # show speed direction
        angle = math.atan(vy*1./vx)
        self._arrowdir.SetArrowAngle(angle)
        
class _PanelArrowDirection(wx.Panel):
    def __init__(self, parent, **kargs):
        super(_PanelArrowDirection, self).__init__(parent, **kargs)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda ev: None)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self._theme = THEME
        self._refsize = self.GetSize()
        self._angle = None
        
    def SetArrowAngle(self, angle):
        self._angle = angle
        self.Refresh()
        
    def HideArrow(self):
        self._angle = None
        self.Refresh()
        
    def _DrawCenteredArrowDirection(self, dc, sw, sh, l, angle):
        # use a GraphicsContext to ease the drawings
        gc = wx.GraphicsContext.Create(dc)
        
        if gc:
            # Set coords system to be centered on the sw,sh and properly rotated
            gc.Translate(sw/2, sh/2)
            gc.Rotate(-angle)
            gc.SetPen(dc.GetPen())
            gc.SetAntialiasMode(True)
            
            # Draw the arrow
            path = gc.CreatePath()
            path.MoveToPoint(-l/2, 0)
            path.AddLineToPoint(l/2, 0)
            path.AddLineToPoint(l/4, l/5)
            path.MoveToPoint(l/2, 0)
            path.AddLineToPoint(l/4, -l/5)
            gc.StrokePath(path)
        
    def OnSize(self, ev):
        self._refsize = ev.GetSize()
        self.Refresh()
        
    def OnPaint(self, ev):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        
        # bounding rect
        dc.DrawRectangle(0, 0, self._refsize[0], self._refsize[1])
        
        if not self._angle is None:
            # draw arrow
            w, h = self._refsize
            dc.SetPen(wx.Pen(self._theme["arrow"], self._theme["arrow_width"]))
            self._DrawCenteredArrowDirection(dc, w, h, w/2, self._angle)

__all__ = ["PanelSimuStatus"]
