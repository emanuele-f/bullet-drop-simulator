import wx

class PanelObstaclesCtrl(wx.Panel):
    def __init__(self, parent, **kargs):
        super(PanelObstaclesCtrl, self).__init__(parent, **kargs)
        
        self.selector = wx.ComboBox(self, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.delete = wx.Button(self, label="Elimina")
        self.add = wx.Button(self, label="Aggiungi")
        self.x = wx.TextCtrl(self)
        self.y = wx.TextCtrl(self)
        self.width = wx.TextCtrl(self)
        self.height = wx.TextCtrl(self)
        self.lb_x = wx.StaticText(self, label="x")
        self.lb_y = wx.StaticText(self, label="y")
        self.lb_width = wx.StaticText(self, label="larghezza")
        self.lb_height = wx.StaticText(self, label="altezza")
        
        # Horizontal sizer
        hs = wx.BoxSizer(wx.HORIZONTAL)
        hs.Add(self.selector)
        hs.Add(self.delete)
        hs.Add(self.add)
        
        # Table sizer
        ts = wx.GridSizer(rows=4, cols=2)
        ts.Add(self.lb_x)
        ts.Add(self.x)
        ts.Add(self.lb_y)
        ts.Add(self.y)
        ts.Add(self.lb_width)
        ts.Add(self.width)
        ts.Add(self.lb_height)
        ts.Add(self.height)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hs)
        sizer.Add(ts)
        
        # Outer box
        box = wx.StaticBox(self, label="Gestione ostacoli")
        bs = wx.StaticBoxSizer(box)
        bs.Add(sizer)
        
        self.SetSizer(bs)
    
__all__ = ["PanelObstaclesCtrl"]
