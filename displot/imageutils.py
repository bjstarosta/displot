# -*- coding: utf-8 -*-
import os
import csv
import numpy as np

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

def cluster_analysis(feature_list, k):
    points = []
    for feature in feature_list:
        points.append([float(feature.x), float(feature.y)])
    points = np.array(points)

    km = vq.kmeans2(points, k, iter=10, thresh=1e-05, minit='points', missing='warn')

    for i, cluster in enumerate(km[1]):
        feature_list[i].cluster_id = cluster

    return feature_list
