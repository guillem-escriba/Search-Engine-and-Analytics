import json
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import re
import nltk
nltk.download('stopwords')

def build_terms(line):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.

    Argument:
    line -- string (text) to be preprocessed

    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    line = url_pattern.sub(r'', line)

    emoji_pattern = re.compile(pattern="["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F700-\U0001F77F"  # alchemical symbols
                                u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                                u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                                u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                                u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                                u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                                u"\U00002702-\U000027B0"  # Dingbats
                                "]+", flags=re.UNICODE)
    line = emoji_pattern.sub(r'', line)

    line=  line.lower()       ## Transform in lowercase
    line=  line.split()       ## Tokenize the text to get a list of terms
    #line = [term.strip(string.punctuation) if term[0] != '#' else term[1:] for term in line] #Identify hashtags and delete the symbol
    line = [term.strip(string.punctuation) for term in line] #Remove puntuaction signs, # included
    line = [word for word in line if word not in stop_words]  ## Eliminate the stopwords (HINT: use List Comprehension)
    line = [stemmer.stem(word) for word in line]  ## perform stemming (HINT: use List Comprehension)
    return line

def read_tweets(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()

    tweets = []
    for line in lines:
        try:
            tweet = json.loads(line.strip())
            tweets.append(tweet)
        except json.JSONDecodeError:
            # Handle the error if line is not a valid JSON
            pass

    print("There are ", len(tweets), " valid tweets")
    return tweets

def get_tweet_info(tweet):
    tweet_id = tweet['id']
    date = tweet['created_at']
    text = tweet['full_text']
    hashtags = [tag['text'] for tag in tweet['entities']['hashtags']]
    likes = tweet['favorite_count']
    retweets = tweet['retweet_count']
    url = f"https://twitter.com/user_name/status/{tweet_id}"
    tweet_info = f"Date: {date}\nText: {text}\nHashtags: {hashtags}\nLikes: {likes}\nRetweets: {retweets}\nURL: {url}\n{'-'*50}"

    return ({
        'id':tweet_id,
        'Tweet': text,
        'Date': date,
        'Hashtags': hashtags,
        'Likes': likes,
        'Retweets': retweets,
        'Url': url
    })

def get_tweet(tweet_id, tweets):
    for tweet in tweets:
        #tweet = json.loads(tweet)
        if tweet['id'] == (tweet_id):
            return get_tweet_info(tweet)
    return None