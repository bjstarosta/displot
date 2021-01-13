# -*- coding: utf-8 -*-
"""displot - UI module.

Contains both UI definitions and functionality.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from ._mainwindow import DisplotUi
from ._console import Console, ConsoleHandler
from ._dialog import GenericDialog, AboutDialog
from ._styles import GuiStyles

__all__ = [
    "DisplotUi",
    "Console", "ConsoleHandler",
    "GenericDialog", "AboutDialog",
    "GuiStyles"
]
