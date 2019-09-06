import tweepy

auth = tweepy.OAuthHandler('Z6RfmhAIYODAPrBOepk4oPZpD', 'ZkZC46kU9V7LRE4A88Y4J1OqWGtYNWysq4Wjds2OtaoAA13DuZ')
auth.set_access_token('1111543125162500097-UDXD6i78MzILZLhYtk9XbWCmgCvt1J', 'XEmdFRwxPiNz4O7d903zjEVNz5PaQpEKRv4ZpxxA09ISp')

api = tweepy.API(auth)
'''
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

'''
# Get the User object for twitter...
user = api.get_user('twitter')

print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)