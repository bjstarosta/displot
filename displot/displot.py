# -*- coding: utf-8 -*-
import os
from ui import DisplotUi
from imageutils import Image


displotInfo = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha'
}

UI = DisplotUi(displotInfo)

def imageOpen():
    filePath = UI.imageFileDlgOpen()
    if filePath == False:
        return
    image = Image(filePath)
    UI.imageTabOpen(image, os.path.basename(filePath))

def main():
    # Setup common events
    UI.tabWidget.tabCloseRequested.connect(UI.imageTabClose)

    UI.windowUi.actionOpenImage.triggered.connect(imageOpen)
    UI.windowUi.actionCloseImage.triggered.connect(UI.imageTabClose)
    UI.windowUi.actionExit.triggered.connect(UI.exit)

    UI.run()

if __name__ == '__main__':
    main()
