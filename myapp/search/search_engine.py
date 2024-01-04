import random
from myapp.search.embeddings import obtain_similarity
from myapp.core.utils import get_tweet

class SearchEngine:
    """educational search engine"""

    def search(self, search_query, search_id, corpus, tweets):
        print("Search query:", search_query)
        res = []
        k = 50
        results = obtain_similarity(search_query, corpus, k) #search_query)  # replace with call to search algorithm
        for tweet_id in results['Tweet_id'][:k]:
            selected_tweet = get_tweet(tweet_id, tweets)
            print(selected_tweet)
            print(selected_tweet['id'])
            if selected_tweet:
                res.append(selected_tweet)

        return res
