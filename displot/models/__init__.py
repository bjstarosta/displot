# -*- coding: utf-8 -*-
"""Models module.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import os
import errno
import importlib
import logging


log = logging.getLogger('displot')

PATH_MODELS = os.path.dirname(os.path.abspath(__file__))


def path(model_id, basename=False):
    """Return a path to a model schema with relevant identifiers.

    Args:
        model_id (str): Model identifier.
        basename (bool): If False, an absolute path will be returned.
            If True, only the filename will be returned.

    Returns:
        str: Path to file or full filename.

    """
    bn = model_id + '.py'
    if basename is True:
        return bn
    else:
        return os.path.join(PATH_MODELS, bn)


def load_model(model_id):
    """Load a model schema using the given identifier.

    Loads the target file, runs the build() function and returns the result.
    The vars parameter gets unpacked as named arguments and passed to the
    build() function.

    Args:
        model_id (str): Model identifier.

    Returns:
        module: Python module of the loaded model.

    """
    if model_exists(model_id):
        log.info('Loading model `{0}`.'.format(model_id))
        mod = importlib.import_module('displot.models.' + model_id)
        return mod
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path(model_id))


def list_models(with_desc=False):
    """List all model schemas present in the directory.

    Args:
        with_desc (bool): If True, the returned list will be a list of tuples
            containing dataset ID, dataset __doc__.

    Returns:
        list: List of model identifiers.

    """
    lst = []
    for f in os.listdir(PATH_MODELS):
        if not f.endswith('.py'):
            continue
        if f in ['__init__.py']:
            continue
        f_ = os.path.splitext(f)[0]
        if with_desc is True:
            mod = importlib.import_module('displot.models.' + f_)
            lst.append((f_, mod.__doc__))
        else:
            lst.append(f_)
    return sorted(lst)


def model_exists(model_id):
    """Check if a given model schema exists.

    Args:
        model_id (str): The identifier of the model.

    Returns:
        bool: True if model schema exists, False otherwise.

    """
    return os.path.exists(path(model_id))
