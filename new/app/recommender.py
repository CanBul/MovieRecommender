import pandas as pd
import numpy as np
import json


def my_ids(pointtable):
    mylist = []
    for each in pointtable:
        if each['id'] not in mylist:
            mylist.append(each['id'])

    return mylist


def get_preferences(points):

    result = {'Actors': {}, 'Director': {}, 'Genres': {}}
    with open('/home/canbulguoglu/app/id_table.json', 'r') as f:
        movies = json.load(f)

    for each in points:
        movie_id = each['id']
        score = int(each['rating'])

        movie_director = movies[movie_id]['director']
        movie_actors = movies[movie_id]['cast']
        movie_genres = movies[movie_id]['genres']

        if movie_director in result['Director']:
            result['Director'][movie_director] = (
                result['Director'][movie_director] + score)/2
        else:
            result['Director'].update({movie_director: score})

        for actor in movie_actors:
            if actor in result['Actors']:
                result['Actors'][actor] = (result['Actors'][actor] + score)/2
            else:
                result['Actors'].update({actor: score})

        for genre in movie_genres:
            if genre in result['Genres']:
                result['Genres'][genre] = (result['Genres'][genre] + score)/2
            else:
                result['Genres'].update({genre: score})

    return result


def point_table(points, mylist, howMany=15):
    df = pd.read_json('/home/canbulguoglu/app/movies.json')
    df = df[~df.imdb_id.isin(mylist)]

    # actor points (biggest)
    actor_points = [np.nan for each in range(df.shape[0])]
    actors = points['Actors']
    cast = df['cast'].to_numpy()

    for actor in actors:
        for i, each in enumerate(cast):
            if actor in each:

                if actors[actor] >= actor_points[i] or np.isnan(actor_points[i]):

                    actor_points[i] = actors[actor]

    df['actor_points'] = np.array(actor_points)

    # director points

    directors = points['Director']
    director_points = [np.nan for each in range(df.shape[0])]

    for director in directors:
        for i, each in enumerate(df.director):

            if director == each:

                if directors[director] >= director_points[i] or np.isnan(director_points[i]):

                    director_points[i] = directors[director]

    df['director_points'] = np.array(director_points)

    # genre points (average)
    genres = points['Genres']
    genre_points = [np.nan for each in range(df.shape[0])]
    df_genres = df['genres'].to_numpy()

    for genre in genres:
        for i, each in enumerate(df_genres):
            if genre in each:
                if np.isnan(genre_points[i]):
                    genre_points[i] = genres[genre]
                else:
                    genre_points[i] = (genre_points[i]+genres[genre])/2

    df['genre_points'] = np.array(genre_points)

    df['points_average'] = df.apply(lambda row: np.nanmean(
        [row['actor_points'], row['director_points'], row['genre_points']]), axis=1)
    df['total_average'] = df.apply(lambda row: (
        row['vote_average']+row['points_average'])/2, axis=1)

    df = df.nlargest(80, 'total_average')
    df = df.sample(howMany)
    df = df[['imdb_id', 'title', 'total_average']]

    return list(df.values.tolist())
