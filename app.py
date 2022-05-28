
import json
from main import Manager
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.get("/recipe/")
async def root(recipe: str):
    runtime = json.load(open("runtime.json"))
    m = Manager()

    m.get_soup(recipe)
    m.get_recipe_title()
    m.runtime(runtime)
    return m.get_result()
    # return {"message": "a"}
    

'''
uvicorn app:app --reload
url = 'https://cookpad.com/recipe/2312038'
http://127.0.0.1:8000/recipe/{url}?recipe=https://cookpad.com/recipe/2312038
'''