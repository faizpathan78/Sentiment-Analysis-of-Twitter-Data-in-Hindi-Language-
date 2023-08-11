import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(from:elonmusk)"
tweets_list = []
limit = 10


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets_list) == limit:
        break
    else:
        tweets_list.append([tweet.content])

tweets_str = ','.join(str(item) for innerlist in tweets_list for item in innerlist)

print(tweets_str)