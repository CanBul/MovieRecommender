from app import app
from flask import Flask, jsonify, request
from app.recommender import my_ids, get_preferences, point_table
from app.funkrecommender import FunkSVD
import warnings
warnings.filterwarnings("ignore")

@app.route("/flask", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        data = []
        try:
            points = request.get_json()
            mylist = my_ids(points)
            points = get_preferences(points)
            data = point_table(points, mylist,20)

            return jsonify(data)

        except:
            return jsonify(data)

    else:
        return jsonify({'movie_id': 'tmb6324', 'predicted_rating': 8.2})


@app.route("/funk", methods=['GET', 'POST'])
def funk():
    if request.method == 'POST':
        data = []

        try:
            points = request.get_json()

            MyFunk = FunkSVD(points)
            data = MyFunk.get_recommendation()

        except:
            data.append({'movie_id': 'tm12345', 'expected_rating': 8.3})
        return jsonify(data)
    else:
        return jsonify({'movie_id': 'tmb6324', 'predicted_rating': 8.2})
