import sys
import os
import shutil
import papermill as pm
import scrapbook as sb
import pandas as pd
import numpy as np
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from recommenders.utils.timer import Timer
#from recommenders.models.ncf.ncf_singlenode import NCF
from ncf_singlenode import NCF
from recommenders.models.ncf.dataset import Dataset as NCFDataset
from recommenders.datasets import movielens
# from recommenders.datasets.python_splitters import python_chrono_split
from recommenders.evaluation.python_evaluation import (rmse, mae, rsquared, exp_var, map_at_k, ndcg_at_k, precision_at_k, recall_at_k, get_top_k_items)
from recommenders.utils.constants import SEED as DEFAULT_SEED

import math

print("System version: {}".format(sys.version))
print("Pandas version: {}".format(pd.__version__))
print("Temsorflow version: {}".format(tf.__version__))

DEFAULT_USER_COL = "userID"
DEFAULT_ITEM_COL = "itemID"
DEFAULT_TIMESTAMP_COL = "timestamp"

def _get_column_name(name, col_user, col_item):
    if name == "user":
        return col_user
    elif name == "item":
        return col_item
    else:
        raise ValueError("name should be either 'user' or 'item'.")

def min_rating_filter_pandas(
    data,
    min_rating=1,
    filter_by="user",
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
):
    """Filter rating DataFrame for each user with minimum rating.

    Filter rating data frame with minimum number of ratings for user/item is usually useful to
    generate a new data frame with warm user/item. The warmth is defined by min_rating argument. For
    example, a user is called warm if he has rated at least 4 items.

    Args:
        data (pandas.DataFrame): DataFrame of user-item tuples. Columns of user and item
            should be present in the DataFrame while other columns like rating,
            timestamp, etc. can be optional.
        min_rating (int): minimum number of ratings for user or item.
        filter_by (str): either "user" or "item", depending on which of the two is to
            filter with min_rating.
        col_user (str): column name of user ID.
        col_item (str): column name of item ID.

    Returns:
        pandas.DataFrame: DataFrame with at least columns of user and item that has been filtered by the given specifications.
    """
    split_by_column = _get_column_name(filter_by, col_user, col_item)

    if min_rating < 1:
        raise ValueError("min_rating should be integer and larger than or equal to 1.")

    return data.groupby(split_by_column).filter(lambda x: len(x) >= min_rating)

def process_split_ratio(ratio):
    """Generate split ratio lists.

    Args:
        ratio (float or list): a float number that indicates split ratio or a list of float
        numbers that indicate split ratios (if it is a multi-split).

    Returns:
        tuple:
        - bool: A boolean variable multi that indicates if the splitting is multi or single.
        - list: A list of normalized split ratios.
    """
    if isinstance(ratio, float):
        if ratio <= 0 or ratio >= 1:
            raise ValueError("Split ratio has to be between 0 and 1")

        multi = False
    elif isinstance(ratio, list):
        if any([x <= 0 for x in ratio]):
            raise ValueError(
                "All split ratios in the ratio list should be larger than 0."
            )

        # normalize split ratios if they are not summed to 1
        if math.fsum(ratio) != 1.0:
            ratio = [x / math.fsum(ratio) for x in ratio]

        multi = True
    else:
        raise TypeError("Split ratio should be either float or a list of floats.")

    return multi, ratio

def _do_stratification(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    is_random=True,
    seed=42,
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
):
    # A few preliminary checks.
    if not (filter_by == "user" or filter_by == "item"):
        raise ValueError("filter_by should be either 'user' or 'item'.")

    if min_rating < 1:
        raise ValueError("min_rating should be integer and larger than or equal to 1.")

    if col_user not in data.columns:
        raise ValueError("Schema of data not valid. Missing User Col")

    if col_item not in data.columns:
        raise ValueError("Schema of data not valid. Missing Item Col")

    if not is_random:
        if col_timestamp not in data.columns:
            raise ValueError("Schema of data not valid. Missing Timestamp Col")

    multi_split, ratio = process_split_ratio(ratio)

    split_by_column = col_user if filter_by == "user" else col_item

    ratio = ratio if multi_split else [ratio, 1 - ratio]

    if min_rating > 1:
        data = min_rating_filter_pandas(
            data,
            min_rating=min_rating,
            filter_by=filter_by,
            col_user=col_user,
            col_item=col_item,
        )

    if is_random:
        np.random.seed(seed)
        data["random"] = np.random.rand(data.shape[0])
        order_by = "random"
    else:
        order_by = col_timestamp

    data = data.sort_values([split_by_column, order_by])

    groups = data.groupby(split_by_column)

    data["count"] = groups[split_by_column].transform("count")
    data["rank"] = groups.cumcount() + 1

    if is_random:
        data = data.drop("random", axis=1)

    splits = []
    prev_threshold = None
    for threshold in np.cumsum(ratio):
        condition = data["rank"] <= round(threshold * data["count"])
        if prev_threshold is not None:
            condition &= data["rank"] > round(prev_threshold * data["count"])
        splits.append(data[condition].drop(["rank", "count"], axis=1))
        prev_threshold = threshold

    return splits

def python_chrono_split(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
):
    """Pandas chronological splitter.

    This function splits data in a chronological manner. That is, for each user / item, the
    split function takes proportions of ratings which is specified by the split ratio(s).
    The split is stratified.

    Args:
        data (pandas.DataFrame): Pandas DataFrame to be split.
        ratio (float or list): Ratio for splitting data. If it is a single float number
            it splits data into two halves and the ratio argument indicates the ratio of
            training data set; if it is a list of float numbers, the splitter splits
            data into several portions corresponding to the split ratios. If a list is
            provided and the ratios are not summed to 1, they will be normalized.
        seed (int): Seed.
        min_rating (int): minimum number of ratings for user or item.
        filter_by (str): either "user" or "item", depending on which of the two is to
            filter with min_rating.
        col_user (str): column name of user IDs.
        col_item (str): column name of item IDs.
        col_timestamp (str): column name of timestamps.

    Returns:
        list: Splits of the input data as pandas.DataFrame.
    """
    return _do_stratification(
        data,
        ratio=ratio,
        min_rating=min_rating,
        filter_by=filter_by,
        col_user=col_user,
        col_item=col_item,
        col_timestamp=col_timestamp,
        is_random=False,
    )

def do_stratification(
    data,
    ratio=0.75,
    min_rating=1,
    filter_by="user",
    is_random=True,
    seed=42,
    col_user=DEFAULT_USER_COL,
    col_item=DEFAULT_ITEM_COL,
    col_timestamp=DEFAULT_TIMESTAMP_COL,
):
    multi_split, ratio = process_split_ratio(ratio)

    split_by_column = col_user if filter_by == "user" else col_item

    ratio = ratio if multi_split else [ratio, 1 - ratio]

    if min_rating > 1:
        data = min_rating_filter_pandas(
            data,
            min_rating=min_rating,
            filter_by=filter_by,
            col_user=col_user,
            col_item=col_item,
        )

    if is_random:
        np.random.seed(seed)
        data["random"] = np.random.rand(data.shape[0])
        order_by = "random"
    else:
        order_by = col_timestamp

    data = data.sort_values([split_by_column, order_by])

    groups = data.groupby(split_by_column)

    data["count"] = groups[split_by_column].transform("count")
    data["rank"] = groups.cumcount() + 1

    if is_random:
        data = data.drop("random", axis=1)

    splits = []
    prev_threshold = None
    for threshold in np.cumsum(ratio):
        condition = data["rank"] <= round(threshold * data["count"])
        if prev_threshold is not None:
            condition &= data["rank"] > round(prev_threshold * data["count"])
        splits.append(data[condition].drop(["rank", "count"], axis=1))
        prev_threshold = threshold

    return splits

TOP_K = 10
MOVIELENS_DATA_SIZE = '100k'

EPOCHS = 100
BATCH_SIZE = 512

SEED = DEFAULT_SEED

#df = movielens.load_pandas_df(size=MOVIELENS_DATA_SIZE, header=["userID", "itemID", "rating", "timestamp"])
df = pd.read_csv('~/Documents/graduation_project/1017data.csv', sep=',', names=['user_id', 'location_id', 'score'], usecols=[0, 1, 3])
df.head()

#train, test = python_chrono_split(df, 0.75)
train, test = do_stratification(data=df, ratio=0.75, col_user="user_id", col_item="location_id")

test = test[test["user_id"].isin(train["user_id"].unique())]
test = test[test["location_id"].isin(train["location_id"].unique())]

leave_one_out_test = test.groupby("user_id").last().reset_index()

train_file = "./train.csv"
test_file = "./test.csv"
leave_one_out_test_file = "./leave_one_out_test.csv"
train.to_csv(train_file, index=False)
test.to_csv(test_file, index=False)
leave_one_out_test.to_csv(leave_one_out_test_file, index=False)

data = NCFDataset(
    train_file=train_file,
    test_file=leave_one_out_test_file,
    seed=SEED,
    overwrite_test_file_full=True,
    col_user="user_id",
    col_item="location_id",
    col_rating="score"
)

model = NCF(
        n_users=data.n_users, 
        n_items=data.n_items,
        model_type="NeuMF",
        n_factors=3,
        layer_sizes=[64,32,16,8,4],
        n_epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        learning_rate=0.001,
        verbose=10,
        seed=SEED
)

model.save("./MLPmodel")

with Timer() as train_time:
    model.fit(data)

print("Took {} seconds for training.".format(train_time.interval))

predictions = [[row.user_id, row.location_id, model.predict(row.user_id, row.location_id)]
                for (_, row) in test.iterrows()]
predictions = pd.DataFrame(predictions, columns=['user_id', 'location_id', 'prediction'])
predictions.head()
predictions.to_csv("./prediction.csv")

users, items, preds = [], [], []
item = list(train.location_id.unique())
for user in train.user_id.unique():
    user = [user] * len(item)
    users.extend(user)
    items.extend(item)
    preds.extend(list(model.predict(user, item, is_list=True)))

all_predictions = pd.DataFrame(data={"user_id": users, "location_id": items, "prediction": preds})

merged = pd.merge(train, all_predictions, on=["user_id", "location_id"], how="outer")
all_predictions = merged[merged.score.isnull()].drop('score', axis=1)
all_predictions.to_csv("./all_prediction.csv")

'''
with Timer() as test_time:
    users, items, preds = [], [], []
    item = list(train.location_id.unique())
    for user in train.user_id.unique():
        user = [user] * len(item)
        users.extend(user)
        items.extend(item)
        preds.extend(list(model.predict(user, item, is_list=True)))

    all_predictions = pd.DataFrame(data={"user_id": users, "location_id": items, "prediction": preds})

    merged = pd.merge(train, all_predictions, on=["user_id", "location_id"], how="outer")
    all_predictions = merged[merged.score.isnull()].drop('score', axis=1)

print("Took {} seconds for prediction.".format(test_time.interval))

eval_map = map_at_k(test, all_predictions, col_user="user_id", col_item="location_id", col_rating="score", col_prediction='prediction', k = TOP_K)
eval_ndcg = ndcg_at_k(test, all_predictions, col_user="user_id", col_item="location_id", col_rating="score", col_prediction='prediction', k = TOP_K)
eval_precision = precision_at_k(test, all_predictions, col_user="user_id", col_item="location_id", col_rating="score", col_prediction='prediction', k = TOP_K)
eval_recall = recall_at_k(test, all_predictions, col_user="user_id", col_item="location_id", col_rating="score", col_prediction='prediction', k = TOP_K)

print("MAP: \t\t%f" % eval_map,
      "NDCG: \t\t%f" % eval_ndcg,
      "Precision@K: \t%f" % eval_precision,
      "Recall@K: \t%f" % eval_recall, sep='\n')

# leave one out testing
k = TOP_K
ndcgs = []
hit_ratio = []

for b in data.test_loader():
    user_input, item_input, labels = b
    output = model.predict(user_input, item_input, is_list=True)

    output = np.squeeze(output)
    rank = sum(output >= output[0])
    if rank <= k:
        ndcgs.append(1 / np.log(rank + 1))
        hit_ratio.append(1)
    else:
        ndcgs.append(0)
        hit_ratio.append(0)
    
eval_ndcg = np.mean(ndcgs)
eval_hr = np.mean(hit_ratio)

print("HR:\t%f" % eval_hr)
print("NDCG:\t%f" % eval_ndcg)

all_predictions.to_csv("./predictions.txt", sep='\t', encoding="utf-8", header=True, index=False)
'''
