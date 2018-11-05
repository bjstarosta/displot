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
    def __init__(self, imageHandle, imageRegion):
        self.image = imageHandle
        self.label = imageRegion

    def move(self, x1, y1, x2=None, y2=None):
        pass


def edgeDetection(image, sigma=1., min_area=0, margin=0,
region_class=ImageRegion):

    stats = {
        'minAreaDiscarded': 0,
        'marginDiscarded': 0
    }

    if type(sigma) is int or type(sigma) is str:
        sigma = float(sigma)
    if type(sigma) is float or type(sigma) is str:
        min_area = int(min_area)
    if type(sigma) is float or type(sigma) is str:
        margin = int(margin)

    edge_detect = feature.canny(image, sigma=sigma)
    label_image = label(edge_detect)
    label_regions = regionprops(label_image, coordinates='rc')

    region_list = []
    for region in label_regions:
        if region.area < min_area:
            stats['minAreaDiscarded'] += 1
            continue

        minr, minc, maxr, maxc = region.bbox
        margin_r, margin_c = image.shape
        margin_r = margin_r - margin
        margin_c = margin_c - margin
        if minr < margin or minc < margin or maxr > margin_r or maxc > margin_c:
            stats['marginDiscarded'] += 1
            continue

        region_obj = region_class(image, region)
        region_list.append(region_obj)

    return region_list, stats

def testGLCM(image, region_list,
distances=[4], angles=[0, np.pi/2], patch_size=25,
targets=(0,0), tolerances=(0,0)):

    stats = {
        'borderOverlapDiscarded': 0,
        'GLCMPropsDiscarded': 0
    }

    if type(patch_size) is float or type(patch_size) is str:
        patch_size = int(patch_size)

    # Dissimilarity interval
    d_interval = (
        float(targets[0]) - float(tolerances[0]),
        float(targets[0]) + float(tolerances[0])
    )
    # Correlation interval
    c_interval = (
        float(targets[1]) - float(tolerances[1]),
        float(targets[1]) + float(tolerances[1])
    )

    cooccuring_regions = []

    for region in region_list:
        minr, minc, maxr, maxc = region.label.bbox
        if (image.shape[1] < (minc + patch_size)
        or image.shape[0] < (minr + patch_size)):
            stats['borderOverlapDiscarded'] += 1
            continue
        patch = image[minr:minr+patch_size, minc:minc+patch_size]

        glcm = greycomatrix(patch, distances, angles, 256, symmetric=True, normed=True)
        dissimilarity = greycoprops(glcm, 'dissimilarity')
        correlation = greycoprops(glcm, 'correlation')

        valid = False
        for i, x in np.ndenumerate(dissimilarity):
            if (dissimilarity[i] >= d_interval[0]
            and dissimilarity[i] <= d_interval[1]
            and correlation[i] >= c_interval[0]
            and correlation[i] <= c_interval[1]):
                cooccuring_regions.append(region)
                valid = True

        if valid == False:
            stats['GLCMPropsDiscarded'] += 1

    return cooccuring_regions, stats

def removeOverlap(image, region_list):
    pass
