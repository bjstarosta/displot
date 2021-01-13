# -*- coding: utf-8 -*-
"""displot - Toolbar UI functionality definitions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

from PyQt5 import QtWidgets


class Toolbar(QtWidgets.QToolBar):

    def link(self, window):
        """Link toolbar actions to event functions.

        Args:
            window (ui.DisplotUi): Displot main window object.

        Returns:
            None

        """
        self.window = window

        lt = self.window.layout
        self.btns = {
            'selectFeature': lt.actionSelectFeature,
            'addFeature': lt.actionAddFeature,
            'hideAllFeatures': lt.actionHideAllFeatures,
            # 'addExclusion': lt.actionAddExclusion,
            # 'removeExclusion': lt.actionRemoveExclusion
        }

        for k, v in self.btns.items():
            method = getattr(self, "on_" + k, None)
            if method is None:
                continue
            v.triggered[bool].connect(method)

        self.updateButtons()

    def updateButtons(self):
        """Update state of toolbar buttons depending on program state.

        Returns:
            None

        """
        it = self.window.tabWidget.currentWidget()

        # Enable and uncheck all
        for k, v in self.btns.items():
            v.setEnabled(True)
            if v.isCheckable() is True:
                v.setChecked(False)

        # Disable all if current tab is not ImageTab
        if type(it).__name__ != 'ImageTab':
            for k, v in self.btns.items():
                v.setEnabled(False)
            return

        # Set checked depending on mouse mode
        cm = self.window.cursorMode
        if cm.currentMode == 'feature_select':
            self.btns['selectFeature'].setChecked(True)
        if cm.currentMode == 'feature_new':
            self.btns['addFeature'].setChecked(True)
        if cm.currentMode in ['exclusion_new', 'exclusion_new_draw']:
            self.btns['addExclusion'].setChecked(True)

        if hasattr(it, 'featuresHidden'):
            self.btns['hideAllFeatures'].setChecked(it.featuresHidden)

    # Button event methods

    def on_selectFeature(self, checked=False):
        if checked is True:
            self.window.cursorMode.setMode('feature_select')
        else:
            self.window.cursorMode.resetMode()

        self.updateButtons()

    def on_addFeature(self, checked=False):
        if checked is True:
            self.window.cursorMode.setMode('feature_new')
        else:
            self.window.cursorMode.resetMode()

        self.updateButtons()

    def on_hideAllFeatures(self, checked=False):
        it = self.window.imageTabCurrent()
        if it is None:
            return

        if checked is True:
            it.hideAllFeatures()
        else:
            it.showAllFeatures()

        self.updateButtons()

    def on_addExclusion(self, checked=False):
        if checked is True:
            self.window.cursorMode.setMode('exclusion_new')
        else:
            self.window.cursorMode.resetMode()

        self.updateButtons()

    def on_removeExclusion(self, checked=False):
        self.updateButtons()
