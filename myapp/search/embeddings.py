import json
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from myapp.core.utils import read_tweets
import re

# Check if a CUDA-enabled GPU is available, and use it if possible
device = torch.device("cuda" if torch.cuda.is_available() else "mps")

# Load the Sentence Transformers model onto the GPU
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
model.to(device)

def create_tweet_dataframe(tweets):
    tweet_info_list = []

    for tweet in tweets:
        tweet = json.loads(tweet)
        tweet_id = tweet['id_str']
        date = tweet['created_at']
        text = tweet['full_text']
        hashtags = [tag['text'] for tag in tweet['entities']['hashtags']]
        likes = tweet['favorite_count']
        retweets = tweet['retweet_count']
        url = f"https://twitter.com/user_name/status/{tweet_id}"

        tweet_info_list.append({
            'Tweet_id': tweet_id,
            'Date': date,
            'Text': text,
            'Hashtags': hashtags,
            'Likes': likes,
            'Retweets': retweets,
            'Url': url
        })

    tweet_df = pd.DataFrame(tweet_info_list)
    return tweet_df


def df_embeddings(paragraphs):
    """
    input: list of paragraphs
    output: dataframe mapping each paragraph to its embedding
    """
    # Encode embeddings on the GPU
    embeddings = model.encode(paragraphs, convert_to_tensor=True).cpu().numpy()
    df = pd.DataFrame({"Embedding": embeddings[i]} for i in range(len(embeddings)))
    return df


def obtain_similarity(query, df, k):
    """
    arguments:
        - query: word or sentence to compare
        - df: dataframe mapping paragraphs to embeddings
        - k: number of selected similar paragraphs
    output: list of paragraphs relevant for the query and the position in the dataframe at which they are
    """

    query_embedding = model.encode(query, convert_to_tensor=True).cpu().numpy()
    
    max_likes = np.max(df["Likes"])
    max_retweets = np.max(df["Retweets"])

    df["Similarity"] = df["Embedding"].apply(lambda emb: cosine_similarity([emb], [query_embedding])[0, 0])
    df["Similarity"] = df["Similarity"] + 0.15*(df["Likes"]/(2*max_likes)) + 0.15*(df["Retweets"]/(2*max_retweets))

    df = df.sort_values("Similarity", ascending=False, ignore_index=True)
    top_k = df.drop(["Embedding"],axis=1)[:k]
    return top_k

def create_embeddings(docs_path):
  tweets = []
  lines = read_tweets(docs_path)
  for line in lines:
      tweet = json.loads(line)
      text = tweet["full_text"]
      tweets.append(text)

  df = df_embeddings(tweets)
  tweets_df = create_tweet_dataframe(lines)

  combined_df = pd.concat([tweets_df,df], axis=1)

  combined_df.to_csv('embeddings_df.csv', index=False)
  return combined_df

def parse(vector_string):
  vector_string = vector_string.replace('\n', '')
  float_values = [float(match) for match in re.findall(r'-?\d+.\d+e?-?\d*', vector_string)]
  vector_array = np.array(float_values)
  return vector_array