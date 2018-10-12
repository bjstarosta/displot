import sys
import numpy as np
import skimage.external.tifffile as tifffile

from ui import DisplotUi


displotInfo = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha'
}

def main():
    UI = DisplotUi(displotInfo)
    UI.run()

if __name__ == '__main__':
    main()
