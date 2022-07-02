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
            "進む":self.get_next_page
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
        return Ingredient(self.data["ingredients_list"], self.order).return_data()

    def get_start_page(self):
        """
        ページの順番に関する単語を命令としたとき、データ(self.data["preparation_list"])から該当ページの情報を返す
        :return: 
        """
        return Page(self.data).return_data()

    def get_next_page(self):
        """
        ページの順番に関する単語を命令としたとき、データ(self.data["preparation_list"])から該当ページの情報を返す
        :return: 
        """
        return Page(self.data["preparation_list"]).return_data()

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
    i = {
        "history": "鴨南蛮をﾘｰｽﾞﾅﾌﾞﾙで手軽な鶏もも肉で作ってみたところ、家族に好評！温かいうどんの定番ﾒﾆｭｰになりました❤",
        "history_title": "このレシピの生い立ち",
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
        },
        "ingredients_title": "材料",
        "memo": "麺つゆを控えめにして、その分だしを追加。素材の味を活かした優しい味付けになってます。",
        "memo_title": "コツ・ポイント",
        "preparation_list": {
            "1": {
                "description": "鶏もも肉は余分な脂肪を除いて8等分。油揚げは油抜きして4等分。舞茸は小分けする。三つ葉･長葱は 洗って切る。",
                "help_links": [
                    {
                        "油抜き": {
                            "description": "油で揚げてある材料（油揚げ、厚揚げ、さつま揚げなど）を熱湯でさっと茹でるか、熱湯をまわしかけるかして、表面に残る油を取り除くこと。油臭さが抜け、味のしみこみがよくなります。いなり寿司のように、油揚げ自体にしっかり味を染み込ませる場合は、1〜2分茹でて油抜きをします。水気をよく絞ってから調味します。",
                            "help_links": [],
                            "image": [
                                "https://img.cpcdn.com/cms_article_images/12776/560/8751cbe9c249275346cad1a02fde5e3c?p=1434342519"
                            ],
                            "title": "油抜きとは"
                        }
                    }
                ],
                "image": [
                    "https://img.cpcdn.com/steps/12151943/m/94d426ec6b1d70971bb81854cf8dae2e?u=4038599&p=1376194163"
                ]
            },
            "2": {
                "description": "ﾌﾗｲﾊﾟﾝを熱して、鶏もも肉の皮を下にして焦げ色が付くまで焼く。その後、長葱と舞茸を入れて鶏から出る脂で焼く。",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/12151944/m/16461f039ef5bda0260de9893129c2e6?u=4038599&p=1376194172"
                ]
            },
            "3": {
                "description": "鶏もも肉･舞茸･長ﾈｷﾞの両面に、美味しそうな焼き色が付いたらOK。",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/12151945/m/9b0bbd7e69a4e2dab9ca7900e8248c95?u=4038599&p=1376194182"
                ]
            },
            "4": {
                "description": "鍋につゆの材料を入れて沸騰したら、うどんを入れて再沸騰させる。その後、具を全部入れて煮立ったら火を止める。",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/12151953/m/e4ead46bfd61daa8f1655c006518fb29?u=4038599&p=1376194319"
                ]
            },
            "5": {
                "description": "器にうどんを入れて、具を盛り付け、熱々のつゆをかけたら出来上がり★お好みでゆず入り七味唐辛子 を振りかけて下さいね。",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/12151952/m/e69130beeef67daf1b67241dc717a181?u=4038599&p=1445658488"
                ]
            },
            "6": {
                "description": "Yahooﾊﾟｿｺﾝ版ﾄｯﾌﾟﾍﾟｰｼﾞ、ｽﾎﾟｯﾄﾗｲﾄｺｰﾅｰにて2015年2月6日にﾚｼﾋﾟが紹介されました。",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/15692918/m/123fda410854154f8c0085d72d46a219?u=4038599&p=1423298483"
                ]
            },
            "7": {
                "description": "★話題入り感謝★2015.3.9話題入りしました。作って下さり、つくれぽ届けて下さった方々ありがとうございました❤",
                "help_links": [
                    {}
                ],
                "image": [
                    "https://img.cpcdn.com/steps/16054361/m/ab6339713177a344c68c9c459669c49b?u=4038599&p=1426651282"
                ]
            }
        },
        "preparation_title": "作り方",
        "title": "簡単♫ほっこり優しい味✿鶏南蛮うどん✿"
    }
    j = {
        "0": {
            "history": "鴨南蛮をﾘｰｽﾞﾅﾌﾞﾙで手軽な鶏もも肉で作ってみたところ、家族に好評！温かいうどんの定番ﾒﾆｭｰになりました❤",
            "history_title": "このレシピの生い立ち",
            "ingredients": {
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
            },
            "ingredients_title": "材料",
            "memo": "麺つゆを控えめにして、その分だしを追加。素材の味を活かした優しい味付けになってます。",
            "memo_title": "コツ・ポイント",
            "title": "簡単♫ほっこり優しい味✿鶏南蛮うどん✿"
        },
        "1": {
            "description": "鶏もも肉は余分な脂肪を除いて8等分。油揚げは油抜きして4等分。舞茸は小分けする。三つ葉･長葱は洗っ て切る。",
            "help_links": [
                {
                    "油抜き": {
                        "description": "油で揚げてある材料（油揚げ、厚揚げ、さつま揚げなど）を熱湯でさっと茹でるか、熱湯をまわしかけるかして、表面に残る油を取り除くこと。油臭さが抜け、味のしみこみがよくなります。いなり寿司のように、油揚げ自体にしっかり味を染み込ませる場合は、1〜2分茹でて油抜きをします。水気をよく絞ってから調味します。",
                        "help_links": [],
                        "image": [
                            "https://img.cpcdn.com/cms_article_images/12776/560/8751cbe9c249275346cad1a02fde5e3c?p=1434342519"
                        ],
                        "title": "油抜きとは"
                    }
                }
            ],
            "image": [
                "https://img.cpcdn.com/steps/12151943/m/94d426ec6b1d70971bb81854cf8dae2e?u=4038599&p=1376194163"
            ]
        },
        "2": {
            "description": "ﾌﾗｲﾊﾟﾝを熱して、鶏もも肉の皮を下にして焦げ色が付くまで焼く。その後、長葱と舞茸を入れて鶏から出る脂で焼く。",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/12151944/m/16461f039ef5bda0260de9893129c2e6?u=4038599&p=1376194172"
            ]
        },
        "3": {
            "description": "鶏もも肉･舞茸･長ﾈｷﾞの両面に、美味しそうな焼き色が付いたらOK。",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/12151945/m/9b0bbd7e69a4e2dab9ca7900e8248c95?u=4038599&p=1376194182"
            ]
        },
        "4": {
            "description": "鍋につゆの材料を入れて沸騰したら、うどんを入れて再沸騰させる。その後、具を全部入れて煮立ったら火を止める。",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/12151953/m/e4ead46bfd61daa8f1655c006518fb29?u=4038599&p=1376194319"
            ]
        },
        "5": {
            "description": "器にうどんを入れて、具を盛り付け、熱々のつゆをかけたら出来上がり★お好みでゆず入り七味唐辛子を振 りかけて下さいね。",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/12151952/m/e69130beeef67daf1b67241dc717a181?u=4038599&p=1445658488"
            ]
        },
        "6": {
            "description": "Yahooﾊﾟｿｺﾝ版ﾄｯﾌﾟﾍﾟｰｼﾞ、ｽﾎﾟｯﾄﾗｲﾄｺｰﾅｰにて2015年2月6日にﾚｼﾋﾟが紹介されました。",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/15692918/m/123fda410854154f8c0085d72d46a219?u=4038599&p=1423298483"
            ]
        },
        "7": {
            "description": "★話題入り感謝★2015.3.9話題入りしました。作って下さり、つくれぽ届けて下さった方々ありがとうございました❤",
            "help_links": [
                {}
            ],
            "image": [
                "https://img.cpcdn.com/steps/16054361/m/ab6339713177a344c68c9c459669c49b?u=4038599&p=1426651282"
            ]
        }
    }
    list_j = ['最初', 'スタート', '進む', '前', '戻る', '最後', '終わり']
    order = input("命令は: ")
    while order != "停止":
        data = j if order in list_j else i
        o = Order(order, data)
        order = input("命令は: ")

