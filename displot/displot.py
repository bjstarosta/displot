# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import os, sys, re
    import urllib.request
    import webbrowser

    from ui import DisplotUi, GenericDialog


displot_info = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha',
    'author': 'Bohdan Starosta',
    'authorEmail': 'bjstarosta@gmail.com',
    'projectPage': 'https://github.com/bjstarosta/displot/'
}

def checkReleases(info):
    verCheckUrl = 'https://raw.githubusercontent.com/bjstarosta/displot/master/displot/displot.py'

    try:
        with urllib.request.urlopen(verCheckUrl, timeout=3) as h:
            contents = str(h.read())
    except urllib.error.URLError as e:
        print("Couldn't check for new version. Error: ({}) {}".format(e.code, e.reason))
        return

    m = re.search("'appVersion': '([a-zA-Z0-9-_\.]+)',", contents)
    if m == None:
        return

    ver = m.group(1)
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
    dlg.setAccept(lambda: sys.exit())
    dlg.show()
    dlg.exec_()

def main():
    checkReleases(displot_info)
    UI = DisplotUi(displot_info)
    UI.run()

if __name__ == '__main__':
    main()
