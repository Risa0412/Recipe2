class Ingredients:
    def __init__(self, data):
        self.data = data
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

    