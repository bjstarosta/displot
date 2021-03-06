# -*- coding: utf-8 -*-
"""Displot main module.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import logging
import displot.io
import displot.detection
import displot.tf

log = logging.getLogger('displot')


class Displot(object):
    """Program functionality class.

    It is inherited by the Qt UI image tab class, meaning the UI hooks into the
    functionality present in this class.

    Attributes:
        data_obj (io.DisplotData): Data object (main model).

    """

    def __init__(self):
        self.data_obj = None
        displot.tf.detect_gpu_support()

    def load_data(self, path):
        self.data_obj = displot.io.load_displot_data(path)
        log.info('Loaded file: "{0}".'.format(path))

    def save_data(self, path):
        displot.io.save_displot_data(path, self.data_obj)
        log.info('Saved file: "{0}".'.format(path))

    def save_features(self, path):
        displot.io.save_features(path, self.data_obj)
        log.info('Saved features: "{0}".'.format(path))

    def detection(self, *args, **kwargs):
        if self.data_obj is None:
            log.error('Data object is not loaded.')

        tds = displot.detection.detection(*args, **kwargs)
        log.info('Detection process completed. Features found: {0}.'.format(
            len(tds[0])
        ))
        log.info('Average prediction confidence: {:.3f}.'.format(tds[1]))
        self.data_obj.markers = tds[0]

    def discrimination(self, *args, **kwargs):
        if self.data_obj is None:
            log.error('Data object is not loaded.')

        if len(self.data_obj.markers) == 0:
            log.info('There are no features currently defined. Nothing to do.')
            return

        tds = displot.detection.discrimination(*args, **kwargs)
        for i, td in enumerate(self.data_obj.markers):
            if td in tds[0]:
                self.data_obj.markers[i].isHidden = False
            else:
                self.data_obj.markers[i].isHidden = True

        log.info('Discrimination completed. Visible features: {0}.'.format(
            len(tds[0])
        ))
        log.info('Avg. visible prediction confidence: {:.3f}.'.format(tds[1]))
