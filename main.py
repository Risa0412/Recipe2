import json
from tools.tools import Hash
from crawler.builder import Builder
from tags import Tags


class Manager:
    def __init__(self):
        self.param_json = {
            'indent': 4,
            'sort_keys': True,
            'default': str,
            'ensure_ascii': False
        }
        self.result = {}
        self.reference = {
            "p": "description",
            "span": "description",
            "img": "image",
            "a": "help_links"
        }

    def get_soup(self, url):
        b = Builder()
        self.soup = b.get_data(url)
        
    def soup(self):
        return self.soup

    def get_recipe_title(self):
        self.result['title'] = self.soup.find('h1', {'class': 'recipe-title'}).getText().strip()

    def get_content(self, id, category, tag, param=None):
        self.ig = self.soup.find('div', {'id': id})
        self.category = category
        self.result[category] = self.ig.find(tag, param or '').getText().strip()

    def get_ingredients_row(self):
        il = self.ig.find('div', {'id': 'ingredients_list'})
        rows = il.find_all('div', {'class': 'ingredient_row'})

        self.result['ingredients_list'] = {}
        category = 'default'
        for row in rows:
            if 'ingredient_category' in str(row):
                category = row.getText().strip().split('\n')[-1]
            
            if not self.result['ingredients_list'].get(category):
                self.result['ingredients_list'][category] = {}

            if 'ingredient_name' in str(row):
                data = row.getText().strip().split('\n')
                self.result['ingredients_list'][category][data[0]] = data[1]

    def get_steps(self):
        il = self.ig.find('div', {'id': 'steps'})
        rows = il.find_all('li')

        self.result['preparation_list'] = {}

        for row in rows:
            step_num = row.find('dt', {'class': 'step_number'}).getText().strip()
            image = row.find('img')['data-large-photo'] if row.find('img') else ''
            descriptions = row.find('p')
            description = descriptions.getText().strip()
            a_links = descriptions.find_all('a', href=True)
            help_links = {}
            if a_links:
                for link in a_links:
                    help_links[link.getText().strip()] = self.get_basic_cooking(link['href'])
            var_dict = {'image':[], 'description':"", 'help_links':[]}
            for key in var_dict:
                if isinstance(var_dict[key], str):
                    var_dict[key] += eval(key)
                elif isinstance(var_dict[key], list):
                    var_dict[key].append(eval(key))

            self.result['preparation_list'][step_num] = var_dict


    def get_memo_history(self):
        self.result[self.category.split('_')[0]] = self.ig.find('div', {'class': 'text_content'}).getText().strip()

    def get_basic_cooking(self, url):
        # article_wrapper show
        # https://cookpad.com/cooking_basics/6190
        b = Builder()
        soup = b.get_data(f'https://cookpad.com{url}')
        # soup = b.get_data('https://cookpad.com/cooking_basics/12073')
        article = soup.find('div', {'class': 'article_wrapper'})

        self.tags = Tags()
        title = self.tags.heading(article.find('h1', {'class': 'title_border'}))
        descriptions = article.find('div', {'class': 'main_content'})
        text = {
            'title': title,
            "description": "",
            "image": [],
            "help_links": []
        }
        self.get_child_tags(descriptions, text)
        return text

    def get_child_tags(self, parent, text):
        for tag in parent.find_all(recursive=False):
            to_add = getattr(self.tags, 'heading' if tag.name.startswith('h') else tag.name)(tag)
            if to_add not in text[self.reference[tag.name]]:
                if isinstance(text[self.reference[tag.name]], str):
                    text[self.reference[tag.name]] += to_add
                elif isinstance(text[self.reference[tag.name]], list):
                    text[self.reference[tag.name]].append(to_add)

            self.get_child_tags(tag, text)

    # @staticmethod
    # def add_data(var, data):
    #     if isinstance(var, str):
    #         var += data
    #     elif isinstance(var, list):
    #         var.append(data)

    def runtime(self, args):
        """

        :param args: argsはディクショナリ型。
        :return:
        """
        for values in args.values():
            # 「**」はディクショナリ型の中からキー値を取得する（Unpacking）
            self.get_content(**values['params'])
            # self＝Class, メソッド内の関数名
            getattr(self, values['func'])()
        
        # ファイルの作成
        self.save_recipe(Hash(self.result['title']).get_hash())        

    def save_recipe(self, filename, data=None):
        data = self.result if not data else data
        with open(f'{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, **self.param_json)


if __name__ == '__main__':
    m = Manager()
    runtime = json.load(open("runtime.json"))

    # urls = ['https://cookpad.com/recipe/2312038', 'https://cookpad.com/recipe/7099551', 'https://cookpad.com/recipe/6960335', 'https://cookpad.com/recipe/7158352', 'https://cookpad.com/recipe/2312110']
    urls = ['https://cookpad.com/recipe/2312038']

    for url in urls:
        m.get_soup(url)
        m.get_recipe_title()
        m.runtime(runtime)

    # text cleaning: '/n'


'''
https://cookpad.com/cooking_basics/12073
https://cookpad.com/cooking_basics/5343
https://cookpad.com/cooking_basics/20521
https://cookpad.com/cooking_basics/11347
https://cookpad.com/cooking_basics/5071


{
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
'''