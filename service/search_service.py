import pandas as pd

from model.bm25 import BM25
from service.spell_checker_service import spell_checking

food = pd.read_csv('./data/food.csv')
food.drop('Unnamed: 0', axis='columns', inplace=True)
food.drop('Ingredients', axis='columns', inplace=True)

bm25 = BM25()
bm25.fit(food["Title"].astype('U'))
mark25 = BM25()

mark = []


def search_by_bm25(query):
    result = bm25.transform(query, food["Title"].astype('U'))
    return result.argsort()[-50:][::-1]


def search_by_bm25_ingredient(ingredient):
    result = bm25.transform(ingredient, food["Cleaned_Ingredients"].astype('U'))
    return result.argsort()[-50:][::-1]


def search_by_bm25_instruction(instr):
    result = bm25.transform(instr, food["Instructions"].astype('U'))
    return result.argsort()[-50:][::-1]


def search_by_title(query):
    return_data = []
    result = search_by_bm25(query)
    for i in result:
        data = {
            'id': int(i),
            'title': food.iloc[i].to_dict()["Title"],
            'instructions': [x.lstrip().strip("'") for x in str(food.iloc[i].to_dict()["Instructions"]).split('.')],
            'image_Name': food.iloc[i].to_dict()["Image_Name"],
            'ingredients': [x.lstrip().strip("'") for x in
                            food.iloc[i].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
        }
        return_data.append(data)
    return return_data


def search_by_ingreidents(query):
    return_data = []
    result = search_by_bm25_ingredient(query)
    for i in result:
        data = {
            'id': int(i),
            'title': food.iloc[i].to_dict()["Title"],
            'instructions': [x.lstrip().strip("'") for x in str(food.iloc[i].to_dict()["Instructions"]).split('.')],
            'image_Name': food.iloc[i].to_dict()["Image_Name"],
            'ingredients': [x.lstrip().strip("'") for x in
                            food.iloc[i].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
        }
        return_data.append(data)
    return return_data


def search_by_instruciton(query):
    return_data = []
    result = search_by_bm25_instruction(query)
    for i in result:
        data = {
            'id': int(i),
            'title': food.iloc[i].to_dict()["Title"],
            'instructions': [x.lstrip().strip("'") for x in str(food.iloc[i].to_dict()["Instructions"]).split('.')],
            'image_Name': food.iloc[i].to_dict()["Image_Name"],
            'ingredients': [x.lstrip().strip("'") for x in
                            food.iloc[i].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
        }
        return_data.append(data)
    return return_data


def search_recipe(query, type):
    misspelled = spell_checking(query)
    if len(misspelled) != 0:
        return {"did_you_mean": [x for x in misspelled]}

    if type == 'ingredient':
        return search_by_ingreidents(query)

    if type == 'title':
        return search_by_title(query)

    if type == 'instruction':
        return search_by_instruciton(query)


def get_recipe_details(id):
    return {
        'id': int(id),
        'title': food.iloc[id].to_dict()["Title"],
        'instructions': [x.lstrip().strip("'") for x in str(food.iloc[id].to_dict()["Instructions"]).split('.')],
        'image_Name': food.iloc[id].to_dict()["Image_Name"],
        'ingredients': [x.lstrip().strip("'") for x in
                        food.iloc[id].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
    }


def get_mark_recipe(li):
    global mark
    mark = []
    for i in li:
        index = int(i)
        data = {
            'id': index,
            'title': food.iloc[index].to_dict()["Title"],
            'instructions': [x.lstrip().strip("'") for x in str(food.iloc[index].to_dict()["Instructions"]).split('.')],
            'image_Name': food.iloc[index].to_dict()["Image_Name"],
            'ingredients': [x.lstrip().strip("'") for x in
                            food.iloc[index].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
        }
        mark.append(data)
    return mark


def search_mark_recipe(query):
    print(mark)
    misspelled = spell_checking(query)
    if len(misspelled) != 0:
        return {"did_you_mean": [x for x in misspelled]}

    return_data = []
    mark_recipe = pd.DataFrame(mark)
    mark25.fit(mark_recipe["title"].astype('U'))
    result = bm25.transform(query, mark_recipe["title"].astype('U'))
    for i in result.argsort()[::-1]:
        index = int(i)
        data = {
            'id': index,
            'title': mark_recipe.iloc[index].to_dict()["title"],
            'instructions': [x.lstrip().strip("'") for x in str(mark_recipe.iloc[index].to_dict()["instructions"]).split('.')],
            'image_Name': mark_recipe.iloc[index].to_dict()["image_Name"],
            'ingredients': [x.lstrip().strip("'") for x in
                            mark_recipe.iloc[index].to_dict()["ingredients"]],
        }
        return_data.append(data)
    return return_data
