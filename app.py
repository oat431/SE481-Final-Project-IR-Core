from flask import Flask, request, jsonify
from flask_cors import cross_origin
from service.search_service import *

app = Flask(__name__)


@app.route('/all-recipe')
def get_all_songs():
    pass


@app.route('/search-recipe', methods=['POST'])
@cross_origin()
def get_recipe_by_title():
    return jsonify(search_recipe(request.json['query'], request.json['type']))


if __name__ == '__main__':
    app.run()
