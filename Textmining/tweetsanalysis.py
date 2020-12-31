
#1) Extract tweets for any user (try choosing a user who has more tweets)
#2) Perform sentimental analysis on the tweets extracted from the above

import pandas as pd
import tweepy 
#pip install tweepy
#Twitter API credentials

#####################Extraction of Tweets by twitter API and storing in system as structure format##############
consumer_key = "Please provide key"
consumer_secret = "ms8SiOpnSZMmaddPs58jd......secret"
access_key = "1336636014442422................accesskey"
access_secret = "IcYuv....................secret"

alltweets = []	

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    new_tweets = api.user_timeline(screen_name =screen_name ,count=200)
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1
    while len(new_tweets)>0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))                # tweet.get('user', {}).get('location', {})
 
    outtweets = [[tweet.created_at,tweet.entities["hashtags"],tweet.entities["user_mentions"],tweet.favorite_count,
                  tweet.geo,tweet.id_str,tweet.lang,tweet.place,tweet.retweet_count,tweet.retweeted,tweet.source,tweet.text,
                  tweet._json["user"]["location"],tweet._json["user"]["name"],tweet._json["user"]["time_zone"],
                  tweet._json["user"]["utc_offset"]] for tweet in alltweets]
    
    import pandas as pd
    tweets_df = pd.DataFrame(columns = ["time","hashtags","user_mentions","favorite_count",
                                    "geo","id_str","lang","place","retweet_count","retweeted","source",
                                    "text","location","name","time_zone","utc_offset"])
    tweets_df["time"]  = pd.Series([str(i[0]) for i in outtweets])
    tweets_df["hashtags"] = pd.Series([str(i[1]) for i in outtweets])
    tweets_df["user_mentions"] = pd.Series([str(i[2]) for i in outtweets])
    tweets_df["favorite_count"] = pd.Series([str(i[3]) for i in outtweets])
    tweets_df["geo"] = pd.Series([str(i[4]) for i in outtweets])
    tweets_df["id_str"] = pd.Series([str(i[5]) for i in outtweets])
    tweets_df["lang"] = pd.Series([str(i[6]) for i in outtweets])
    tweets_df["place"] = pd.Series([str(i[7]) for i in outtweets])
    tweets_df["retweet_count"] = pd.Series([str(i[8]) for i in outtweets])
    tweets_df["retweeted"] = pd.Series([str(i[9]) for i in outtweets])
    tweets_df["source"] = pd.Series([str(i[10]) for i in outtweets])
    tweets_df["text"] = pd.Series([str(i[11]) for i in outtweets])
    tweets_df["location"] = pd.Series([str(i[12]) for i in outtweets])
    tweets_df["name"] = pd.Series([str(i[13]) for i in outtweets])
    tweets_df["time_zone"] = pd.Series([str(i[14]) for i in outtweets])
    tweets_df["utc_offset"] = pd.Series([str(i[15]) for i in outtweets])
    tweets_df.to_csv(r"file path"+screen_name+"_tweets.csv")
    return tweets_df
########################Senttimental Analysis#####################
    
vkohli= get_all_tweets("imVkohli")
vkohli.columns
vkohli_text=list(vkohli["text"])
 # Joinining all the reviews into single paragraph 
tweets_rev_string = " ".join(vkohli_text)

import re
# Removing unwanted symbols incase if exists
tweets_rev_string = re.sub("[^A-Za-z" "]+"," ",tweets_rev_string).lower()
tweets_rev_string = re.sub("[0-9" "]+"," ",tweets_rev_string)

tweets_reviews_words = tweets_rev_string.split(" ")

with open(r"filepath\stop.txt","r") as sw:
    stopwords = sw.read()
    
stopwords = stopwords.split("\n")

tweets_reviews_words = [w for w in tweets_reviews_words if not w in stopwords]

# Joinining all the reviews into single paragraph 
tweets_rev_string = " ".join(tweets_reviews_words)


import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud_ip = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweets_rev_string)

plt.imshow(wordcloud_ip)

# positive words # Choose the path for +ve words stored in system
with open(r"filepath\positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")
  

# negative words  Choose path for -ve words stored in system
with open(r"filepath\negative-words.txt","r") as neg:
  negwords = neg.read().split("\n")


# negative word cloud
# Choosing the only words which are present in negwords
tweets_neg_in_neg = " ".join ([w for w in tweets_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweets_neg_in_neg)

plt.imshow(wordcloud_neg_in_neg)

# Positive word cloud
# Choosing the only words which are present in positive words
tweets_pos_in_pos = " ".join ([w for w in tweets_reviews_words if w in poswords])
wordcloud_pos_in_pos = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(tweets_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)
 

# Unique words 
vkohli_unique_words = list(set(" ".join(vkohli_text).split(" ")))
