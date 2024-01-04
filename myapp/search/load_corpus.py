import pandas as pd
import torch
from myapp.core.utils import read_tweets
from myapp.search.embeddings import parse
from pandas import json_normalize

_corpus = {}

def load_corpus(json_path, df_path):
    print('Reading embeddings...')
    combined_df = pd.read_csv(df_path)
    combined_df["Embedding"] = combined_df["Embedding"].apply(lambda vector_string: parse(vector_string))
    print('Embeddings loaded!')
    tweets = read_tweets(json_path)
    return tweets, combined_df


