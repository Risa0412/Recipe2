
class Pagination:
    def __init__(self, data):
        self.data = data

    def type_page(self):
            """
            ページ情報の順番を定義する
            :return: dic

            title
            history_title
            history
            memo_title
            memo
            ingredients_title
            ingredients
            """
            sequence = {
                0: {
                    "title": self.data['title'],
                    "history_title": self.data['history_title'],
                    "history": self.data['history'],
                    "memo_title": self.data['memo_title'],
                    "memo": self.data['memo'],
                    "ingredients_title": self.data['ingredients_title'],
                    "ingredients_list": self.data['ingredients_list']
                }
            }

            for num, step_info in enumerate(self.data['preparation_list'].values(), 1):
                sequence[num] = step_info

            return sequence
