from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

import sys


class MainWindow(QMainWindow):
    def __init__(self, url, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        # self.browser.setUrl(QUrl(url))

        timer = QTimer()
        timer.timeout.connect(self.append)
        self.page = self.browser.page()
        self.page.loadFinished.connect(lambda: timer.start(4000))
        self.page.setUrl(QUrl(url))

        self.setCentralWidget(self.browser)

        self.show()

    def append(self):
        self.page.runJavaScript(f"document.getElementById('global_announce_wrapper').innerHTML = '<p>{self.page.url().toString()}</p>'")


if __name__ == '__main__':
    url = 'https://cookpad.com/'

    app = QApplication(sys.argv)
    window = MainWindow(url)

    app.exec_()
