from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import sys


class MainWindow(QMainWindow):
    def __init__(self, url, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        # self.browser.setUrl(QUrl(url))

        # timer = QTimer()
        # timer.timeout.connect(self.append)
        self.page = self.browser.page()
        # self.page.loadFinished.connect(lambda: timer.start(4000))
        self.page.setUrl(QUrl(url))

        self.setCentralWidget(self.browser)

        self.show()
        self.get_order()

    def get_order(self):
        import json
        import sys
        sys.path.append('..')
        from order import Order

        with open('../120827325313727089740978093670340282809289569548.json', encoding='utf-8') as file:
            i = json.load(file)
        with open('../page_120827325313727089740978093670340282809289569548.json', encoding='utf-8') as file:
            j = json.load(file)
        list_j = ['最初', 'スタート', '進む', '前', '戻る', '次', '最後', '終わり']
        order = input("命令は: ")
        page_position = None
        while order != "停止":
            data = j if order in list_j else i
            o = Order(order, data, page_position)
            data = o.runtime()
            self.append(data)
            if order in list_j:
                page_position = o.page_position
            order = input("命令は: ")

    def append(self, data):
        # self.page.runJavaScript(f"document.getElementById('global_announce_wrapper').innerHTML = '<p>{self.page.url().toString()}</p>'")
        add = []
        for d in data:
            if isinstance(d, list):
                add.extend([f'<img src="{img}">' for img in d])
            else:
                add.append(f'<p>{d}</p>')
        print(add)
        self.page.runJavaScript(f"document.getElementById('global_announce_wrapper').innerHTML += '{'<br>'.join(add)}'")


if __name__ == '__main__':
    url = 'https://cookpad.com/'

    app = QApplication(sys.argv)
    window = MainWindow(url)

    app.exec_()

    


'''
self.reference = {
    "材料":self.get_ingredients, 
    "ざいりょう":self.get_ingredients, 
    "ザイリョウ":self.get_ingredients, 
    "最初":self.get_start_page,
    "スタート":self.get_start_page,
    "次":self.get_next_page,
    "進む":self.get_next_page,
    "戻る":self.get_before_page,
    "前":self.get_before_page,
    "最後":self.get_last_page,
    "サイゴ":self.get_last_page,
    "さいご":self.get_last_page
    }
    '''