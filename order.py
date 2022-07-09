from orders.ingredients import Ingredients
from orders.ingredient import Ingredient
from orders.page import Page


class Order:
    def __init__(self, order, data):
        self.order = order
        self.data = data
        self.reference = {
            "材料":self.get_ingredients, 
            "ざいりょう":self.get_ingredients, 
            "ザイリョウ":self.get_ingredients, 
            "最初":self.get_start_page,
            "スタート":self.get_start_page,
            "次":self.get_next_page,
            "進む":self.get_next_page,
            "最後":self.get_last_page,
            "サイゴ":self.get_last_page,
            "さいご":self.get_last_page
            }
        self.runtime()

    def get_ingredients(self):  
        """
        大項目の材料名を命令としたとき、データ(self.data["ingredients_list"])から材料の情報を返す
        :return: 
        """
        return Ingredients(self.data["ingredients_list"], self.order).return_data()

    def get_ingredient(self):
        """
        各材料名を命令としたとき、データ(self.data["ingredients_list"])から材料の情報を返す
        :return: 
        """
        print(self.data.keys())
        return Ingredient(self.data["ingredients_list"], self.order).return_data()

    def get_start_page(self):
        """
        ページの順番に関する単語を命令としたとき、データ(self.data["preparation_list"])から該当ページの情報を返す
        :return: 
        """
        p = Page(self.data)
        p.start_page()
        return p.return_data()

    def get_next_page(self):
        """
        ページの順番に関する単語を命令としたとき、データ(self.data["preparation_list"])から該当ページの情報を返す
        :return: 
        """
        return Page(self.data["preparation_list"]).return_data()

    def get_last_page(self):
        """
        ページの順番に関する単語を命令としたとき、データ(self.data["preparation_list"])から該当ページの情報を返す
        :return: 
        """
        p = Page(self.data)
        p.last_page()
        return p.return_data()

    def error(self):
        return f'「{self.order}」は材料に含まれません。'

    def runtime(self):
        func = self.reference.get(self.order, self.get_ingredient)
        result = func()
        if isinstance(result, str):
            print(result)
        elif isinstance(result, list):
            for re in result:
                print(re)

    
if __name__ == '__main__':
    from pagination import Pagination
    import json
    with open('120827325313727089740978093670340282809289569548.json', encoding='utf-8') as file:
        i = json.load(file)
    list_j = ['最初', 'スタート', '進む', '前', '戻る', '最後', '終わり']
    order = input("命令は: ")
    while order != "停止":
        data = Pagination(i).type_page() if order in list_j else i
        o = Order(order, data)
        order = input("命令は: ")

