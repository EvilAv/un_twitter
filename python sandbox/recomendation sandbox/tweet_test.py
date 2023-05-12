from collections import defaultdict

import pandas as pd
from surprise import Dataset, dump, Reader, KNNWithMeans
from surprise.model_selection import cross_validate
import os

# This is the same data that was plotted for similarity earlier
# with one new user "E" who has rated only movie 1
tweets = {
    1: 'politic_a',
    2: 'politic_b',
    3: 'politic_c',
    4: 'movie_a',
    5: 'movie_b',
    6: 'movie_c'
}
ratings_dict = {
    "item": [1, 2, 3, 1, 2, 3, 4, 4, 5, 6, 4, 5, 6, 1, 1, 2, 4, 5, 6, 5, 6, 1, 2, 3, 2, 3],
    "user": ['A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'A', 'A', 'A', 'B', 'B',
             'C', 'C', 'C', 'D', 'D'],
    "is_liked": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}


df = pd.DataFrame(ratings_dict)
reader = Reader(rating_scale=(0, 1))

# print(df.head(20))

# Loads Pandas dataframe
data = Dataset.load_from_df(df[["user", "item", "is_liked"]], reader)
# test = data.build_full_trainset()
# anti_test = test.build_anti_testset(fill=0)

# Loads the builtin Movielens-100k data


# To use item-based cosine similarity
sim_options = {
    "name": "pearson_baseline",
    "user_based": False,  # Compute  similarities between items
}
algo = KNNWithMeans(sim_options=sim_options)

# algo.fit(test)
# algo.test(anti_test)
# print(test)
# print(anti_test)

cross_validate(algo, data, verbose=False)
# cross_validate(algo, data, verbose=True)
file_name = os.path.join(os.getcwd(), 'dump')
print(file_name)
print(os.path.exists(file_name))
_, loaded_algo = dump.load(file_name)

dump.dump(file_name, algo=algo)

# trainingSet = data.build_full_trainset()
# algo.fit(trainingSet)


for i in range(1, 7):
    print('tweet ' + str(i) + ' with probability: ' + str(algo.predict('E', i).est))
for i in range(1, 7):
    print('tweet ' + str(i) + ' with probability: ' + str(loaded_algo.predict('E', i).est))


def get_top_n(user, unviewed_tweets, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    dataset = []
    for tweet in unviewed_tweets:
        dataset.append((user, tweet, 1))
    # top_n = defaultdict(list)
    # predictions = algo.test(dataset)
    # for uid, iid, true_r, est, _ in predictions:
    #     top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    # for uid, user_ratings in top_n.items():
    #     user_ratings.sort(key=lambda x: x[1], reverse=True)
    #     top_n[uid] = user_ratings[:n]
    #
    # return top_n
    predictions = loaded_algo.test(dataset)
    raw_list = []
    for uid, iid, true_r, est, _ in predictions:
        raw_list.append((iid, est))
    raw_list.sort(key=lambda a: a[1], reverse=True)

    res = []
    for i in raw_list:
        res.append(i[0])
    print(raw_list)
    return res


print(get_top_n('E', [1, 2, 3, 4, 5, 6]))
