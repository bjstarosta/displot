# -*- coding: utf-8 -*-
"""Tensorflow interface functions.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import logging
import numpy as np
import tensorflow as tf

import displot.models as models
import displot.weights as weights

log = logging.getLogger('displot')


def predict(X, model_id, weights_id):
    """Output predictions for input samples using selected trained model.

    Args:
        X (numpy.ndarray): Input data to use for predictions.
        model_id (str): Model identifier in string format.
        weights_id (tuple): Weights file identifier in tuple of strings format.
            The tuple should be of the form: (model_id, iteration_id).

    Returns:
        numpy.ndarray: Predictions.

    """
    model = models.load_model(model_id)
    model_nn = weights.load_weights(weights_id[0], weights_id[1])

    single_image = False
    if len(X.shape) == 2:
        single_image = True
        X = np.array([X])

    X = model.pack_data(X)
    log.debug(
        "after pack: min(X)={0}, max(X)={1}, avg(X)={2}, var(X)={3}".format(
            np.min(X), np.max(X), np.average(X), np.var(X)
        )
    )

    pred = model_nn.predict(X)
    log.debug(
        "after predict: min(X)={0}, max(X)={1}, avg(X)={2}, var(X)={3}".format(
            np.min(pred), np.max(pred), np.average(pred), np.var(pred)
        )
    )

    pred = model.unpack_data(pred)

    if single_image is True:
        pred = np.squeeze(pred)

    return pred
    
    
def detect_gpu_support():
    """Output information about the state of GPU support to STDERR.

    Returns:
        None

    """
    if not tf.test.is_built_with_cuda():
        log.warning("Tensorflow is not built with CUDA.")
        return
    pgpus = tf.config.list_physical_devices('GPU')
    log.info(
        "Physical GPUs: {0}".format(len(pgpus))
    )

