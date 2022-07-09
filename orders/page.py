class Page:
    def __init__(self, data):
        self.data = data
        self.result = []
        self.page_list = list(self.data.keys())
            
    def start_page(self):
        """
        最初のページの情報を取得する
        :return: 
        """
        self.result.append(self.data[1]['image'])
        describe = f'{self.announce_pages(1)}、{self.data[1]["description"]}'
        if self.data[1]['help_links']:
            for links in self.data[1]['help_links']:
                describe = describe.replace(list(links.keys())[0], f'[red]{list(links.keys())[0]}[/red]')
        self.result.append(describe)

    def next_page(self):
        """
        次のページの情報を取得する
        :return:
        """
        # self.result.append(self.data[])
        pass
    
    def last_page(self):
        """
        最後のページの情報を取得する
        :return: 
        """
        page_num = self.page_list[-1]
        self.result.append(self.data[page_num]['image'])
        describe = f'{self.announce_pages(page_num)}、{self.data[page_num]["description"]}'
        if self.data[page_num]['help_links']:
            for links in self.data[page_num]['help_links']:
                describe = describe.replace(list(links.keys())[0], f'[red]{list(links.keys())[0]}[/red]') if links else describe 
        self.result.append(describe)

    def announce_pages(self, page_position):
        """
        ページ番号に応じた文言を返す
        :return: 
        """
        reference = {1:"最初に", self.page_list[-1]:"最後に"}
        return reference.get(page_position, f'{page_position}、次に')

    def return_data(self):
        """
        引数のデータから、データ処理する関数と、結果を取得する関数を実行する
        :return: 
        """
        return self.result