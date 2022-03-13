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
    return jsonify(search_recipe(request.json['query'], request.json['type']))


@app.route('/search-mark',methods=['POST'])
@cross_origin()
def get_mark_recipe_by_title():
    return jsonify(search_mark_recipe(request.json['query']))


@app.route('/recipe/<int:id>')
@cross_origin()
def get_recipe_by_id(id):
    return jsonify(get_recipe_details(id))


@app.route('/see-mark-recipe',methods=["POST"])
@cross_origin()
def get_user_mark_recipe():
    return jsonify(get_mark_recipe(request.json['mark']))


if __name__ == '__main__':
    app.run()
