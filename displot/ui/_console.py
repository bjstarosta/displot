# -*- coding: utf-8 -*-
"""displot - Console widget UI functionality definition.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import logging
from time import localtime, strftime
from PyQt5 import QtWidgets


class Console(QtWidgets.QFrame):
    """Console widget.

    Used for embedding logging output in the UI."""

    _HTMLBEGIN = '<span style="font-family: monospace;">'
    _HTMLEND = '</span>'
    _LINEFMT = "<b>[{0}]</b> {1}<br>"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._toggleButton = None
        self._textBox = None
        self._lines = []

    def link(self):
        """Instantiate relevant elements and set up events.

        Returns:
            None

        """
        self._toggleButton = self.findChild(QtWidgets.QPushButton,
            "consoleTitleLabel")
        self._textBox = self.findChild(QtWidgets.QTextEdit, "consoleTextBox")

        self._toggleButton.clicked.connect(self.toggle)
        self._textBox.hide()

    def toggle(self):
        """Toggle console visibility.

        Returns:
            None

        """
        if self._textBox.isVisible() is True:
            self._textBox.hide()
        else:
            self._textBox.show()

    def add_line(self, text):
        """Add new log line to console.

        Args:
            text (str): Log line contents.

        Returns:
            None

        """
        self._lines.append(
            (strftime("%Y-%m-%d %H:%M:%S", localtime()), text))
        self.update()

    def update(self):
        """Update console GUI widget.

        Should be called after each change to the widget's contents.
        Will scroll the console window to the bottom.

        Returns:
            None

        """
        html = self._HTMLBEGIN
        for line in self._lines:
            html += self._LINEFMT.format(line[0], line[1])
        html += self._HTMLEND
        self._textBox.setHtml(html)

        vscroll = self._textBox.verticalScrollBar()
        vscroll.setValue(vscroll.maximum())


class ConsoleHandler(logging.Handler):
    """Console widget logging handler.

    Usable with the logging package included with Python.

    Args:
        console (ui.Console): Console widget pointer.
        level (int): Error logging level.

    Attributes:
        console

    """

    def __init__(self, console, level=logging.NOTSET):
        super().__init__(level)
        self.console = console

    def emit(self, record):
        try:
            msg = self.format(record)
            self.console.add_line(msg)
            self.flush()
        except Exception:
            self.handleError(record)
