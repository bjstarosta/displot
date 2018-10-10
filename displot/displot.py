import sys
import numpy as np
import skimage.external.tifffile as tifffile

from PyQt5 import QtGui, QtWidgets
from ui_def import *

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

mainwindow = ui_displot.Ui_MainWindow()
mainwindow.setupUi(window)

window.show()
MainWindow.setWindowTitle(_translate("MainWindow", "displot"))
sys.exit(app.exec_())

#testtif = '../../SADC_test/01-04-15_Nano-dash/M6_5K.TIF'

#with tifffile.TiffFile(testtif) as tif:
#    print(tif.info())
