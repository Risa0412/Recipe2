class Page:
    def __init__(self, data, page_num=None):
        self.data = data
        self.result = []
        self.page_list = list(self.data.keys())
        self.page_num = page_num if page_num else self.page_list[1]
    
    def start_page(self):
        self.page_num = self.page_list[1]

    def last_page(self):
        self.page_num = self.page_list[-1]

    def next_page(self):
        """
        次のページの情報を取得する
        :return:
        """
        self.page_num = self.page_list[self.page_list.index(self.page_num) + 1]
        return self.page_num
    
    def get_page(self):
        """
        最後のページの情報を取得する
        :return: 
        """
        self.result.append(self.data[self.page_num]['image'])
        describe = f'{self.announce_pages(self.page_num)}、{self.data[self.page_num]["description"]}'
        if self.data[self.page_num]['help_links']:
            for links in self.data[self.page_num]['help_links']:
                describe = describe.replace(list(links.keys())[0], f'[red]{list(links.keys())[0]}[/red]') if links else describe 
        self.result.append(describe)

    def announce_pages(self, page_position):
        """
        ページ番号に応じた文言を返す
        :return: 
        """
        reference = {self.page_list[1]:"最初に", self.page_list[-1]:"最後に"}
        return reference.get(page_position, f'{page_position}、次に')

    def page_position(self):
        print(self.page_num)
        return self.page_num

    def return_data(self):
        """
        引数のデータから、データ処理する関数と、結果を取得する関数を実行する
        :return: 
        """
        self.get_page()
        return self.result, self.page_num