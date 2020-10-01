import numpy as np
import pickle as pkl
import bisect


cwd = '/home/canbulguoglu/app'


class FunkSVD():
    def __init__(self, data):
        # Accepts pandas dataframe where column names are user_id, item_id and Rating
        with open(cwd+'/flask.p', 'rb') as f:
            myDicts = pkl.load(f)
        self.user_features = myDicts[0]
        self.item_features = myDicts[1]
        self.user_data = {}

        for each in data:
            if str(each['id']) in self.item_features:

                self.user_data[str(each['id'])] = float(each['rating'])/2

    def get_recommendation(self, howMany=20):

        user_predictions = self.__user_prediction_for_same_movies(
            self.user_data)
        # Find most most similar user_ids
        user_ids = FunkSVD.get_most_similar_users(
            self.user_data, user_predictions, 1)

        result_list = []
        # get user features for users who are most similar to given new user
        for user in user_ids:
            for item, item_feature in self.item_features.items():
                # predict ratings for most similar users
                prediction = np.dot(
                    self.user_features[user], item_feature)
                bisect.insort(result_list, [prediction, item])

        return_list = []
        for pair in result_list:
            if len(return_list) >= 60:
                break
            if pair[1] in return_list:
                continue

            return_list.append(pair[1])
        np.random.shuffle(return_list)

        return return_list[:howMany]

    def __user_prediction_for_same_movies(self, user_ratings):
        result = {}
        for key in user_ratings:
            if key not in self.item_features:
                continue

            for user in self.user_features:
                result.setdefault(user, []).append(
                    np.dot(self.user_features[user], self.item_features[key]))

        return result

    @staticmethod
    def mean_squared_difference(a, b):
        summation = 0
        n = len(a)
        for i in range(0, n):
            difference = a[i] - b[i]
            squared_difference = difference**2
            summation = summation + squared_difference
        MSE = summation/n

        return 1/MSE

    @staticmethod
    def get_most_similar_users(user_ratings, user_predictions, howMany):
        similarities = []

        for user, ratings in user_predictions.items():

            similarity = FunkSVD.mean_squared_difference(
                list(user_ratings.values()), ratings)

            similarities.append([user, similarity])

        similarities.sort(reverse=True, key=lambda x: x[1])

        return [each[0] for each in similarities[:howMany]]
