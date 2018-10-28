# -*- coding: utf-8 -*-
import os
import numpy as np

from skimage import feature
from skimage.morphology import label
from skimage.measure import regionprops
from skimage.feature import greycomatrix, greycoprops
import skimage.external.tifffile as tifffile


class Image(object):
    """Image data object.

    Attributes:
        data: False if no data has been loaded, otherwise is a 2-dim list of
            pixel values.
        isLoaded: False on init, becomes True once the load() method is called.
        filePath: returns the OS path to the file, will be False unless the
            load() method is called.
        imageDim: returns a (width, height) tuple with the size of the image,
            or False if an image was not yet loaded.

    """

    def __init__(self, filePath=""):
        self.data = False
        self.filePath = False

        if filePath != '':
            self.load(filePath)

    def load(self, filePath):
        self.filePath = filePath
        with tifffile.TiffFile(filePath) as tif:
            self.data = tif.asarray()
            #print(tif.info())

    @property
    def isLoaded(self):
        if self.data == False:
            return False
        else:
            return True

    @property
    def fileSize(self):
        if not os.path.isfile(self.filePath):
            return 0

        size = os.stat(self.filePath).st_size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    @property
    def dimensions(self):
        if isinstance(self.data, bool):
            return False
        return {
            'w': self.data.shape[1],
            'h': self.data.shape[0]
        }


class ImageRegion(object):
    def __init__(self, imageHandle, x1, y1, x2, y2):
        pass

    def move(self, x1, y1, x2=None, y2=None):
        pass


def edgeDetection():
    pass

def discriminateLabels():
    pass

def testGLCM():
    pass
