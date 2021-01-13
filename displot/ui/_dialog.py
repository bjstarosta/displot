# -*- coding: utf-8 -*-
"""displot - Dialog window UI functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import os
import markdown
from PyQt5 import QtCore, QtWidgets

from .ui_displot_about import Ui_AboutDialog
from .ui_displot_dialog import Ui_DialogBox


class AboutDialog(QtWidgets.QDialog):
    """About window object."""

    _HTMLBEGIN = '<span style="font-family:\'Roboto\', Arial, sans-serif;">'
    _HTMLEND = '</span>'

    def __init__(self, version):
        super().__init__()

        self.layout = Ui_AboutDialog()
        self.layout.setupUi(self)

        dp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')

        path = os.path.join(dp, 'markdown/about.md')
        with open(path, 'r', encoding='utf-8') as f:
            html = markdown.markdown(f.read())

        html = html.replace('{version}', str(version))

        browser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        browser.setHtml(self._HTMLBEGIN + html + self._HTMLEND)


class GenericDialog(QtWidgets.QDialog):
    """Generic dialog window object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = Ui_DialogBox()
        self.layout.setupUi(self)

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowTitleHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

    def setText(self, text):
        label = self.findChild(QtWidgets.QLabel, "dialogText")
        label.setText(text)

    def setAccept(self, func):
        btn = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        return btn.accepted.connect(func)

    def setReject(self, func):
        btn = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        return btn.rejected.connect(func)
