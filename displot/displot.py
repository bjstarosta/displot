# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import os

    from ui import DisplotUi
    import imageutils


displot_info = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha',
    'author': 'Bohdan Starosta',
    'authorEmail': 'bjstarosta@gmail.com',
    'projectPage': 'https://github.com/bjstarosta/displot/'
}

def imageOpen(UI):
    filePath = UI.imageFileDlgOpen()
    if filePath == False:
        return

    image = imageutils.Image(filePath)

    UI.setStatusBarMsg('Loading image file: ' + filePath)
    UI.imageTabOpen(image, os.path.basename(filePath))
    UI.updateWindowTitle()
    UI.setStatusBarMsg('Done.')

def main():
    UI = DisplotUi(displot_info)

    UI.layout.actionOpenImage.triggered.connect(lambda: imageOpen(UI))

    UI.run()

if __name__ == '__main__':
    main()
