from os import remove
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import sys


class MainWindow(QMainWindow):
    def __init__(self, url, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.url = ''
        self.browser = QWebEngineView()
        self.browser.resize(990, 800)
        # self.browser.setUrl(QUrl(url))

        # timer = QTimer()
        # timer.timeout.connect(self.append)
        self.page = self.browser.page()
        self.page.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

        self.show()
        # self.page.clicked.connect(self.get_current_url)
        self.page.loadFinished.connect(self.edit_size)
        self.page.loadFinished.connect(self.remove_ad)
        self.browser.focusProxy().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.browser.focusProxy() and event.type() == event.MouseButtonPress:
            self.page.loadStarted.connect(self.get_current_url)
            print("☆☆", self.url, self.page.history().currentItem().url().toString())
            if "recipe" in self.url:
                self.get_order()  # "recipe"が含まれているURLのみ実行する
        return super(MainWindow, self).eventFilter(obj, event)

    def get_order(self):
        import json
        import sys
        sys.path.append('..')
        from order import Order
        from main import Manager
        m = Manager()
        runtime = json.load(open("runtime.json"))

        m.get_soup(self.url)
        m.get_recipe_title()
        filename = m.runtime(runtime)

        # self.page.url().toString()
        with open(f'../{filename}.json', encoding='utf-8') as file:
            i = json.load(file)
        with open(f'../page_{filename}.json', encoding='utf-8') as file:
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
                _img = d[0]
            else:
                add.append(f'<p>{d}</p>')
                _text = d
        print(add)
        template = f'<div style="clear: left;"><div class="large_photo_content large_photo_dialog enable_large portrait type_step"><div class="large_photo_content_title recipe_title">お月見だんごで郷土のおやつ しんこだんご</div><div class="main"><h3 class="large_photo_title"></h3><div class="user_name"><a class="author recipe_author_container" href="/kitchen/15123348"><img src="https://img.cpcdn.com/users/15123348/40x40c/f08986b6fa158df228de18956d6d8a80?u=15123348&amp;p=1521126337" width="20" height="20" alt="薩摩のやすねこ" class="author_icon">薩摩のやすねこ</a></div><div class="large_photo_container"><div class="large_photo_wrapper"><img class="large_photo" style="height:70%; max-width:600px;" src="{_img}"></div><div class="large_photo_info"><div class="large_photo_description"><p>{_text}</p></div><div class="large_photo_contributor"></div></div></div><div class="dialog_bottom"><div class="page_count">4 / 6</div></div></div></div></div>'
        # self.page.runJavaScript(f"document.getElementById('contents').innerHTML = '{'<br>'.join(add)}'")
        self.page.runJavaScript(f"document.getElementById('contents').innerHTML = '{template}'")

    def remove_ad(self):
        # search_footer_wrapper: ad_wrapper
        tags = {
            "getElementsByClassName": "ad_wrapper",
            "getElementById": "side"
        }
        for element, tag in tags.items():
            self.page.runJavaScript(
                f"[...document.{element}('{tag}')].map(n => n && n.remove())" 
                if element == 'getElementsByClassName' 
                else f"document.{element}('{tag}').remove()"
        )

    def edit_size(self):
        self.page.runJavaScript("document.getElementById('main').style.width = '780px';")
        self.page.runJavaScript("document.getElementById('container').style.width = '780px';")
        self.page.runJavaScript("document.getElementById('main-photo').style.height = 'auto';")
        self.page.runJavaScript("document.getElementById('main-photo').style.max-height = 'null';")
        self.page.runJavaScript("document.getElementById('main-photo').style.max-width = '100%';")

    def get_current_url(self):
        self.url = self.page.url().toString()
        



if __name__ == '__main__':
    url = 'https://cookpad.com/'

    app = QApplication(sys.argv)
    window = MainWindow(url)

    app.exec_()

    

    '''
    2022/09/11 今後 やること
    ・綺麗なデザインにする
    ・広告を消す

horizontal_rectangles clearfix
id="side"
id="contents"
    '''