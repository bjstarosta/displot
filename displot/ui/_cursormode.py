# -*- coding: utf-8 -*-
"""displot - Cursor mode management.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtCore


class CursorMode(QtCore.QObject):
    """Cursor mode management class.

    Cursor modes are defined first, then events corresponding to those modes
    and particular event types. The currently active cursor mode can be set
    using the setMode method. Afterwards, calling the appropriate event
    method will fire all events assigned to the currently active mode and
    event type corresponding to the event method.

    'default' is always defined as a mode, and should have no events
    associated to it.

    Attributes:
        modes (list): List of all cursor modes.
        currentMode (str): Currently enabled mode.
        events (dict): Dictionary of all of the events grouped by type, then
            mode.
        modeChanged (QtCore.pyqtSignal): Qt signal that emits on mode change.

    """

    MOUSE_PRESS = 1
    MOUSE_RELEASE = 2
    MOUSE_MOVE = 3
    MOUSE_LEAVE = 4

    modeChanged = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.modes = []
        self.currentMode = None
        self.events = {
            self.MOUSE_PRESS: {},
            self.MOUSE_RELEASE: {},
            self.MOUSE_MOVE: {},
            self.MOUSE_LEAVE: {}
        }
        self.defineMode('default')
        self.setMode('default')

    def defineMode(self, mode):
        """Define a cursor mode.

        Args:
            mode (str): Mode identifier string.
                Can also accept a list of strings, in which case all of the
                strings will be set as separate modes.

        Returns:
            None

        """
        if type(mode) is list:
            for m in mode:
                self.defineMode(m)
            return

        if type(mode) is not str:
            raise ValueError('Cursor mode ID must be str: {0} - {1}'
                .format(mode, type(mode)))
        if mode in self.modes:
            raise ValueError('Cursor mode already defined: {0}'.format(mode))

        self.modes.append(mode)
        for k, v in self.events.items():
            self.events[k][mode] = []

    def setMode(self, mode):
        """Set currently active cursor mode.

        Args:
            mode (str): Mode identifier string.

        Returns:
            None

        """
        if mode not in self.modes:
            raise ValueError('Undefined cursor mode: {0}'.format(mode))

        self.currentMode = mode
        self.modeChanged.emit(mode)

    def resetMode(self):
        """Reset cursor mode to 'default'.

        Returns:
            None

        """
        self.setMode('default')

    def defineEvent(self, fn, evtype, mode):
        """Define an event on which to call the given callable object.

        The callable object will be called only if the specified mode is
        currently set, and the correct event type fires.

        Args:
            fn (callable): Callable object.
            evtype (int): Event type.
            mode (str): Previously defined cursor mode.

        Returns:
            None

        """
        if evtype not in self.events:
            raise ValueError('Undefined event type: {0}'.format(evtype))
        if mode not in self.modes:
            raise ValueError('Undefined cursor mode: {0}'.format(mode))
        if not callable(fn):
            raise ValueError('Event function not callable: {0}'.format(fn))

        self.events[evtype][mode].append(fn)

    def onMousePress(self, e):
        """Mouse press event delegator.

        Call this method from a QWidget that reimplements the mousePressEvent
        method to tie cursor mode events to that widget.

        Args:
            e (QtGui.QMouseEvent): Mouse event object.

        Returns:
            None

        """
        for fn in self.events[self.MOUSE_PRESS][self.currentMode]:
            fn(e)

    def onMouseRelease(self, e):
        """Mouse release event delegator.

        Call this method from a QWidget that reimplements the mouseReleaseEvent
        method to tie cursor mode events to that widget.

        Args:
            e (QtGui.QMouseEvent): Mouse event object.

        Returns:
            None

        """
        for fn in self.events[self.MOUSE_RELEASE][self.currentMode]:
            fn(e)

    def onMouseMove(self, e):
        """Mouse move event delegator.

        Call this method from a QWidget that reimplements the mouseMoveEvent
        method to tie cursor mode events to that widget.

        Args:
            e (QtGui.QMouseEvent): Mouse event object.

        Returns:
            None

        """
        for fn in self.events[self.MOUSE_MOVE][self.currentMode]:
            fn(e)

    def onMouseLeave(self, e):
        """Mouse leave event delegator.

        Call this method from a QWidget that reimplements the leaveEvent
        method to tie cursor mode events to that widget.

        Args:
            e (QtGui.QMouseEvent): Mouse event object.

        Returns:
            None

        """
        for fn in self.events[self.MOUSE_LEAVE][self.currentMode]:
            fn(e)
