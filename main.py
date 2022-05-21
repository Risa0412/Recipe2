import json
from crawler.builder import Builder
from tags import Tags


class Manager:
    def __init__(self):
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
        # soup = b.get_data(f'https://cookpad.com{url}')
        soup = b.get_data('https://cookpad.com/cooking_basics/12073')
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

    def get_result(self):
        param = {
            'indent': 4,
            'sort_keys': True,
            'default': str,
            'ensure_ascii': False
        }
        print(json.dumps(self.result, **param))


if __name__ == '__main__':
    m = Manager()
    runtime = {
        'ingredients': {
            'func': 'get_ingredients_row',
            'params': {
                'id': 'ingredients',
                'category': 'ingredients_title',
                'tag': 'h2',
                'param': {'class': 'recipe_heading'}
            }
        },
        'steps': {
            'func': 'get_steps',
            'params': {
                'id': 'steps_wrapper',
                'category': 'preparation_title',
                'tag': 'h2',
                'param': {'class': 'recipe_heading'}
            }
        },
        'memo': {
            'func': 'get_memo_history',
            'params': {
                'id': 'memo_wrapper',
                'category': 'memo_title',
                'tag': 'h3'
            }
        },
        'history': {
            'func': 'get_memo_history',
            'params': {
                'id': 'history_wrapper',
                'category': 'history_title',
                'tag': 'h3'
            }
        }
    }

    # urls = ['https://cookpad.com/recipe/2312038', 'https://cookpad.com/recipe/7099551', 'https://cookpad.com/recipe/6960335', 'https://cookpad.com/recipe/7158352', 'https://cookpad.com/recipe/2312110']
    urls = ['https://cookpad.com/recipe/2312038']

    for url in urls:
        m.get_soup(url)
        m.get_recipe_title()
        m.runtime(runtime)
        m.get_result()

    # text cleaning: '/n'


'''
https://cookpad.com/cooking_basics/12073
https://cookpad.com/cooking_basics/5343
https://cookpad.com/cooking_basics/20521
https://cookpad.com/cooking_basics/11347
https://cookpad.com/cooking_basics/5071
'''