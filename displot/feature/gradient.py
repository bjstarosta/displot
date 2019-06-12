# -*- coding: utf-8 -*-
"""Method: GRADIENT

Based on a method by Simon Krausel (SADC).

Remove the background then apply an expanded Sobel gradient to retrieve the
details.

"""

from .__init__ import FeatureExtractor, FeatureExtractorException, Feature, FeatureException

import numpy as np
import cv2


class gradient(FeatureExtractor):

    FG_MEDIAN = 3
    BG_MEDIAN = 21
    CSIGMA = 0.33

    def __init__(self):
        super().__init__()

        self.desc = 'GRADIENT'

    def run(self):
        # remove background
        if int(self.FG_MEDIAN) % 2 == 0:
            raise FeatureException('FG_MEDIAN must be an odd integer.')
        if int(self.BG_MEDIAN) % 2 == 0:
            raise FeatureException('BG_MEDIAN must be an odd integer.')

        image_fg = cv2.medianBlur(self.image, int(self.FG_MEDIAN)).astype(np.float32)
        image_bg = cv2.medianBlur(self.image, int(self.BG_MEDIAN)).astype(np.float32)
        image_nobg = image_fg - image_bg
        image_nobg = self._feature_scale(image_nobg, 0, 255, np.uint8)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        image_nobg = clahe.apply(image_nobg)
        image_nobg = cv2.GaussianBlur(image_nobg, (9, 9), 0)

        self._image_debug_save('image_nobg', image_nobg)

        # Apply Canny edge detection
        median = np.median(image_nobg)
        lower = int(max(0, (1.0 - float(self.CSIGMA)) * median))
        upper = int(min(255, (1.0 + float(self.CSIGMA)) * median))
        bin_edges = cv2.Canny(image_nobg, lower, upper)
        self._image_debug_save('Canny edges', bin_edges)

        labels = self._feature_extract_edges(bin_edges)

        # merge both feature lists and discriminate based on expected properties
        labels_work = labels
        for region in labels:
            # remove obvious artifacts (features with too low width / height ratio)
            dim = region.dim
            ratio = min(dim[0], dim[1]) / max(dim[0], dim[1])
            if ratio < 0.1:
                labels_work.remove(region)
                continue

        labels = labels_work

        #print('len(labels)', len(labels))
        self.list = labels
