# -*- coding: utf-8 -*-
import sys
import numpy as np
import skimage.external.tifffile as tifffile


class Image(object):
    """Image data object.

    Attributes:
        data: False if no data has been loaded, otherwise is a 2-dim list of
            pixel values.
    """

    def __init__(self, filePath=""):
        self.data = False
        self.filePath = False

        if filePath != '':
            self.load(filePath)

    def load(self, filePath):
        self.filePath = filePath
        with tifffile.TiffFile(filePath) as tif:
            #print(tif.info())
            self.data = tif.asarray()

    def resize(self):
        pass

    @property
    def isLoaded(self):
        if self.data == False:
            return False
        else:
            return True
