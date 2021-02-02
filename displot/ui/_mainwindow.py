# -*- coding: utf-8 -*-
"""displot - Main window UI functionality definitions.

Contains basic main window instantiation, open/close/save events for image
tabs, and tab indexing methods.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import gc
import os
import sys
import json
import logging
import markdown
from PyQt5 import QtCore, QtWidgets

import displot.io
import displot.weights
from ._cursormode import CursorMode
from ._dialog import GenericDialog, AboutDialog
from ._imagetab import ImageTab
from ._imagetab_cursors import ImageTabCursors
from ._styles import GuiStyles
from .ui_displot import Ui_MainWindow

log = logging.getLogger('displot')


class DisplotUi(QtWidgets.QMainWindow):
    """Main window UI object.

    Attributes:
        app (QtWidgets.QApplication): Qt application object.
        layout (ui.Ui_MainWindow): Layout definition object.
            Generated from .ui files in /devel/.
        imageTabs (list): List of ImageTab objects representing currently
            opened images.
        imageTabFeatureStyle (ImageTabFeatureStyle): Style object containing
            Qt pen and brush definitions.
        tabWidget (QtWidgets.QTabWidget): Reference to the QTabWidget object
            holding the opened images.
        appTitle (str): Application title as shown on the title bar.
        appVersion (str): Application version as shown on the title bar.
        titleFormat (str): Template for string displayed on the title bar.

    """

    def __init__(self):
        # Start the application before main window init
        self.app = QtWidgets.QApplication(sys.argv)
        self.threadpool = QtCore.QThreadPool()

        super().__init__()

        # Set up layout
        self.layout = Ui_MainWindow()
        self.layout.setupUi(self)

        self.imageTabs = []
        self.styles = GuiStyles()

        # Reference important UI objects
        self.tabWidget = self.layout.tabWidget
        self.console = self.layout.consoleFrame
        self.console.link()

        # Load project metadata
        dp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
        with open(os.path.join(dp, 'meta.json'), 'r', encoding='utf-8') as f:
            self.meta = json.load(f)

        # Query available weight files
        self.weights = displot.weights.list_weights()

        # Populate the welcome page
        dp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
        path = os.path.join(dp, 'markdown/stab.md')

        html = '<span style="font-family:\'Roboto\', Arial, sans-serif;">'
        with open(path, 'r', encoding='utf-8') as f:
            html += markdown.markdown(f.read())
        html += '</span>'

        browser = self.layout.whatsNewBrowser
        browser.setHtml(html)

        # Other properties
        self._lastDir = os.getcwd()

        # Linkages and updates
        self.toolbar = self.layout.toolBar
        self.toolbar.link(self)

        self.appTitle = 'displot'
        self.appVersion = self.meta['app_version']
        self.titleFormat = "{app} v.{ver} - [{file}]"
        self.updateWindowTitle()

        lt = self.layout
        lt.actionOpenImage.triggered.connect(self.imageTabOpen)
        lt.actionSaveImageAs.triggered.connect(self.imageTabSave)
        lt.actionExport_Features.triggered.connect(self.imageTabExportFeatures)
        lt.actionExport_Bitmap.triggered.connect(self.imageTabExport)
        lt.actionCloseImage.triggered.connect(self.imageTabClose)
        lt.actionExit.triggered.connect(self.exit)
        lt.actionAbout.triggered.connect(self.openAbout)
        self.updateMenuBar()

        # Setup cursor modes
        self.cursorMode = CursorMode()
        self.cursorMode.defineMode([
            'feature_select',
            'feature_new',
            'feature_move',
            'exclusion_new',
            'exclusion_new_draw',
            'exclusion_move',
            'exclusion_resize'
        ])

        # Setup events
        self.imageTabCursors = ImageTabCursors(self)
        self.tabWidget.tabCloseRequested.connect(self.imageTabClose)
        self.tabWidget.currentChanged.connect(self.updateWindowTitle)
        self.tabWidget.currentChanged.connect(self.updateMenuBar)
        self.tabWidget.currentChanged.connect(self.cursorMode.resetMode)
        self.tabWidget.currentChanged.connect(self.toolbar.updateButtons)
        self.cursorMode.modeChanged.connect(self.toolbar.updateButtons)

    def run(self):
        """Show the GUI, then block until window is closed.

        All non-event code running after this method will not execute.
        """
        self.show()
        sys.exit(self.app.exec_())

    def exit(self):
        """Exits the program gracefully."""
        gc.collect(1)
        self.app.quit()

    def closeEvent(self, ev):
        """Event handler reimplementation for the window close event."""
        self.exit()

    def openAbout(self):
        """Opens the program About dialog."""
        dlg = AboutDialog(self.appVersion)
        dlg.show()
        dlg.exec_()

    def setStatusBarMsg(self, message="", timeout=0):
        """Shows a short message in the status bar at the bottom of the window.

        Args:
            message (str): Message string to show in the status bar.
            timeout (int): Amount of time in seconds after which the message
                will disappear. By default it's set to 0, which means the
                message will stay shown until replaced with something else.

        Returns:
            None

        """
        self.statusBar().showMessage(message, timeout)

    def imageTabOpen(self):
        """Open a file browser dialog for selecting an image file.

        Launches a file browser dialog to get a file path, then loads that
        file path as an image into a new tab.

        Returns:
            None

        """
        dlg = QtWidgets.QFileDialog(self, 'Open image', self._lastDir)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        # dlg.setFilter(QtCore.QDir.AllEntries | QtCore.QDir.NoDotAndDotDot)
        dlg.setNameFilters([
            'Displot readable files (*.tif *.png *{0})'.format(
                displot.io.DP_EXT),
            'Image files (*.tif *.png)',
            'Displot data files (*{0})'.format(displot.io.DP_EXT),
            'All files (*)'
        ])

        ret = dlg.exec_()
        self._lastDir = dlg.history()[-1]

        if ret == QtWidgets.QDialog.Accepted:
            path = dlg.selectedFiles()[0]
        else:
            return

        self.setStatusBarMsg('Loading image file: ' + path)
        self.imageTabCreate(path, os.path.basename(path))
        self.setStatusBarMsg('Done.', 3)

        self.updateWindowTitle()
        self.updateMenuBar()

    def imageTabCreate(self, path, tab_name="No image"):
        """Create a new tab for the specified image path.

        Args:
            path (str): Path to image file.
            tab_name (str): Name of the image tab.

        Returns:
            ui.ImageTab: Tab object reference.
                Will return None if loading failed.

        """
        try:
            it = ImageTab(self, self.tabWidget, tab_name, path)
        except (
            RuntimeError,
            FileNotFoundError,
            IsADirectoryError,
            PermissionError
        ) as e:
            errstr = 'Unknown error when loading: "{0}".'
            print(type(e))
            if isinstance(e, FileNotFoundError):
                errstr = 'Cannot load, file not found: "{0}".'
            if isinstance(e, IsADirectoryError):
                errstr = 'Cannot load, path leads to directory: "{0}".'
            if isinstance(e, PermissionError):
                errstr = 'Cannot load, file not readable: "{0}".'
            if isinstance(e, RuntimeError):
                errstr = 'Cannot load, filetype not supported: "{0}".'
            log.info(errstr.format(e))
            it = None

        if it is not None:
            self.imageTabs.append(it)

        return it

    def imageTabClose(self, index=None, dialog=True):
        """Close and remove the image tab at the specified index.

        Args:
            index (int): Image tab index. Corresponds to its order in the
                tab list. If None is passed, the method will attempt to
                determine the currently selected tab.

        Returns:
            None

        """
        if index is None or index is False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it is None:
            return

        if dialog is True:
            dlg = GenericDialog(parent=self)
            dlg.setText('Changes will be unsaved. '
                'Are you sure you want to close this tab?')
            dlg.setWindowTitle('Are you sure?')
            dlg.setAccept(lambda: self.imageTabClose(index, dialog=False))
            dlg.show()
            dlg.exec_()
        else:
            it.remove()
            self.imageTabs.remove(it)

    def imageTabSave(self, index=None):
        """Open a file browser dialog for saving a displot data file.

        Args:
            index (int): Index of the ImageTab the image data of which should
                be saved. If None is passed, the method will attempt to find
                the currently selected tab.

        Returns:
            None

        """
        if index is None or index is False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it is None:
            return

        dlg = QtWidgets.QFileDialog(self, 'Save as', self._lastDir)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilter('Displot data file (*{0})'.format(
            displot.io.DP_EXT
        ))

        ret = dlg.exec_()
        self._lastDir = dlg.history()[-1]

        if ret == QtWidgets.QDialog.Accepted:
            path = dlg.selectedFiles()[0]
            # snf = dlg.selectedNameFilter()
        else:
            return

        splitext = os.path.splitext(path)
        if splitext[1] == '':
            path = path + displot.io.DP_EXT

        self.setStatusBarMsg('Saving displot file: ' + path)
        it.syncFeaturesFromUi()
        it.save_data(path)
        self.setStatusBarMsg('Saved displot file: ' + path, 3000)

    def imageTabExport(self, index=None):
        """Export the current image tab graphics scene into a bitmap.

        Opens a GUI file dialog to determine the bitmap path.

        Args:
            index (int): Index of the ImageTab the image data of which should
                be saved. If None is passed, the method will attempt to find
                the currently selected tab.

        Returns:
            None

        """
        if index is None or index is False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it is None:
            return

        dlg = QtWidgets.QFileDialog(self, 'Export bitmap', self._lastDir)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilter('PNG image (*.png)')

        ret = dlg.exec_()
        self._lastDir = dlg.history()[-1]

        if ret == QtWidgets.QDialog.Accepted:
            path = dlg.selectedFiles()[0]
        else:
            return

        splitext = os.path.splitext(path)
        if splitext[1] == '':
            path = path + '.png'

        self.setStatusBarMsg('Exporting image file: ' + path)
        it.imView.getScenePixmap().save(path)
        self.setStatusBarMsg('Exported image file: ' + path, 3000)

    def imageTabExportFeatures(self, index):
        """Export the current image tab feature data into a file.

        Opens a GUI file dialog to determine the file path.

        Args:
            index (int): Index of the ImageTab the image data of which should
                be saved. If None is passed, the method will attempt to find
                the currently selected tab.

        Returns:
            None

        """
        if index is None or index is False:
            it = self.imageTabCurrent()
        else:
            it = self.imageTabFind(index)

        if it is None:
            return

        dlg = QtWidgets.QFileDialog(self, 'Export features', self._lastDir)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilter('CSV file (*.csv)')

        ret = dlg.exec_()
        self._lastDir = dlg.history()[-1]

        if ret == QtWidgets.QDialog.Accepted:
            path = dlg.selectedFiles()[0]
        else:
            return

        splitext = os.path.splitext(path)
        if splitext[1] == '':
            path = path + '.csv'

        self.setStatusBarMsg('Exporting file: ' + path)
        it.syncFeaturesFromUi()
        it.save_features(path)
        self.setStatusBarMsg('Exported file: ' + path, 3000)

    def imageTabFind(self, index):
        """Find the image tab at the specified index.

        Args:
            index (int): Image tab index. Corresponds to its order in the
                tab list.

        Returns:
            ui.ImageTab: ImageTab object, or None if no selected object was
                found.

        """
        if index == -1:
            return None

        for o in self.imageTabs:
            if o.tabIndex == index:
                return o

        return None

    def imageTabCurrent(self):
        """Return currently selected image tab.

        Returns:
            ui.ImageTab: ImageTab object, or None if no selected object was
                found.

        """
        return self.imageTabFind(self.tabWidget.currentIndex())

    def updateWindowTitle(self):
        """Update windowbar title to reflect currently focused image file.

        Returns:
            None

        """
        it = self.imageTabCurrent()
        if it is None:
            cur_file = 'No image'
        else:
            cur_file = it.imagePath

        title = self.titleFormat.format(
            app=self.appTitle,
            ver=self.appVersion,
            file=cur_file
        )
        self.setWindowTitle(title)

    def updateMenuBar(self):
        """Update elements within the menu bar based on selected tab.

        Returns:
            None

        """
        it = self.imageTabCurrent()
        if isinstance(it, ImageTab):
            enable = True
        else:
            enable = False

        items = [
            self.layout.actionSaveImageAs,
            self.layout.actionExport_Features,
            self.layout.actionExport_Bitmap,
            self.layout.actionCloseImage
        ]
        for i in items:
            i.setEnabled(enable)
