import pandas as pd

from sklearn import preprocessing
from sklearn import neighbors
from sklearn import tree
from sklearn import naive_bayes
from sklearn import model_selection
from sklearn import metrics

from numpy import hstack

import multiprocessing as mp

import string

import json
import re

import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

from model.bm25 import BM25
from service.spell_checker_service import spell_checking

food = pd.read_csv('./data/food.csv')
food.drop('Unnamed: 0', axis='columns',inplace=True)
food.drop('Ingredients', axis='columns',inplace=True)

bm25 = BM25()
bm25.fit(food["Title"].astype('U'))


def search_by_bm25(query):
    result = bm25.transform(query, food["Title"].astype('U'))
    return result.argsort()[-50:][::-1]


def search_by_title(query):
    misspelled = spell_checking(query)
    if len(misspelled) != 0:
        return {"did-you-mean": [x for x in misspelled]}

    return_data = []
    result = search_by_bm25(query)
    index = 0
    for i in result:
        index += 1
        data = {
            'id': index,
            'title': food.iloc[i].to_dict()["Title"],
            'instructions': [x for x in str(food.iloc[i].to_dict()["Instructions"]).split('.')],
            'image_Name': food.iloc[i].to_dict()["Image_Name"],
            'ingredients': [x for x in food.iloc[i].to_dict()["Cleaned_Ingredients"].strip("][").split(',')],
        }
        return_data.append(data)
    return return_data
