# -*- coding: utf-8 -*-
import os
import csv
import numpy as np

from scipy.cluster import vq

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
        file_size: Size of the image file in human readable format.
        file_path: returns the OS path to the file, will be False unless the
            load() method is called.
        dimensions: returns a (width, height) tuple with the size of the image,
            or False if an image was not yet loaded.

    """

    FORMAT_PNG = 'png'
    FORMAT_CSV = 'csv'

    def __init__(self, file_path=""):
        self.data = None
        self.metadata = None
        self.regions = []
        self.cluster_id = None

        self.file_path = None

        if file_path != '':
            self.load(file_path)

    def load(self, file_path):
        self.file_path = file_path
        with tifffile.TiffFile(file_path) as tif:
            self.data = tif.asarray()
            self.metadata = tif.info()

    def save(self, file_path, format):
        if format == self.FORMAT_CSV:
            fieldnames = [
                'x', 'y', 'w', 'h', 'midpoint_x', 'midpoint_y',
                'glcm_dissimilarity', 'glcm_correlation', 'cluster_id'
            ]

            with open(file_path, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for region in self.regions:
                    writer.writerow({
                        'x': region.x,
                        'y': region.y,
                        'w': region.w,
                        'h': region.h,
                        'midpoint_x': region.midpoint[0],
                        'midpoint_y': region.midpoint[1],
                        'glcm_dissimilarity': region.glcm['dissimilarity'],
                        'glcm_correlation': region.glcm['correlation'],
                        'cluster_id': self.cluster_id
                    })

    def is_loaded(self):
        if self.data is None:
            return False
        else:
            return True

    @property
    def file_size(self):
        if not os.path.isfile(self.file_path):
            return 0

        size = os.stat(self.file_path).st_size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    @property
    def dimensions(self):
        if self.data is None:
            return None
        return {
            'w': self.data.shape[1],
            'h': self.data.shape[0]
        }


class ImageRegion(object):
    def __init__(self, imageRegion=None):
        self.label = imageRegion

        if imageRegion != None:
            self.bbox = imageRegion.bbox
            self.x = self.bbox[1]
            self.y = self.bbox[0]
            self.w = self.bbox[3]
            self.h = self.bbox[2]
        else:
            self.bbox = (0,0,0,0)
            self.x = 0
            self.y = 0
            self.w = 0
            self.h = 0
        self.glcm = {
            'dissimilarity': None,
            'correlation': None
        }

    @property
    def midpoint(self):
        x = round(self.x + (self.w / 2))
        y = round(self.y + (self.h / 2))
        return (x, y)

    def setSize(self, x, y, w, h):
        self.bbox = (x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move(self, x, y):
        self.x = x
        self.y = y
        self.bbox = (y, x, self.bbox[2], self.bbox[3])

    def moveMidpoint(self, x=None, y=None):
        if x is None:
            x = self.midpoint[0]
        if y is None:
            y = self.midpoint[1]

        x = round(x - (self.w / 2))
        y = round(y - (self.h / 2))
        self.move(x, y)

    def resize(self, w, h):
        self.w = w
        self.h = h
        self.bbox = (self.bbox[0], self.bbox[1], h, w)


def edge_detection(image, sigma=1., min_area=0, margin=0,
region_class=ImageRegion):
    """Canny edge detection for highlighting features of interest on images.

    Uses the scikit-image toolkit for the Canny implementation.

    Args:
        image (ndarray): A 2-dim numpy array containing the image data
        sigma (float): The sigma value to be used in the gaussian blur done by
            the Canny edge detector. A higher value means less edges highlighted.
        min_area (int): Minimum feature area in pixels. If a feature gets flagged
            with an area less than this number, it is discarded.
        margin (int): Discard all features that lay within this many pixels from
            the edge of the image.
        region_class (class): Class of the object that all highlighted features
            will be instantiated as. This class should ideally inherit from the
            ImageRegion class.

    Returns:
        tuple: The first element will contain a list of highlighted feature objects,
            the second element will contain a dictionary of statistics about the
            feature list.

    """

    stats = {
        'minAreaDiscarded': 0,
        'marginDiscarded': 0,
        'edgeDetectInitial': 0
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
    stats['edgeDetectFound'] = len(label_regions)

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

        region_obj = region_class(region)
        region_list.append(region_obj)

    return region_list, stats

def test_glcm(image, region_list,
distances=[4], angles=[0, np.pi/2], patch_size=25,
targets=(0,0), tolerances=(0,0)):
    """Grey level cooccurence matrix properties calculating function.

    Uses the scikit-image toolkit for the GLCM implementation. Takes a list of
    select regions of an image (say through edge detection, or using a simple
    iteration across the image)

    Args:
        image (ndarray): A 2-dim numpy array containing the image data
        region_list (list): A list of ImageRegion objects defining features to
            be scanned.
        distances (list): List of pixel pair distance offsets.
        angles (list): List of pixel pair angles in radians.
        patch_size (int): Size of the square edge of each computed region. The
            function takes the top left origin of each feature listed in
            region_list and extracts a square patch with the width and height
            defined by this parameter.
        targets (tuple): A tuple defining the midpoints of the target range for
            the following GLCM properties in order:
            dissimilarity, correlation.
        tolerances (tuple): A tuple defining the min/max offsets of the target
            range for the following GLCM properties in order:
            dissimilarity, correlation.

    Returns:
        tuple: The first element will contain a list of highlighted feature objects,
            the second element will contain a dictionary of statistics about the
            feature list.

    """

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
                region.glcm['dissimilarity'] = dissimilarity[i]
                region.glcm['correlation'] = correlation[i]
                cooccuring_regions.append(region)
                valid = True
                break

        if valid == False:
            stats['GLCMPropsDiscarded'] += 1

    return cooccuring_regions, stats

def cluster_analysis(region_list, k):
    points = []
    for region in region_list:
        pass

    return region_list

def remove_overlapped_regions(region_list, allowed_overlap=0):
    pass
