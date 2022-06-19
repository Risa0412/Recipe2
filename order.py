class Order:
    def __init__(self, order, data):
        self.order = order
        self.data = data
        self.reference = {
            "材料":self.ingredients, 
            "ざいりょう":self.ingredients, 
            "ザイリョウ":self.ingredients, 
            "最初":self.start_page,
            "スタート":self.start_page
            }
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
                    
    def start_page(self):
        result = []
        result.append(self.data["preparation_list"]["1"]['image'])
        describe = f'{self.announce_pages("1")}、{self.data["preparation_list"]["1"]["description"]}'
        if self.data["preparation_list"]["1"]['help_links']:
            for links in self.data["preparation_list"]["1"]['help_links']:
                describe = describe.replace(list(links.keys())[0], f'[red]{list(links.keys())[0]}[/red]')
        result.append(describe)
        return result
    
    def announce_pages(self, page_position):
        page_list = list(self.data["preparation_list"].keys())
        reference = {"1":"最初に", page_list[-1]:"最後に"}
        return reference.get(page_position, f'{page_position}、次に')

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
    o = Order(input("命令は: "), i)

