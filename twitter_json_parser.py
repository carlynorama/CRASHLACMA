import json
from pprint import pprint
import re
import urllib
import time

# TODO: handle test cases
# testcases:
# hollywood & vine, hollywood and vine
# order of operations: hashtag, img, address, other text.
# hashtag allcaps or lowercase
# uploaded image, link to hosted image
# multiple urls? currently hard-coded to only accept the first url seen. probably best this way.

class TwitterJsonParser():
	
	# parser useful fields from file of json tweet objects
	def get_data_from_tweets(self, input_data):
		
		tweet_data = []
		processed_tweets = []
		with open(input_data) as f:
			for line in f:
				if line.strip():
					tweet_data = json.loads(line)
					
					tweet = tweet_data["text"]
						
					# scrub out any @mentions or #hashtags to leave behind address / text
					tweet_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",tweet).split())
					
					# img uploaded via twitter
					if tweet_data["entities"].get('media'): 
						print "DEBUG: img uploaded"
						img_url = tweet_data["entities"]["media"][0]["media_url"]	
					# if img passed as url
					else:  
						print "DEBUG: img as url"
						img_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)[0]
	
					print("tweet: %s") % tweet
					print("tweet_text: %s, img_url: %s") % (tweet_text, img_url)
					
					self.save_img_from_tweet(tweet_text, img_url)
					
					processed_tweets.extend([tweet, tweet_text, img_url])
					
		return processed_tweets
						
	# this is run on one tweet at a time
	def save_img_from_tweet(self, tweet_text, img_url):
		DIR_FINISHED_IMGS='data_finished_images'
			
		# TODO: check first to make sure filename does not already exist

		# clean address to be usable as a filename
		title = re.sub('[^a-zA-Z0-9\n]', '_', tweet_text) + '.jpg'

		# save url to disk with address as filename
		try:
			file = urllib.urlretrieve(img_url, DIR_FINISHED_IMGS + '/' + title)
			print("Saved: %s" % title)
		except IOError, e:
			print 'could not retrieve %s' % url

		time.sleep(1.5)

		print("--------------------------------------------------------") # DEBUG

		return 
	