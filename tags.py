class Tags:
    def __init__(self):
        pass

    def heading(self, soup):
        return soup.getText().strip()

    def img(self, soup):
        return soup['src']

    def a(self, soup):
        return f"{soup.getText().strip()}: {soup['href']}"

    def p(self, soup):
        return soup.getText().strip()

'''
p
a
h1
h2
h3
img
'''