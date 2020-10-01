import pickle
import numpy as np
from app import app
from flask import Flask, jsonify, request
from app.recommender import my_ids, get_preferences, point_table
from app.funkrecommender import FunkSVD
import warnings
warnings.filterwarnings("ignore")
base = '/home/canbulguoglu/app/'


def get_neighbour(city, features):
    city_feature = features[city]
    results = []
    all_movies = [x for x in features]
    for each in all_movies:
        z1 = np.dot(city_feature, features[each])
        sigmoid = 1/(1+np.exp(-z1))
        if sigmoid > 0.6:
            if each == city:
                continue
            results.append([each, round(sigmoid, 2)])
    results.sort(reverse=True, key=lambda x: x[1])

    return results[:20]


@app.route("/content", methods=['GET', 'POST'])
def content():
    if request.method == 'POST':
        data = []

        try:
            points = request.get_json()

            for each in points:
                if points[each] == max(points.values()):
                    best = each

            with open(base + 'content.p', 'rb+') as f:
                feats = pickle.load(f)

            return_list = get_neighbour(best, feats)
            data.extend(return_list)

        except:
            data.append({'movie_id': 'tm12345', 'expected_rating': 8.3})
        return jsonify(data)
    else:
        return jsonify({'movie_id': 'tmb6324', 'predicted_rating': 8.2})


@app.route("/flask", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        data = []
        try:
            points = request.get_json()
            mylist = my_ids(points)
            points = get_preferences(points)
            data = point_table(points, mylist, 20)

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
