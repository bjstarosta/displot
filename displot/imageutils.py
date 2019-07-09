# -*- coding: utf-8 -*-
import os
import csv
import tarfile
import numpy as np
from PyQt5 import QtGui

from scipy.cluster import vq
import skimage.external.tifffile as tifffile

import displot.feature as feature
from displot.feature import *


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
        self.file_path = None

        self._feature_extractors = feature.get_methods()
        self.features = self._feature_extractors['swt4haar2']

        if file_path != '':
            self.load(file_path)

    def set_feature_extractor(self, fe):
        self.features = self._feature_extractors[fe]
        self.features.set_image_data(self.data)

    def load(self, file_path):
        self.file_path = file_path
        with tifffile.TiffFile(file_path) as tif:
            self.data = tif.asarray()
            self.metadata = tif.info()

        self.features.set_image_data(self.data)

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
    def file_name(self):
        return os.path.basename(self.file_path)

    @property
    def dimensions(self):
        if self.data is None:
            return None
        return {
            'w': self.data.shape[1],
            'h': self.data.shape[0]
        }

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]


class ImageData(object):

    def __init__(self, displot_info):
        self.metadata = {
            'dataVersion': displot_info['dataVersion']
        }
        self.editordata = {}

        self.image = None
        self.features = None

    def imageSavePng(self, scene, filepath):
        pixmap = QtGui.QPixmap(self.image.width, self.image.height)
        painter = QtGui.QPainter(pixmap)
        scene.render(painter)
        painter.end()
        pixmap.save(filepath, 'PNG')

    def imageSaveCsv(self, infodict, filepath):
        fieldnames = [
            'x', 'y', 'bx1', 'by1', 'bx2', 'by2', 'cluster_id'
        ]

        with open(filepath, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({
                'x': '--DISPLOT CSV FILE',
                'y': self.metadata['dataVersion'],
                'bx1': self.image.features.desc,
                'by1': self.image.file_path
            })

            for region in self.features:
                writer.writerow({
                    'x': region.x,
                    'y': region.y,
                    'bx1': region.bx1,
                    'by1': region.by1,
                    'bx2': region.bx2,
                    'by2': region.by2,
                    'cluster_id': region.cluster_id
                })

    def imageSavePackage(self, infodict, filepath):
        filename = os.path.basename(filepath)
        filename = filename[:filename.index('.')]
        csv_temp = os.getcwd() + '/' + filename + '.csv'
        self.imageSaveCsv(infodict, csv_temp)

        with tarfile.open(filepath, "w") as tar:
            for name in [self.image.file_path, csv_temp]:
                tar.add(name, os.path.basename(name))

        os.remove(csv_temp)


class BoundingRect(object):

    def __init__(self, x1, y1, x2, y2):

        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            raise ValueError('Argument values cannot be negative ('+str([x1, y1, x2, y2])+')')

        if x2 > x1:
            self.x1 = x1
            self.x2 = x2
        else:
            self.x1 = x2
            self.x2 = x1

        if y2 > y1:
            self.y1 = y1
            self.y2 = y2
        else:
            self.y1 = y2
            self.y2 = y1

    @property
    def width(self):
        return x2 - x1

    @property
    def height(self):
        return y2 - y1

    @property
    def area(self):
        return self.width * self.height

    def overlap_point(self, x, y):
        if (x >= self.x1 and x <= self.x2) and (y >= self.y1 and y <= self.y2):
            return True
        else:
            return False

    def overlap_rect(self, x1, y1, x2, y2):
        ix1 = max(x1, self.x1)
        iy1 = max(y1, self.y1)
        ix2 = min(x2, self.x2)
        iy2 = min(y2, self.y2)
        intr = (ix1 - ix2, iy1 - iy2)
        if intr[0] < 1 or intr[1] < 1:
            return False
        else:
            return True


def cluster_analysis(feature_list, k):
    points = []
    for feature in feature_list:
        points.append([float(feature.x), float(feature.y)])
    points = np.array(points)

    km = vq.kmeans2(points, k, iter=10, thresh=1e-05, minit='points', missing='warn')

    for i, cluster in enumerate(km[1]):
        feature_list[i].cluster_id = cluster

    return feature_list

def exclude_features(feature_list, exclusion_list):
    """Iterates through the feature list and checks for overlap with any
    exclusion areas on the second argument.

    Args:
        feature_list (list): A list of Feature objects. See feature/__init__.py.
        exclusion_list (str): A list of ImageExclusionArea objects. See ui_widgets.py.

    Returns:
        A list of filtered Feature objects.

    """
    out = []
    for f in feature_list:
        exclude = False
        for ex in exclusion_list:
            if ex.overlap_point(f.x, f.y) == True:
                exclude = True
        if exclude == False:
            out.append(f)
    return out
