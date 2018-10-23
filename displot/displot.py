# -*- coding: utf-8 -*-
if __name__ == '__main__':
    from ui import DisplotUi


displotInfo = {
    'appTitle': 'displot',
    'appVersion': 'pre-alpha',
    'author': 'Bohdan Starosta',
    'authorEmail': 'bjstarosta@gmail.com',
    'projectPage': 'https://github.com/bjstarosta/displot/'
}

if __name__ == '__main__':
    UI = DisplotUi(displotInfo)
    UI.run()
