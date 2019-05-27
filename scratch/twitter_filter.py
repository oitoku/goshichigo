import os
from twitter import *
from keys import *
import gsheets

CHARACTER_THRESHOLD = 120
SAMPLE_SIZE = 8

PORN_SPAM_THRESHOLD = 2
PORN_SPAM_WORDS = ["fucking", "anal", "videos", "porno", "teen", "lesbian", "gay", "nipple", "mpgs",
					"hardcore", "asses", "nude", "fucked"]



def check_porn_spam(t):
	"""
	Check if a tweet has more than PORN_SPAM_THRESHOLD occurrences of words in the porn spam word bank,
	to filter out tweets that are just a bunch of porn search terms, followed by a country. (???)
	"""
	word_match = sum([w in t["text"] for w in PORN_SPAM_WORDS])
	if word_match >= PORN_SPAM_THRESHOLD:
		print("Filtered tweet with", word_match, "matches as probable porn spam:", t["text"])
		return True
	return False


def twitter_connect(stream=False):
	"""
	From the Python Twitter Tools repo documentation
	Connect to Twitter or to the Twitter stream.
	"""
	MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
	if not os.path.exists(MY_TWITTER_CREDS):
	    oauth_dance("My App Name", CONSUMER_KEY, CONSUMER_SECRET,
	                MY_TWITTER_CREDS)

	oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

	if stream:
		connection = TwitterStream(auth=OAuth(
	    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
	else:
		connection = Twitter(auth=OAuth(
		    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

	return connection


def get_tweet_samples(connection, sample_size=SAMPLE_SIZE, remove_links=True):
	"""
	Get SAMPLE_SIZE tweets from the tweet stream that fulfill a number of filtering criteria.
	"""

	old_ids = gsheets.get_all_old_tweet_ids()


	sample = []
	iterator = connection.statuses.sample()

	for tweet in iterator:
		if tweet["id"] in old_ids:
			print("Already done this tweet, skipping.")
			continue
		if tweet.get('lang', None) != "en":
			continue
		if tweet["truncated"] is True:
			continue
		if len(tweet["text"]) < CHARACTER_THRESHOLD:
			continue
		if tweet.get("is_quote_status", None) is True:
			continue
		if tweet.get("in_reply_to_status_id_str", None) is not None:
			continue
		if tweet.get("display_text_range", None) is not None and \
		len(tweet["text"][tweet["display_text_range"][0]:tweet["display_text_range"][1]]) < CHARACTER_THRESHOLD:
			continue
		if tweet["text"][0:4] == "RT @":
			continue
		if tweet.get("possibly_sensitive", None) is not None and tweet.get("possibly_sensitive", None) is True:
			continue
		if check_porn_spam(tweet) is True:
			continue
		if remove_links and tweet["text"].find("https://t.co/") != -1:
			continue

		sample.append(tweet)
		if len(sample) > SAMPLE_SIZE:
			break

		# Get non-truncated English tweets which meet minimum length requirements and aren't quotes
		# if tweet.get('lang', None) == "en" and tweet["truncated"] is False and \
		# len(tweet["text"]) >= CHARACTER_THRESHOLD and\
		# tweet.get("is_quote_status", None) is False:

			# Get tweets which are not replies and which are still minimum length after cutting out bad ranges
			# if tweet.get("in_reply_to_status_id_str", None) is None:
			# 	if tweet.get("display_text_range", None) is None or \
			# 	len(tweet["text"][tweet["display_text_range"][0]:tweet["display_text_range"][1]]) >= CHARACTER_THRESHOLD:

			# 		# Remove retweets and tweets with "possibly sensitive" content
			# 		if tweet["text"][0:4] != "RT @" and \
			# 		(tweet.get("possibly_sensitive", None) is None or \
			# 		tweet.get("possibly_sensitive", None) == False):


			# 			# Remove porn spam tweets and tweets with links
			# 			if check_porn_spam(tweet) is False:

			# 				if not remove_links or tweet["text"].find("https://t.co/") == -1:

			# 					print("Grabbed valid tweet.")
						
			# 					sample.append(tweet)
			# 					if len(sample) > SAMPLE_SIZE:
			# 						break
			# 				else:
			# 					print("Skipping tweet with link.")

	return sample


if __name__ == "__main__":

	twitter_stream = twitter_connect(stream=True)
	sampled_stream = get_tweet_samples(twitter_stream)
	for t in sampled_stream:
		print(t['text'])

