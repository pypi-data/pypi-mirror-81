#!/usr/bin/env python
#
"""
This is a collection of general purpose utility functions and classes,
especially useful for wx functionality
"""
import sys
import wx
import wx.lib.masked as masked

import numpy


def set_float(val):
    """ utility to set a floating value,
    useful for converting from strings """
    out = None
    if not val in (None, ''):
        try:
            out = float(val)
        except ValueError:
            return None
        if numpy.isnan(out):
            out = default
    return out

class Closure:
    """A very simple callback class to emulate a closure (reference to
    a function with arguments) in python.

    This class holds a user-defined function to be executed when the
    class is invoked as a function.  This is useful in many situations,
    especially for 'callbacks' where lambda's are quite enough.
    Many Tkinter 'actions' can use such callbacks.

    >>>def my_action(x=None):
    ...    print('my action: x = ', x)
    >>>c = Closure(my_action,x=1)
    ..... sometime later ...
    >>>c()
     my action: x = 1
    >>>c(x=2)
     my action: x = 2

    based on Command class from J. Grayson's Tkinter book.
    """
    def __init__(self, func=None, *args, **kws):
        self.func  = func
        self.kws   = kws
        self.args  = args

    def __call__(self,  *args, **kws):
        self.kws.update(kws)
        if hasattr(self.func, '__call__'):
            self.args = args
            return self.func(*self.args, **self.kws)


class FloatCtrl(wx.TextCtrl):
    """ Numerical Float Control::
    a wx.TextCtrl that allows only numerical input, can take a precision argument
    and optional upper / lower bounds
    Options:

    """
    def __init__(self, parent, value='', minval=None, maxval=None,
                 precision=3, bell_on_invalid = True,
                 action=None, action_kw=None, **kws):

        self.__digits = '0123456789.-'
        self.__prec   = precision
        if precision is None:
            self.__prec = 0
        self.format   = '%%.%if' % self.__prec
        self.is_valid = True
        self.__val = set_float(value)
        self.__max = set_float(maxval)
        self.__min = set_float(minval)
        self.__bound_val = None
        self.__mark = None
        self.__action = None

        self.fgcol_valid   = "Black"
        self.bgcol_valid   = "White"
        self.fgcol_invalid = "Red"
        self.bgcol_invalid = (254, 254, 80)
        self.bell_on_invalid = bell_on_invalid

        # set up action
        if action_kw is None:
            action_kw = {}
        self.SetAction(action, **action_kw)

        this_sty =  wx.TE_PROCESS_ENTER|wx.TE_RIGHT
        if 'style' in kws:
            this_sty = this_sty | kws['style']
        kws['style'] = this_sty

        wx.TextCtrl.__init__(self, parent, wx.ID_ANY, **kws)

        self.__CheckValid(self.__val)
        self.SetValue(self.__val)

        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TEXT, self.OnText)

        self.Bind(wx.EVT_SET_FOCUS,  self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.__GetMark()

    def SetAction(self, action, **kws):
        "set callback action"
        if hasattr(action,'__call__'):
            self.__action = Closure(action, **kws)

    def SetPrecision(self, prec=0):
        "set precision"
        self.__prec = prec
        self.format = '%%.%if' % prec

    def __GetMark(self):
        " keep track of cursor position within text"
        try:
            self.__mark = min(wx.TextCtrl.GetSelection(self)[0],
                              len(wx.TextCtrl.GetValue(self).strip()))
        except:
            self.__mark = 0

    def __SetMark(self, mark=None):
        "set mark for later"
        if mark is None:
            mark = self.__mark
        self.SetSelection(mark, mark)

    def SetValue(self, value=None, act=True):
        " main method to set value "
        if value is None:
            value = wx.TextCtrl.GetValue(self).strip()
        self.__CheckValid(value)
        self.__GetMark()
        if value is not None:
            wx.TextCtrl.SetValue(self, self.format % set_float(value))

        if self.is_valid and hasattr(self.__action, '__call__') and act:
            self.__action(value=self.__val)
        elif not self.is_valid and self.bell_on_invalid:
            wx.Bell()

        self.__SetMark()

    def OnKillFocus(self, event):
        "focus lost"
        self.__GetMark()
        event.Skip()

    def OnSetFocus(self, event):
        "focus gained - resume editing from last mark point"
        self.__SetMark()
        event.Skip()

    def OnChar(self, event):
        """ on Character event"""
        key   = event.GetKeyCode()
        entry = wx.TextCtrl.GetValue(self).strip()
        pos   = wx.TextCtrl.GetSelection(self)
        # really, the order here is important:
        # 1. return sends to ValidateEntry
        if key == wx.WXK_RETURN:
            if not self.is_valid:
                wx.TextCtrl.SetValue(self, self.format % set_float(self.__bound_val))
            else:
                self.SetValue(entry)
            return

        # 2. other non-text characters are passed without change
        if (key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255):
            event.Skip()
            return

        # 3. check for multiple '.' and out of place '-' signs and ignore these
        #    note that chr(key) will now work due to return at #2

        has_minus = '-' in entry
        ckey = chr(key)
        if ((ckey == '.' and (self.__prec == 0 or '.' in entry) ) or
            (ckey == '-' and (has_minus or  pos[0] != 0)) or
            (ckey != '-' and  has_minus and pos[0] == 0)):
            return
        # 4. allow digits, but not other characters
        if chr(key) in self.__digits:
            event.Skip()


    def OnText(self, event=None):
        "text event"
        try:
            if event.GetString() != '':
                self.__CheckValid(event.GetString())
        except:
            pass
        event.Skip()

    def GetValue(self):
        if self.__prec > 0:
            fmt = "{{:.{:d}f}}".format(self.__prec)
            return set_float(fmt.format(self.__val))
        else:
            return int(self.__val)

    def GetMin(self):
        "return min value"
        return self.__min

    def GetMax(self):
        "return max value"
        return self.__max

    def SetMin(self, val):
        "set min value"
        self.__min = set_float(val)

    def SetMax(self, val):
        "set max value"
        self.__max = set_float(val)

    def __CheckValid(self, value):
        "check for validity of value"
        val = self.__val
        self.is_valid = True
        try:
            val = set_float(value)
            if self.__min is not None and (val < self.__min):
                self.is_valid = False
                val = self.__min
            if self.__max is not None and (val > self.__max):
                self.is_valid = False
                val = self.__max
        except:
            self.is_valid = False
        self.__bound_val = self.__val = val
        fgcol, bgcol = self.fgcol_valid, self.bgcol_valid
        if not self.is_valid:
            fgcol, bgcol = self.fgcol_invalid, self.bgcol_invalid

        self.SetForegroundColour(fgcol)
        self.SetBackgroundColour(bgcol)
        self.Refresh()
