class Order:
    def __init__(self, order, data):
        self.order = order
        self.data = data
        self.reference = {"材料":self.ingredients, "ざいりょう":self.ingredients, "ザイリョウ":self.ingredients}
        self.runtime()

    def ingredients(self):
        result = []
        if self.data["ingredients_list"].get("default"):
            result.extend(
                f'{ingredient}は{measure}' 
                for (ingredient, measure) in self.data["ingredients_list"]["default"].items()
            )
            del self.data["ingredients_list"]["default"]

        for category, ingredients in self.data["ingredients_list"].items():
            result.append(f'{category}の材料は')
            result.extend(
                f'{ingredient}は{measure}' 
                for (ingredient, measure) in ingredients.items()
            )
        return result

    def ingredient(self):
        result = []
        for category, ingredients in self.data["ingredients_list"].items():
            # self.orderと"default"以外のタイトルと比較
            if self.order in category:
                # 読取りwordがタイトルのとき、全ての材料名と分量を読み上げ return
                result.append(f'{category}の材料は')
                result.extend(
                    f'{ingredient}は{measure}' 
                    for (ingredient, measure) in ingredients.items()
                )

            else:
                result.extend(
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


        if not result:
            return self.error

        return result
                    

    def error(self):
        return f'「{self.order}」は材料に含まれません。'

    def runtime(self):
        func = self.reference.get(self.order, self.ingredient)
        result = func()
        if isinstance(result, str):
            print(result)
        elif isinstance(result, list):
            for re in result:
                print(re)

    
if __name__ == '__main__':
    i = {
        "ingredients_list": {
            "default": {
                "茹でうどん(冷凍うどん)": "4人分"
            },
            "つゆ": {
                "みりん": "50ml",
                "和風粉末だし": "1袋",
                "水": "1200ml",
                "麺つゆ(2倍濃縮)": "200ml"
            },
            "具": {
                "三つ葉(5㎝に切る)": "1袋",
                "油揚げ(1枚を4等分に切る)": "2枚",
                "舞茸(小分けする)": "1株",
                "長葱(12等分に切る)": "1本",
                "鶏もも肉(8等分に切る)": "1枚"
            }
        }
    }
    o = Order(input("命令は: "), i)
