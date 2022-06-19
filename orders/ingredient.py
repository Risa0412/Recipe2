class Ingredient:
    def __init__(self, data, order):
        self.data = data
        self.order = order
        self.result = []

    def get_ingredient(self):
        """
        データから、各材料において必要な分量を取得する
        :return: 
        """
        for category, ingredients in self.data.items():
            # self.orderと"default"以外のタイトルと比較
            if self.order in category:
                # 読取りwordがタイトルのとき、全ての材料名と分量を読み上げ return
                self.result.append(f'{category}の材料は')
                self.result.extend(
                    f'{ingredient}は{measure}' 
                    for (ingredient, measure) in ingredients.items()
                )

            else:
                self.result.extend(
                    f'{f"{category}に使う" if category != "default" else ""}{ingredient}は{measure}'  
                    for ingredient, measure in ingredients.items()
                    if self.order in ingredient
                )
                # 読取りwordと材料名を順番に比較
                # for ingredient, measure in ingredients.items():
                #     # 読取りwordが材料名のとき、
                #     if self.order in ingredient:
                #         # "default"以外の材料名であるとき、

                #         # タイトルと材料名と分量を読み上げreturn
                #         result.append(
                #             f'{f"{category}に使う" if category != "default" else ""}{ingredient}は{measure}'                    
                #         )
                        # "default"の材料名であるとき、

                            # 材料名と分量を読み上げreturn
                        
                    # 読取りwordがどちらでもないとき、false
    def return_data(self):
        """
        引数のデータから、データ処理する関数と、結果を取得する関数を実行する
        :return: 
        """
        self.get_ingredient()
        if not self.result:
            return "この命令は見つかりませんでした。"

        return self.result

