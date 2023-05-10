import pandas as pd
from surprise import Dataset, dump, Reader, KNNWithMeans
from surprise.model_selection import cross_validate
import os
from pathlib import Path

file_name = os.path.join(Path(__file__).parent.parent, 'recommend_dump/dump')


def train_system(dataset_dict):

    df = pd.DataFrame(dataset_dict)
    reader = Reader(rating_scale=(0, 1))

    data = Dataset.load_from_df(df[["user", "item", "is_liked"]], reader)

    sim_options = {
        "name": "pearson_baseline",
        "user_based": False,  # Compute  similarities between items
    }
    algo = KNNWithMeans(sim_options=sim_options)

    cross_validate(algo, data, verbose=False)

    dump.dump(file_name, algo=algo)


def get_top_predictions(user, unviewed_tweets, n=10):
    if not os.path.exists(file_name):
        return []
    _, algo = dump.load(file_name)

    dataset = []
    for tweet in unviewed_tweets:
        dataset.append((user, tweet, 1))

    predictions = algo.test(dataset)
    raw_list = []
    for uid, iid, true_r, est, _ in predictions:
        raw_list.append((iid, est))
    raw_list.sort(key=lambda a: a[1], reverse=True)

    res = []
    for i in raw_list:
        res.append(i[0])
    print(raw_list)
    return res