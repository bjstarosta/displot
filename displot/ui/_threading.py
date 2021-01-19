# -*- coding: utf-8 -*-
"""displot - UI threading using Qt5.

Author: Bohdan Starosta
University of Strathclyde Physics Department
"""

import sys
import traceback

from PyQt5 import QtCore


class WorkerSignals(QtCore.QObject):
    """Object containing signals usable from a running worker thread.

    Attributes:
        finished (QtCore.pyqtSignal): Accepts no data.
        error (QtCore.pyqtSignal): Accepts tuple. Usual format is:
            ( exception type, value, traceback.format_exc() )
        result (QtCore.pyqtSignal): Accepts any object type.
        progress (QtCore.pyqtSignal): Accepts int indicating progress percent.

    """

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)


class Worker(QtCore.QRunnable):
    """Worker thread object.

    Constructor accepts as arguments a callable function reference, followed by
    a list of arguments to pass to the function when calle.d

    Args:
        fn (callable): Function to call in a worker thread.

    Attributes:
        args (tuple): Arguments to pass to the callback function.
        kwargs (dict): Keywords to pass to the callback function.
        signals (WorkerSignals): Object containing emittable signals.
        fn

    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['_qt5signals'] = self.signals

    @QtCore.pyqtSlot()
    def run(self):
        """Run the worker using the passed function and arguments.

        Results will be communicated back to the main thread using signals.

        Returns:
            None

        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return processing result
        finally:
            self.signals.finished.emit()  # Done
