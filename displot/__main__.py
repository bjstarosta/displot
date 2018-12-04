# -*- coding: utf-8 -*-
"""Displot launcher file.

Note:
    Displot is written using Python 3 and may not work using Python 2.

Example:
    Run the program by running this file in python from the command line.

        $ python -m displot.py

"""

import sys
import re
import urllib.request
import ssl
import webbrowser

from displot.ui import DisplotUi, GenericDialog
from displot.config import DISPLOT_INFO


def check_releases(info):
    """Performs a check on the repository to see whether it needs to nag the
    user to update his release.

    Args:
        info (dict): Program metadata.

    """

    check_url = 'https://raw.githubusercontent.com/bjstarosta/displot/master/displot/displot.py'

    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        with urllib.request.urlopen(check_url, context=ssl_context, timeout=3) as handle:
            contents = str(handle.read())
    except urllib.error.URLError as err:
        print("Couldn't check for new version. Error: ({}) {}".format(
            err.code, err.reason))
        return

    repo_test = re.search(r"'appVersion': '([a-zA-Z0-9-_\.]+)',", contents)
    if repo_test is None:
        return

    ver = repo_test.group(1)
    if ver == info['appVersion']:
        return

    msg = 'Version <b>{}</b> is available in the repository. '
    msg += 'Your version is <b>{}</b>. '
    msg += 'Click <i>OK</i> to go to the repository page to update your program, '
    msg += 'or click <i>Cancel</i> to continue using this version for the moment.'
    msg = msg.format(ver, info['appVersion'])

    dlg = GenericDialog()
    dlg.setText(msg)
    dlg.setAccept(lambda: webbrowser.open(info['projectPage']))
    dlg.setAccept(sys.exit)
    dlg.show()
    dlg.exec_()

def main():
    check_releases(DISPLOT_INFO)
    UI = DisplotUi(DISPLOT_INFO)
    UI.run()

if __name__ == "__main__":
    main()
