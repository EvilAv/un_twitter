import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans
from surprise.model_selection import cross_validate

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

print(df.head(20))

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


# trainingSet = data.build_full_trainset()
# algo.fit(trainingSet)


for i in range(1, 7):
    print('tweet ' + str(i) + ' with probability: ' + str(algo.predict('E', i).est))
