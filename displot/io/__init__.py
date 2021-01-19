# -*- coding: utf-8 -*-
"""displot - Input/output module.

Handles reading and writing images and other data.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import os
from ._io import _load_image, _load_dpfile, _save_dpfile, _save_csv

__all__ = [
    "DisplotData", "DisplotDataFeature",
    "save_displot_data", "load_displot_data"
]

DP_EXT = '.dpa'


class DisplotData(object):

    def __init__(self, image=None, path=None, meta=None):
        self.image = image
        self.image_path = path
        self.image_meta = meta
        self.markers = []
        self.editor_data = {}

    @property
    def image_width(self):
        return self.image.shape[1]

    @property
    def image_height(self):
        return self.image.shape[0]

    @property
    def iw(self):
        return self.image_width

    @property
    def ih(self):
        return self.image_height

    def fromDict(self, d):
        self.image_path = d['image_path']
        self.image_meta = d['image_meta']
        self.editor_data = d['editor_data']

        self.markers = []
        for f in d['markers']:
            o = DisplotDataFeature()
            o.fromDict(f)
            self.markers.append(o)

    def toDict(self):
        d = {}

        basic = ['image_path', 'image_meta', 'editor_data']
        for i in basic:
            d[i] = getattr(self, i)

        d['markers'] = []
        for f in self.markers:
            d['markers'].append(f.toDict())

        return d


class DisplotDataFeature(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.r = 10
        self.confidence = 1

    def fromDict(self, d):
        for attr, value in d.items():
            setattr(self, attr, value)

    def toDict(self):
        return {
            'x': self.x,
            'y': self.y,
            'r': self.r,
            'confidence': self.confidence
        }


def save_displot_data(path, obj):
    ext = os.path.splitext(path)[1].lower()

    if ext == DP_EXT:
        obj = _save_dpfile(path, obj)


def load_displot_data(path):
    """Load a data file recognised by displot.

    Can include a path to a displot archive including both image and editor
    data, as well as purely image data.
    Will raise catchable exceptions if there is a problem with loading files.

    Args:
        path (str): Path to data file.

    Returns:
        io.DisplotData: Displot data object.

    """
    ext = os.path.splitext(path)[1].lower()

    if ext == DP_EXT:
        obj = _load_dpfile(path, DisplotData())
    else:
        obj = _load_image(path, DisplotData())

    return obj


def save_features(path, obj):
    _save_csv(path, obj)
