class Ingredients:
    def __init__(self, data, order):
        self.data = data
        self.order = order
        self.result = []

    def prepare_data(self):
        """
        データのディクショナリがdefaultのとき、結果リストの先頭に配置する
        :return: 
        """
        if self.data.get("default"):
            self.result.extend(
                f'{ingredient}は{measure}' 
                for (ingredient, measure) in self.data["default"].items()
            )
            del self.data["default"]

    def get_ingredients(self):
        """
        データから大項目の材料名に必要な材料の情報を結果リストに追加する
        :return: 
        """
        for category, ingredients in self.data.items():
            self.result.append(f'{category}の材料は')
            self.result.extend(
                f'{ingredient}は{measure}' 
                for (ingredient, measure) in ingredients.items()
            )

    def return_data(self):
        """
        引数のデータから、データ処理する関数と、結果を取得する関数を実行する
        :return: 
        """
        self.prepare_data()
        self.get_ingredients()
        return self.result

    