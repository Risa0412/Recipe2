from os import remove
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import sys


# ユーザがクリックした時のリンクを取得する為のクラス
class ClickedLink(QWebEnginePage):
    # 取得したリンクからアクションが起こせるかを返す（ＯＫ/ＮＧ）
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked and "recipe" in url.toString(): # QWebEnginePage.NavigationTypeLinkClicked：クリックしたところがリンクだったときのタイプ
            print(url.toString())
            self.get_order(url.toString())  # "recipe"が含まれているURLのみ実行する
        
        return super().acceptNavigationRequest(url,  _type, isMainFrame)

    def get_order(self, url):
        pyqtRemoveInputHook()
        import json
        from order import Order
        from data import Manager
        m = Manager()
        runtime = json.load(open("runtime.json"))

        m.get_soup(url)
        m.get_recipe_title()
        filename = m.runtime(runtime)

        with open(f'{filename}.json', encoding='utf-8') as file:
            i = json.load(file)
        with open(f'page_{filename}.json', encoding='utf-8') as file:
            j = json.load(file)
        list_j = ['最初', 'スタート', '進む', '前', '戻る', '次', '最後', '終わり']

        # エラー発生　QCoreApplication::exec: The event loop is already running
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
        add = []
        for d in data:
            if isinstance(d, list):
                add.extend([f'<img src="{img}">' for img in d])
                _img = d[0]
            else:
                add.append(f'<p>{d}</p>')
                _text = d
        template = f'<div style="clear: left;"><div class="large_photo_content large_photo_dialog enable_large portrait type_step"><div class="large_photo_content_title recipe_title">お月見だんごで郷土のおやつ しんこだんご</div><div class="main"><h3 class="large_photo_title"></h3><div class="user_name"><a class="author recipe_author_container" href="/kitchen/15123348"><img src="https://img.cpcdn.com/users/15123348/40x40c/f08986b6fa158df228de18956d6d8a80?u=15123348&amp;p=1521126337" width="20" height="20" alt="薩摩のやすねこ" class="author_icon">薩摩のやすねこ</a></div><div class="large_photo_container"><div class="large_photo_wrapper"><img class="large_photo" style="height:70%; max-width:600px;" src="{_img}"></div><div class="large_photo_info"><div class="large_photo_description"><p>{_text}</p></div><div class="large_photo_contributor"></div></div></div><div class="dialog_bottom"><div class="page_count">4 / 6</div></div></div></div></div>'
        self.page.runJavaScript(f"document.getElementById('contents').innerHTML = '{template}'")


# メインウインドウ
class MainWindow(QMainWindow):
    def __init__(self, url, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.resize(990, 800)
        _page = ClickedLink(self)
        self.browser.setPage(_page)

        # timer = QTimer()
        # timer.timeout.connect(self.append)
        self.page = self.browser.page()
        self.page.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

        self.show()
        self.page.loadFinished.connect(self.edit_size)
        self.page.loadFinished.connect(self.remove_ad)

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
        reference = {
            "main": [("width", "780px")],
            "container": [("width", "780px")],
            "main-photo": [("height", "auto"), ("max-height", "null"), ("max-width", "100%")]
        }
        for css_element, css_styles in reference.items():
            for css_style in css_styles:
                self.page.runJavaScript(f"document.getElementById('{css_element}').style.{css_style[0]} = '{css_style[1]}';") 


if __name__ == '__main__':
    url = 'https://cookpad.com/'

    app = QApplication(sys.argv)
    window = MainWindow(url)

    app.exec_()

