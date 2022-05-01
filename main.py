from ast import Param
from cgitb import text
from email.mime import image
import json
from turtle import title
from crawler.builder import Builder


class Manager:
    def __init__(self):
        self.result = {}

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
        self.result[category] =  self.ig.find(tag, param if param else '').getText().strip()

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
            description = row.find('p')
            a_links = description.find_all('a', href=True)
            help_links = {}
            if a_links:
                for link in a_links:
                    help_links[link.getText().strip()] = self.get_basic_cooking(link['href'])
            self.result['preparation_list'][step_num] = {'image':image, 'description':description.getText().strip(), 'help_links':help_links}

    def get_memo_history(self):
        self.result[self.category.split('_')[0]] = self.ig.find('div', {'class': 'text_content'}).getText().strip()

    def get_basic_cooking(self, url):
        # article_wrapper show
        # https://cookpad.com/cooking_basics/6190
        b = Builder()
        # soup = b.get_data(f'https://cookpad.com{url}')
        soup = b.get_data(f'https://cookpad.com/cooking_basics/20523')
        article = soup.find('div', {'class': 'article_wrapper'})
        title = article.find('h1', {'class': 'title_border'}).getText().strip()
        descriptions = article.find('div', {'class': 'main_content'}).find_all()
        text = {}
        for tag in descriptions:
            print(tag.name)
        # for counter, description in enumerate(descriptions):
        #     images = []
        #     get_images = description.find_all('img')
        #     if get_images:
        #         for image in get_images:
        #             images.append(image['src'])
        #     text[counter] = {'description': description.getText().strip(), 'image': images}
        return {'title': title, 'description': text}


    # argsはディクショナリ型。
    def runtime(self, args):
        for values in args.values():
            # 「**」はディクショナリ型の中からキー値を取得する（Unpacking）
            self.get_content(**values['params'])
            # self＝Class, メソッド内の関数名
            getattr(self, values['func'])()

    def get_result(self):
        param = {
            'indent':4,
            'sort_keys':True, 
            'default':str,
            'ensure_ascii':False
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


