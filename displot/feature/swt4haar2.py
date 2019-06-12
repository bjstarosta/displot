# -*- coding: utf-8 -*-
"""Method: SWT4HAAR2

Decompose the image using stationary wavelet transform (SWT) into 4 levels using
the Haar wavelet, and mix the first and second levels to extract detail.

"""

from .__init__ import FeatureExtractor, FeatureExtractorException, Feature, FeatureException

import numpy as np
import cv2
import pywt
from scipy.stats import norm
from matplotlib import pyplot as plt


class swt4haar2(FeatureExtractor):

    FG_MEDIAN = 3
    BG_MEDIAN = 21
    L0MUL = 0.75
    L1MUL = 0.25
    CSIGMA = 0.33

    MAX_BBOX_OVERLAP = 0.33
    MAX_OVERLAP = 0.75
    MIN_FEATURE_AREA = 15
    LARGE_FEATURE_AREA = 100

    def __init__(self):
        super().__init__()

        self.desc = 'SWT4HAAR2'

    def run(self):
        self.list = []

        # separate background from foreground
        if int(self.FG_MEDIAN) % 2 == 0:
            raise FeatureException('FG_MEDIAN must be an odd integer.')
        if int(self.BG_MEDIAN) % 2 == 0:
            raise FeatureException('BG_MEDIAN must be an odd integer.')

        image_fg = cv2.medianBlur(self.image, int(self.FG_MEDIAN)).astype(np.float32)
        image_bg = cv2.medianBlur(self.image, int(self.BG_MEDIAN)).astype(np.float32)
        image_nobg = image_fg - image_bg
        image_nobg = self._feature_scale(image_nobg, 0, 255, np.uint8)

        self._image_debug_save('image_nobg', image_nobg)

        # decompose the image into detail levels
        input_len = self.image.shape[0]
        maxl = pywt.swt_max_level(input_len)
        coeffs = pywt.swt2(image_nobg, 'haar', level=maxl, start_level=0)

        # horizontal detail mix l0 + l1
        lh0 = coeffs[0][1][0]
        lh1 = coeffs[1][1][0]
        lh01 = cv2.addWeighted(lh0, self.L0MUL, lh1, self.L1MUL, 0)

        # vertical detail mix l0 + l1
        hl0 = coeffs[0][1][1]
        hl1 = coeffs[1][1][1]
        hl01 = cv2.addWeighted(hl0, self.L0MUL, hl1, self.L1MUL, 0)

        # mix both together
        img_mixed = cv2.addWeighted(lh01, 0.5, hl01, 0.5, 0)

        # feature scale and cast to 8 bit unsigned
        img_mixed = self._feature_scale(img_mixed, 0, 255, np.uint8)

        # apply histogram equalisation and blur
        img_mixed = cv2.medianBlur(img_mixed, 5).astype(np.uint8)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_mixed = clahe.apply(img_mixed)
        img_mixed = cv2.GaussianBlur(img_mixed, (9, 9), 0)

        self._image_debug_save('Vert. + Horiz. L0+1 coefficients', img_mixed)

        # calculate brightness histogram and thresholding values
        img_ravel = img_mixed.ravel()
        hist, bin_edges = np.histogram(img_ravel, 256, [0, 256], density=True)
        loc, scale = norm.fit(img_ravel)

        thresh_end = int(norm.ppf(0.5, loc=loc, scale=scale))
        thresh_st1 = int(norm.ppf(0.005, loc=loc, scale=scale))
        thresh_st2 = int(norm.ppf(0.001, loc=loc, scale=scale))
        #print(thresh_end, thresh_st1, thresh_st2)

        """# attempt at removing image defects
        lh4 = coeffs[3][1][0]
        hl4 = coeffs[3][1][1]
        l4 = cv2.addWeighted(lh4, 0.5, hl4, 0.5, 0)
        l4 = coeffs[2][1][2]
        l4 = self._feature_scale(l4, 0, 255, np.uint8)
        #l4 = cv2.GaussianBlur(l4, (3, 3), 0)
        l4 = cv2.medianBlur(l4, 5).astype(np.uint8)
        t, l4thresh = cv2.threshold(l4, int(norm.ppf(0.002, loc=loc, scale=scale)), thresh_end, cv2.THRESH_TOZERO_INV)
        #t, l4thresh2 = cv2.threshold(l4thresh, int(norm.ppf(0.001, loc=loc, scale=scale)), thresh_end, cv2.THRESH_BINARY_INV)
        self._image_debug_save('Vert. + Horiz. L3 coefficients', l4thresh)"""

        """# debug histogram plot
        fig, ax = plt.subplots(1, 1)
        #ax.plot(x, pdf)
        plt.hist(img_ravel, 256, [0, 256])
        plt.show()"""

        # prominent features
        t, img_thresh1 = cv2.threshold(img_mixed, thresh_st1, thresh_end, cv2.THRESH_TRUNC)
        self._image_debug_save('After first threshold', img_thresh1)
        t, img_thresh2 = cv2.threshold(img_mixed, thresh_st2, thresh_end, cv2.THRESH_BINARY_INV)
        self._image_debug_save('After second threshold', img_thresh2)
        labels = self._thresh_and_label(img_thresh2)

        # discriminate based on expected properties
        labels_work = labels
        labels_large = []

        self.MIN_FEATURE_AREA = int(self.MIN_FEATURE_AREA)
        self.MAX_BBOX_OVERLAP = float(self.MAX_BBOX_OVERLAP)
        self.MAX_OVERLAP = float(self.MAX_OVERLAP)

        for region1 in labels:
            # remove very small features
            if region1.area < self.MIN_FEATURE_AREA:
                labels_work.remove(region1)
                continue

            # remove obvious artifacts (features with too low width / height ratio)
            dim = region1.dim
            ratio = min(dim[0], dim[1]) / max(dim[0], dim[1])
            if ratio < 0.1:
                labels_work.remove(region1)
                continue

            # remove overlapping features
            for region2 in labels:
                if region1 == region2:
                    continue
                if region1.bboxarea > region2.bboxarea:
                    continue

                overlap = region1.overlap(region2)
                if (overlap[3] >= self.MAX_OVERLAP or overlap[2] >= self.MAX_BBOX_OVERLAP) and region1 in labels_work:
                    labels_work.remove(region1)
                    break

            # if the feature is large, save it for the next pass
            if region1.area >= self.LARGE_FEATURE_AREA:
                region1.is_unclear = True
                labels_large.append(region1)

        labels = labels_work

        # pass to break up "large" features
        for region in labels_large:
            img_slice = img_mixed[region.br1:region.br2, region.bc1:region.bc2]
            t, img_thresh = cv2.threshold(img_slice, thresh_st2, thresh_end, cv2.THRESH_BINARY_INV)
            labels_new = self._thresh_and_label(img_thresh)

            # translate the newly found features with respect to their slice coordinates
            for f in labels_new:
                f.move(region.bx1 + f.x, region.by1 + f.y)

            labels = labels + labels_new

        # final pass to remove overlapping features
        labels_work = labels
        for region1 in labels:
            if region1.is_unclear == True:
                continue

            for region2 in labels:
                if region1 == region2:
                    continue
                if region1.bboxarea > region2.bboxarea:
                    continue
                if region2.is_unclear == True:
                    continue

                overlap = region1.overlap(region2)
                if (overlap[2] >= self.MAX_BBOX_OVERLAP) and region1 in labels_work:
                    #labels_work.remove(region1)
                    break

        labels = labels_work

        #print('len(labels)', len(labels))
        self.list = labels

    def _thresh_and_label(self, img):
        median = np.median(img)
        lower = int(max(0, (1.0 - float(self.CSIGMA)) * median))
        upper = int(min(255, (1.0 + float(self.CSIGMA)) * median))
        bin_edges = cv2.Canny(img, lower, upper)

        return self._feature_extract_edges(bin_edges)
