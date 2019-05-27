from twitter_filter import *
from haiku_maker import *
import numpy as np


stream_conn = twitter_connect(stream=True)

samples = get_tweet_samples(stream_conn)

haikus = []

for t in samples:
	h = text2haiku(t["text"])
	if h:
		haikus.append((t["id"], t["user"]["screen_name"], h))

print(haikus)

selected = haikus[np.random.randint(len(haikus))]

tweet_text = selected[2] + "\n-@" + selected[1]


twitter_conn = twitter_connect()

twitter_conn.statuses.update(status=tweet_text, in_reply_to_status_id=selected[0])


