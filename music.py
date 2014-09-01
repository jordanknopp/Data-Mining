import twitter
import json
from collections import Counter
from prettytable import PrettyTable
from keychain import keychain


keys = keychain()
auth = twitter.oauth.OAuth(keys[2], keys[3], keys[0], keys[1])
#auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


q = 'free music'
count = 200


search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']

status_texts = [ status['text'] 
				for status in statuses]

screen_names = [ user_mention['screen_name']
				for status in statuses
					for user_mention in status['entities']['user_mentions'] ]

hashtags = [ hashtag['text']
				for status in statuses
					for hashtag in status['entities']['hashtags'] ]

urls = [ url['url']
			for status in statuses
				for url in status['entities']['urls'] ]

e_urls = [ url['expanded_url']
			for status in statuses
				for url in status['entities']['urls'] ]

for label, data in (('urls', urls),
					('e_urls', e_urls)):
	pt = PrettyTable(field_names=[label, 'blah'])	
	c = Counter(data)
	[ pt.add_row(kv) for kv in c.most_common()[:50] ]
	print pt


f = open('links.txt', 'w')
for ele in urls:
	f.write(ele)
	f.write("\n")
f.close()


f = open('expanded_links.txt', 'w')
for ele in e_urls:
	f.write(ele)
	f.write("\n")
f.close()