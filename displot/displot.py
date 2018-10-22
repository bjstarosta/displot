# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import os
    from ui import DisplotUi
    from imageutils import Image


displotInfo = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha',
    'author': 'Bohdan Starosta',
    'authorEmail': 'bjstarosta@gmail.com',
    'projectPage': 'https://github.com/bjstarosta/displot/'
}

if __name__ == '__main__':
    UI = DisplotUi(displotInfo)

def imageOpen():
    filePath = UI.imageFileDlgOpen()
    if filePath == False:
        return
    image = Image(filePath)
    UI.setStatusBarMsg('Loading image file: ' + filePath)
    UI.imageTabOpen(image, os.path.basename(filePath))
    UI.updateWindowTitle()
    UI.setStatusBarMsg('Done.')

def main():
    # Setup common events
    UI.tabWidget.tabCloseRequested.connect(UI.imageTabClose)
    UI.tabWidget.currentChanged.connect(UI.updateWindowTitle)

    UI.layout.actionOpenImage.triggered.connect(imageOpen)
    UI.layout.actionCloseImage.triggered.connect(UI.imageTabClose)
    UI.layout.actionExit.triggered.connect(UI.exit)

    UI.layout.actionAbout.triggered.connect(UI.openAbout)

    UI.run()

if __name__ == '__main__':
    main()
