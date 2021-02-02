# -*- coding: utf-8 -*-
"""displot - Handling of different image types.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import os
import io
import csv
import json
import tarfile
import time

import numpy as np
import imageio
try:
    import skimage.external.tifffile as tifffile
except ImportError:
    import tifffile


def _load_image(path, obj):
    """Load an image from disk into a data object.

    Args:
        path (str): Path to image.
        obj (io.DisplotData): Data object to populate with the data.

    Returns:
        io.DisplotData: Displot data object.

    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if os.path.isdir(path):
        raise IsADirectoryError(path)
    if not os.access(path, os.R_OK):
        raise PermissionError(path)

    ext = os.path.splitext(path)[1].lower()
    obj.image_path = path

    if ext == '.tiff' or ext == '.tif':
        with tifffile.TiffFile(path) as tif:
            obj.image = tif.asarray()
            obj.image_meta = {}
            for f in tif.flags:
                obj.image_meta[f] = getattr(tif, f + '_metadata')

    elif ext == '.png':
        obj.image = imageio.imread(path)

    else:
        raise RuntimeError(path)

    # strip all channels except the first one
    if len(obj.image.shape) > 2:
        obj.image = np.copy(obj.image[:, :, 0])

    return obj


def _load_dpfile(path, obj):
    """Load a displot data file from disk into a data object.

    Args:
        path (str): Path to image.
        obj (io.DisplotData): Data object to populate with the data.

    Returns:
        io.DisplotData: Displot data object.

    """
    a = tarfile.open(path, 'r')
    objjson_f = a.extractfile('dp.json')
    objjson = json.loads(str(objjson_f.read(), 'ascii'))
    obj.fromDict(objjson)

    image_f = a.extractfile(os.path.basename(objjson['image_path']))
    with tifffile.TiffFile(image_f) as tif:
        obj.image = tif.asarray()

    return obj


def _save_dpfile(path, obj):
    """Save a displot data object as a file to disk.

    Args:
        path (str): Path to image.
        obj (io.DisplotData): Data object to populate with the data.

    Returns:
        None

    """
    objjson = bytes(json.dumps(obj.toDict()), 'ascii')

    objjson_info = tarfile.TarInfo(name='dp.json')
    objjson_info.size = len(objjson)
    objjson_info.type = tarfile.REGTYPE
    objjson_info.mtime = int(time.time())
    objjson_info.mode = 0o0755

    a = tarfile.open(path, 'w')
    a.add(obj.image_path, os.path.basename(obj.image_path))
    a.addfile(tarinfo=objjson_info, fileobj=io.BytesIO(objjson))
    # a.list()
    a.close()


def _save_csv(path, obj):
    """Save data object features as a CSV file.

    Args:
        path (str): Path to image.
        obj (io.DisplotData): Data object to populate with the data.

    Returns:
        None

    """
    objdict = obj.toDict()

    with open(path, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=objdict['markers'][0].keys())
        writer.writeheader()
        for row in objdict['markers']:
            writer.writerow(row)
