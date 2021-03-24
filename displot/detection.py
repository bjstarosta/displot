# -*- coding: utf-8 -*-
"""displot - Threading dislocation detection logic.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import logging
import functools
import multiprocessing as mp

import numpy as np
import skimage.feature

from displot.io import DisplotDataFeature
import displot.tf

log = logging.getLogger('displot')


def detection(
    image, weights, model='fusionnet', stride=(256, 256),
    min_r=5, max_r=14,
    min_sigma=3, max_sigma=15, num_sigma=15, threshold=.1,
    td_border=3, td_overlap=2, pred_tolerance=0.33,
    _qt5signals=None
):
    """Perform machine learning assisted detection of dislocations on an image.

    See 'skimage.feature.blob_log' for more information about the blob
    detection process.

    Args:
        image (numpy.ndarray): Image to process. Must be in numpy array format.
        weights (tuple): Neural network weight file to use.
            Must be a tuple of two strings. See displot.weights.
        model (str): Neural network model to use. See displot.models.
        stride (tuple): Sliding window stride in (row, column) format.
            Must be a tuple of two integers.
        min_r (int): Minimum blob radius.
        max_r (int): Maximum blob radius.
        min_sigma (int): Blob detection parameter.
            Minimum standard deviation for Gaussian kernel.
        max_sigma (int): Blob detection parameter.
            Maximum standard deviation for Gaussian kernel.
        num_sigma (int): Blob detection parameter.
            Number of intermediate values of standard deviations to consider
            between min_sigma and max_sigma.
        threshold (float): Blob detection parameter.
            The absolute lower bound for scale space maxima. Local maxima
            smaller than thresh are ignored. Reduce this to detect blobs
            with less intensities.
        td_border (int): Remove all TDs within this many pixels of the border.
        td_overlap (int): Allow this many pixels of overlap between blobs.
        pred_tolerance (float): Prune all TDs below this confidence value.

    Returns:
        tuple: (list of DisplotDataFeature, float: average pred. conf.)

    """
    progress = 0
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 0%

    # Get rid of extraneous dimension.
    if len(image.shape) == 3:
        image = np.squeeze(image)

    hw = (512, 512)  # height, width of sliding window
    # stride = (256, 256)  # row, column of sliding window stride

    # Calculate proper padding so that the predictions can be stiched together
    l_pad = stride[1]
    t_pad = stride[0]
    r_pad = stride[1] - (image.shape[1] % stride[1])
    b_pad = stride[0] - (image.shape[0] % stride[0])
    if r_pad % hw[1] > 0:
        r_pad += stride[1]
    if b_pad % hw[0] > 0:
        b_pad += stride[0]

    padding = (l_pad, t_pad, r_pad, b_pad)
    log.debug('l_pad, t_pad, r_pad, b_pad: {0}'.format(padding))
    log.debug('image.shape (before pad): {0}'.format(image.shape))

    # Pad image to get correct stride coverage
    image_padded = np.pad(image, ((t_pad, b_pad), (l_pad, r_pad)), 'constant',
        constant_values=((0, 0), (0, 0)))
    log.debug('image.shape (after pad): {0}'.format(image.shape))

    passes = np.zeros((
        int(image_padded.shape[0] / stride[0]),
        int(image_padded.shape[1] / stride[1])
    ))
    log.debug('passes.shape: {0}'.format(passes.shape))

    # Build array of image inputs for prediction using a sliding window
    X = []
    for r in range(0, image_padded.shape[0] - stride[0], stride[0]):
        for c in range(0, image_padded.shape[1] - stride[1], stride[1]):

            r_ = int(r / stride[0])
            c_ = int(c / stride[1])
            passes[r_:r_ + 2, c_:c_ + 2] += 1

            X.append(image_padded[r:r + hw[0], c:c + hw[1]])

    X = np.array(X)
    log.debug('X.shape: {0}'.format(X.shape))

    progress += 10
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 10%

    # Perform predictions
    log.info('Starting prediction.')
    try:
        Y = displot.tf.predict(X, 'fusionnet', weights)
    except Exception:
        log.error("Unrecoverable error.", exc_info=True)
        exit(1)

    log.info('Prediction complete.')
    log.debug('Y.shape: {0}'.format(Y.shape))

    progress += 40
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 50%

    # Stitch the predictions into 4 separate blob images.
    # Find blobs as well while iterating over the predictions.
    n_row = int(image_padded.shape[0] / stride[0]) - 1
    n_col = int(image_padded.shape[1] / stride[1]) - 1

    lo_row = np.floor(n_row / 2)
    hi_row = np.ceil(n_row / 2)
    lo_col = np.floor(n_col / 2)
    hi_col = np.ceil(n_col / 2)

    blob_l = np.zeros((int(hw[0] * hi_row), int(hw[1] * hi_col)))
    blob_t = np.zeros((int(hw[0] * hi_row), int(hw[1] * lo_col)))
    blob_r = np.zeros((int(hw[0] * lo_row), int(hw[1] * hi_col)))
    blob_b = np.zeros((int(hw[0] * lo_row), int(hw[1] * lo_col)))

    log.debug('blob_l.shape: {0}, blob_t.shape: {1}, '
        'blob_r.shape: {2}, blob_b.shape: {3}'.format(
            blob_l.shape, blob_t.shape, blob_r.shape, blob_b.shape
        )
    )

    log.info('Starting blob detection.')
    tds = []

    row = 0
    col = 0
    bd_funcs = []
    for i, Y_ in enumerate(Y):
        log.debug('ROW: {0}, COL: {1}'.format(row, col))
        Y_ = np.squeeze(Y_)

        if col % 2 == 0:
            x_i = col * stride[1]
        else:
            x_i = col * stride[1] - stride[1]
        log.debug('x_i: {0}'.format(x_i))

        if row % 2 == 0:
            y_i = row * stride[0]
            log.debug('y_i: {0}'.format(y_i))
            if i % 2 == 0:  # left
                blob_l[y_i:y_i + hw[0], x_i:x_i + hw[1]] = Y_
            else:  # top
                blob_t[y_i:y_i + hw[0], x_i:x_i + hw[1]] = Y_
        else:
            y_i = row * stride[0] - stride[0]
            log.debug('y_i: {0}'.format(y_i))
            if i % 2 == 0:  # bottom
                blob_b[y_i:y_i + hw[0], x_i:x_i + hw[1]] = Y_
            else:  # right
                blob_r[y_i:y_i + hw[0], x_i:x_i + hw[1]] = Y_

        bd_funcs.append(functools.partial(_blob_detect,
            Y_,
            x_offset=(col * stride[1]) - padding[0],
            y_offset=(row * stride[0]) - padding[1],
            min_sigma=min_sigma,
            max_sigma=max_sigma,
            num_sigma=num_sigma,
            threshold=threshold,
            min_r=min_r,
            max_r=max_r
        ))

        col += 1
        if col >= n_col:
            col = 0
            row += 1

        # progress += 50 / len(Y)

    with mp.Pool() as pool:
        bd_out = pool.map(_retcall, bd_funcs)

    for i in bd_out:
        tds.extend(i)

    progress += 50
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 100%

    log.info('Blob detection complete.')
    log.debug('TDs found initially: {0}'.format(len(tds)))

    return discrimination(
        image, tds,
        td_border, td_overlap, pred_tolerance, 4, _qt5signals
    )


def discrimination(
    image, tds=[],
    td_border=3, td_overlap=2, pred_tolerance=0.33,
    detect_samples=1,
    _qt5signals=None
):
    """Perform discrimination on a list of dislocations.

    Args:
        image (numpy.ndarray): Image to read properties from.
        tds (list): A list of DisplotDataFeature objects.
        td_border (int): Remove all TDs within this many pixels of the border.
        td_overlap (int): Allow this many pixels of overlap between blobs.
        pred_tolerance (float): Prune all TDs below this confidence value.
        detect_samples (int): Number of samples taken of the same image prior
            to discrimination. In effect this allows the function to expect
            this many overlapping features as standard, instead of treating
            them as an aberration. The function then merges these features
            together and averages their prediction confidence.

    Returns:
        tuple: (list of DisplotDataFeature, float: average pred. conf.)

    """

    progress = 0
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 0%

    tds_pruned = []

    log.info('Starting discrimination.')
    # First pass for bad candidates
    for i, td in enumerate(tds):
        # Prune border TDs as they are largely artifacts
        if (td.x <= td_border or td.x >= (image.shape[1] - td_border)
        or td.y < td_border or td.y >= (image.shape[0] - td_border)):
            continue

        # Prediction < 0.01 means pruned
        if td.confidence < 0.01:
            continue

        tds_pruned.append(td)

    progress += 50
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 50%

    # Second pass for prediction ranking

    # All dislocations should intersect four times with a very close neighbour
    # if this function is being run immediately after prediction.
    # We find those four times and use the one with highest pred then average
    # the pred confidence.
    tds_final = []
    tds_visited = []
    pred_avg = []

    for i, td in enumerate(tds_pruned):
        if i in tds_visited:
            continue

        overlap_list = [td]

        # find all overlapping TDs
        for j, td_ in enumerate(tds_pruned):
            dx = td.x - td_.x
            dy = td.y - td_.y
            d = np.hypot(dx, dy)
            if d >= (td.r + td_.r - td_overlap):
                continue

            overlap_list.append(td_)
            tds_visited.append(j)

        # sort by prediction confidence
        overlap_list = sorted(
            overlap_list,
            key=lambda x: x.confidence,
            reverse=True
        )

        # calculate averaged prediction confidence
        # prediction confidence should always be an average of 4 overlapping
        overlap_list = overlap_list[:detect_samples]
        pred_list = [x.confidence for x in overlap_list]
        pred_list += [0] * (detect_samples - len(overlap_list))
        pred = np.average(pred_list)

        # prune all TDs below set prediction tolerance
        if pred < pred_tolerance:
            continue

        # if we are here, it means TD looks valid and is added to the
        # output list.
        overlap_list[0].confidence = pred
        tds_final.append(overlap_list[0])
        pred_avg.append(pred)

    progress = 100
    if (callable(_qt5signals.progress)
    and hasattr(_qt5signals.progress, 'emit')):
        _qt5signals.progress.emit(progress)  # 100%

    log.info('Discrimination complete.')
    log.debug('TDs after pruning: {0}'.format(len(tds_final)))
    return tds_final, np.average(pred_avg)


def _blob_detect(
    im, x_offset, y_offset,
    min_sigma, max_sigma, num_sigma, threshold,
    min_r, max_r
):
    """Perform blob detection on an image data slice.

    See: https://scikit-image.org/docs/dev/api/skimage.feature.html

    Args:
        im (numpy.ndarray): Image slice to detect blobs on.
            Should be single channel greyscale for performance.
        x_offset (int): X coordinate of the image slice on the full image
            relative to its top left corner.
        y_offset (int): X coordinate of the image slice on the full image
            relative to its top left corner.
        min_sigma (int): Blob detection parameter.
            Minimum standard deviation for Gaussian kernel.
        max_sigma (int): Blob detection parameter.
            Maximum standard deviation for Gaussian kernel.
        num_sigma (int): Blob detection parameter.
            Number of intermediate values of standard deviations to consider
            between min_sigma and max_sigma.
        threshold (float): Blob detection parameter.
            The absolute lower bound for scale space maxima. Local maxima
            smaller than thresh are ignored. Reduce this to detect blobs
            with less intensities.
        min_r (int): Minimum blob radius.
        max_r (int): Maximum blob radius.

    Returns:
        list: List of DisplotDataFeature objects containing positional
            information about detected blobs.

    """

    tds = []

    # This line is very slow.
    blobs_log = skimage.feature.blob_log(
        im,
        min_sigma=min_sigma,
        max_sigma=max_sigma,
        num_sigma=num_sigma,
        threshold=threshold
    )

    # Compute blob radius and clip its values.
    blobs_log[:, 2] = np.clip(blobs_log[:, 2] * np.sqrt(2), min_r, max_r)

    for c_y, c_x, r in blobs_log:
        # Extract all pixel values within the blob radius.
        c_y = int(c_y)
        c_x = int(c_x)
        r_i = int(r)
        sq = im[c_y - r_i:c_y + r_i, c_x - r_i:c_x + r_i]

        pred_n = 0
        pred = 0
        for sq_r, sq_r_ in enumerate(sq):
            for sq_c, sq_c_ in enumerate(sq_r_):
                if (sq_r - r_i)**2 + (sq_c - r_i)**2 > r_i**2:
                    continue
                pred += sq[sq_r, sq_c]
                pred_n += 1

        # Average of pixel values within each blob radius is set as the
        # prediction confidence of that marker. This is because the
        # autoencoder delivers fainter blobs the more "unsure" it is.
        if pred_n > 0:
            pred = (pred / pred_n) / 255
        else:
            pred = 0

        td = DisplotDataFeature()
        td.x = c_x + x_offset
        td.y = c_y + y_offset
        td.r = r
        td.confidence = pred
        tds.append(td)

    return tds


def _retcall(f):
    return f()
