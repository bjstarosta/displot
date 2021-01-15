# -*- coding: utf-8 -*-
"""Displot launcher file.

Example:
    Run the program by running this file in python from the command line.

        $ python -m displot.py

"""

import os
import sys
import logging
import ssl
import json
import webbrowser
import urllib.request

from displot.ui import DisplotUi, GenericDialog, ConsoleHandler


def check_releases():
    """Perform a version check on the repository.

    If the repository has a new version on the master branch, a dialog window
    will be displayed reminding the user to update.
    """

    ch = 'https://raw.githubusercontent.com/bjstarosta/'\
        'displot/master/displot/meta.json'

    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with urllib.request.urlopen(ch, context=ssl_context, timeout=3) as h:
            meta_remote = str(h.read(), 'ascii')
    except urllib.error.URLError as err:
        print("Couldn't check for new version. Error: ({}) {}".format(
            err.code, err.reason))
        return

    try:
        meta_remote = json.loads(meta_remote)
    except json.decoder.JSONDecodeError as err:
        print("Couldn't load remote meta.json. Error: {}".format(err))

    meta_localpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'meta.json')
    with open(meta_localpath, 'r', encoding='utf-8') as f:
        meta_local = json.load(f)

    if meta_remote['app_version'] == meta_local['app_version']:
        return

    msg = "Version <b>{}</b> is available in the repository. Your version is "
    + "<b>{}</b>. Click <i>OK</i> to go to the repository page to update your "
    + "program, or click <i>Cancel</i> to continue using this version for the "
    + "moment."
    msg = msg.format(meta_remote['app_version'], meta_local['app_version'])

    dlg = GenericDialog()
    dlg.setText(msg)
    dlg.setAccept(lambda: webbrowser.open(meta_local['project_page']))
    dlg.setAccept(sys.exit)
    dlg.show()
    dlg.exec_()


def setup_logger(console):
    logger = logging.getLogger('displot')
    logger.setLevel(logging.INFO)

    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(message)s'))
    logger.addHandler(stream)

    console = ConsoleHandler(console)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        '[%(levelname)s] %(message)s'))
    logger.addHandler(console)


def main():
    check_releases()
    UI = DisplotUi()
    setup_logger(UI.console)
    UI.run()


if __name__ == "__main__":
    main()
