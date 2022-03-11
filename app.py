from flask import Flask, request, jsonify
from flask_cors import cross_origin,CORS
from service.search_service import *

app = Flask(__name__)
CORS(app)

@app.route('/all-recipe')
def get_all_songs():
    pass


@app.route('/search-recipe', methods=['POST'])
@cross_origin()
def get_recipe_by_title():
    print(jsonify(search_recipe(request.json['query'], request.json['type'])))
    return jsonify(search_recipe(request.json['query'], request.json['type']))


if __name__ == '__main__':
    app.run()
