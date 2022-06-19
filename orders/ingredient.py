class Ingredients:
    def __init__(self) -> None:
        pass
        
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

