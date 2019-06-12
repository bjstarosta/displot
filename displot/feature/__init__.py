# -*- coding: utf-8 -*-
import sys
import os

import numpy as np
from skimage import measure
import matplotlib.patches as mpatches


def scan_methods():
    dir = os.path.dirname(__file__)
    methods = []
    for f in os.listdir(dir):
        if f.endswith('.py') and f != '__init__.py':
            methods.append(os.path.splitext(f)[0])
    return methods

__all__ = scan_methods()

def get_methods():
    methods = __all__
    ret = {}
    for m in methods:
        m2 = getattr(sys.modules[globals()['__name__']], m)
        c = getattr(m2, m)
        ret[c.__name__] = c()
    return ret


class FeatureExtractor(object):
    """Abstract class for feature extraction methods.

    Attributes:
        desc (string): A short one sentence description of the extraction method.
        flist (list): List of Feature objects detailing found features.
        image (ndarray): A numpy 2d array containing image data to be analysed.
        image_debug (dict): A dictionary of image snapshots for detailed
            observations of the feature selection process.

    """

    def __init__(self):
        self.desc = None

        self.factory = FeatureFactory()
        self.list = None
        self.image = None
        self.image_debug = [[], []]

    def set_image_data(self, ndarray):
        self.image = ndarray

    def get_feature_list(self):
        if self.list is None:
            raise FeatureExtractorException('Image has not been scanned for features.')
        return self.list

    def run(self):
        pass

    def clear_debug(self):
        self.image_debug = [[], []]

    def debug(self, plt):
        titles = ['Original', 'Marked']
        images = [self.image, self.image]

        for k, v in enumerate(self.image_debug[0]):
            titles.append(v)
            images.append(self.image_debug[1][k])

        rt = np.sqrt(len(images))
        rt_floor = int(np.floor(rt))
        rt_ceil = int(np.ceil(rt))

        ncols = rt_floor
        nrows = rt_floor
        if rt > rt_floor + 0.5:
            ncols = rt_ceil
        if rt > rt_floor:
            nrows = rt_ceil

        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True, figsize=(12, 10))
        for i, img in enumerate(images):
            k = i % ncols
            if nrows == 1 and ncols == 1:
                axi = ax
            elif nrows > 1:
                j = int(np.floor(i / ncols))
                axi = ax[j, k]
            else:
                axi = ax[k]

            if i == 1 and self.list is not None:
                for region in self.list:
                    minr, minc, maxr, maxc = region.bbox
                    if region.is_unclear == True:
                        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='green', linewidth=2)
                        axi.add_patch(rect)
                    else:
                        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
                        axi.add_patch(rect)

            #print(np.max(img), img.shape)
            axi.imshow(img, interpolation='nearest', cmap=plt.cm.gray)
            axi.set_title(titles[i], fontsize=10)
            axi.set_xticks([])
            axi.set_yticks([])

        fig.suptitle(self.desc, fontsize=14)
        fig.tight_layout()
        #plt.show()

    def _image_debug_save(self, name, ndarray):
        self.image_debug[0].append(name)
        self.image_debug[1].append(ndarray)

    def _feature_extract_edges(self, bin_edges):
        bin_labels = measure.label(bin_edges)
        labels = measure.regionprops(bin_labels, coordinates='rc')
        out = []
        for region in labels:
            obj = self.factory.factory(region.centroid, region.bbox, region)
            out.append(obj)
        return out

    def _feature_scale(self, img, a, b, type=None):
        """Statistical feature scaling.

        Args:
            img (ndarray): A 2-dim numpy array containing the image data.
            a (int or float): Minimum threshold value.
            b (int or float): Maximum threshold value.
            type: Type to cast the resulting array into.

        Returns:
            ndarray: The feature scaled image.
        """
        min = np.min(img)
        max = np.max(img)
        img = a + ((img - min) * (b - a)) / (max - min)
        if type is not None:
            img = img.astype(type)
        return img


class FeatureExtractorException(Exception):
    def __init__(self, errname, debug=None):
        self.errname = errname
        self.debug = debug

    def __str__(self):
        ret = repr(self.errname)
        if self.debug is not None:
            ret += "\n------------------\nDebug:\n------------------"
            if type(self.debug) is dict:
                for k, v in self.debug.items():
                    ret += "\n" + str(k) + ': ' + str(v)
            else:
                ret += repr(debug)
        return ret

    def error(self):
        return self.errname


class Feature(object):
    def __init__(self, pos=(0,0), bbox=(0,0,0,0), regionprops=None):
        self.r = pos[0]
        self.c = pos[1]
        self.br1 = bbox[0]
        self.bc1 = bbox[1]
        self.br2 = bbox[2]
        self.bc2 = bbox[3]
        self.confidence = None
        self.is_unclear = False
        self.cluster_id = 0

        self.regionprops = regionprops

        if self.regionprops is None:
            return

        self.convex_image = self.regionprops.convex_image

    @property
    def x(self): return self.c
    @property
    def y(self): return self.r
    @property
    def bx1(self): return self.bc1
    @property
    def by1(self): return self.br1
    @property
    def bx2(self): return self.bc2
    @property
    def by2(self): return self.br2
    @x.setter
    def x(self, x): self.c = x
    @y.setter
    def y(self, y): self.r = y
    @bx1.setter
    def bx1(self, x): self.bc1 = x
    @by1.setter
    def by1(self, y): self.br1 = y
    @bx2.setter
    def bx2(self, x): self.bc2 = x
    @by2.setter
    def by2(self, y): self.br2 = y

    @property
    def dimrc(self): return (self.br2 - self.br1, self.bc2 - self.bc1)
    @property
    def dim(self): return (self.bx2 - self.bx1, self.by2 - self.by1)
    @property
    def area(self): return self.regionprops.area
    @property
    def bboxarea(self): return (self.bx2 - self.bx1) * (self.by2 - self.by1)
    @property
    def bboxrc(self): return (self.br1, self.bc1, self.br2, self.bc2)
    @property
    def bbox(self): return (self.bx1, self.by1, self.bx2, self.by2)

    def move(self, x, y):
        """Changes the centroid coordinates of the feature.

        Args:
            x (int): The x-coordinate in pixels.
            y (int): The y-coordinate in pixels.

        """
        x_diff = x - self.x
        y_diff = y - self.y
        self.bx1 = int(round(self.bx1 + x_diff))
        self.bx2 = int(round(self.bx2 + x_diff))
        self.by1 = int(round(self.by1 + y_diff))
        self.by2 = int(round(self.by2 + y_diff))
        self.x = x
        self.y = y

    def transform(self, m):
        """Applies a transformation matrix to the feature.

        Args:
            m (ndarray): A 2D transformation matrix.

        """
        if m.shape != (2, 2):
            raise FeatureException('Transformation matrix shape should be 2x2.', {'transform_matrix': m})

        self.x, self.y = m @ np.array([self.x, self.y])
        self.bx1, self.by1 = m @ np.array([self.bx1, self.by1])
        self.bx2, self.by2 = m @ np.array([self.bx2, self.by2])

    def slice(self, image, radius):
        """Returns an ndarray slice containing a square snapshot of the feature
        coordinates.

        Args:
            image (ndarray): The image from which to retrieve the snapshot.
            radius (int): The horizontal radius of the square (from its centre)
                that will be sliced out of the image.

        """
        pass

    def overlap(self, feature, bbox_only=False):
        """Calculates bounding box overlap and pixelwise overlap between two regions.

        Note that although the percentage parameters return values with respect to the
        combined area of the union of the two features, if the algorithm detects full
        overlap the percentage parameters will return 1 (100%) to indicate this,
        even if the actual overlap percentage of the intersect wth respect to the union
        would be smaller because the two features might not necessarily be of the same
        size.

        Args:
            feature (Feature): The feature to compare against.
            bbox_only (bool): Consider bounding box overlap only to simplify calculations.

        Returns:
            tuple: (number of intersecting bbox pixels,
                number of intersecting pixels,
                percentage of intersecting bbox pixels (w/ respect to the union),
                percentage of intersecting pixels (w/ respect to the union))
        """

        if bbox_only == False and (self.convex_image is None or feature.convex_image is None):
            raise FeatureExtractorException('Both features must have a convex image to compare overlap.')

        # Bounding box intersection coordinates
        ir1, ic1 = (max(self.br1, feature.br1), max(self.bc1, feature.bc1))
        ir2, ic2 = (min(self.br2, feature.br2), min(self.bc2, feature.bc2))

        # No bounding box overlap
        if ir1 >= ir2 or ic1 >= ic2:
            return 0, 0, 0, 0
        # Total bounding box overlap
        elif ir1 == self.br1 and ic1 == self.bc1 and ir2 == self.br2 and ic2 == self.bc2:
            bbox_intersect = self.bboxarea
            bbox_intersect_prc = 1
        elif ir1 == feature.br1 and ic1 == feature.bc1 and ir2 == feature.br2 and ic2 == feature.bc2:
            bbox_intersect = feature.bboxarea
            bbox_intersect_prc = 1
        # Partial bounding box overlap
        else:
            bbox_intersect = (ir2 - ir1) * (ic2 - ic1)
            bbox_union = self.bboxarea + feature.bboxarea - bbox_intersect
            bbox_intersect_prc = bbox_intersect / bbox_union

        if bbox_only == True:
            return bbox_intersect, None, bbox_intersect_prc, None

        # Bounding box union coordinates
        ur1, uc1 = (min(self.br1, feature.br1), min(self.bc1, feature.bc1))
        ur2, uc2 = (max(self.br2, feature.br2), max(self.bc2, feature.bc2))

        overlap_slice1 = np.full((ur2 - ur1, uc2 - uc1), False)
        overlap_slice2 = np.full((ur2 - ur1, uc2 - uc1), False)

        # Calculate relative coordinates
        size_self_r, size_self_c = self.dimrc
        size_feature_r, size_feature_c = feature.dimrc

        self_br1, self_bc1 = (max(0, self.br1 - feature.br1), max(0, self.bc1 - feature.bc1))
        self_br2, self_bc2 = (self_br1 + size_self_r, self_bc1 + size_self_c)
        feature_br1, feature_bc1 = (max(0, feature.br1 - self.br1), max(0, feature.bc1 - self.bc1))
        feature_br2, feature_bc2 = (feature_br1 + size_feature_r, feature_bc1 + size_feature_c)

        # Place the binary maps in positions relative to each other on the two slices
        try:
            overlap_slice1[self_br1:self_br2, self_bc1:self_bc2] = self.convex_image
            overlap_slice2[feature_br1:feature_br2, feature_bc1:feature_bc2] = feature.convex_image
        except ValueError as e:
            raise FeatureExtractorException("Image data slicing failed due to incorrect array dimensions or coordinates.", {
                "self.dim": self.dim,
                "feature.dim": feature.dim,
                "overlap_slice1_xy": (overlap_slice1.shape[1], overlap_slice1.shape[0]),
                "self_rel_bbox": (self_br1, self_bc1, self_br2, self_bc2),
                "feature_rel_bbox": (feature_br1, feature_bc1, feature_br2, feature_bc2)
            }) from e

        # Find the intersection of the binary maps
        overlap = np.logical_and(overlap_slice1, overlap_slice2)
        overlap_pixels = np.count_nonzero(overlap == True)
        area1 = np.count_nonzero(overlap_slice1 == True)
        area2 = np.count_nonzero(overlap_slice2 == True)

        if overlap_pixels == area1 or overlap_pixels == area2:
            overlap_prc = 1
        else:
            overlap_prc = overlap_pixels / (area1 + area2 - overlap_pixels)

        return bbox_intersect, overlap_pixels, bbox_intersect_prc, overlap_prc

    def similarity(self, feature, bbox_only=False):
        """Calculates feature similarity.

        Args:
            feature (Feature): The feature to compare against.
            bbox_only (bool): Consider positional similarity only.

        """

        pass


class FeatureException(FeatureExtractorException):
    pass


class FeatureFactory(object):
    def __init__(self):
        self.bc = Feature

    def setBaseClass(self, c):
        self.bc = c

    def getBaseClass(self):
        return self.bc.__name__

    def factory(self, *args, **kwargs):
        return self.bc(*args, **kwargs)
