#Find some news source
#Scrape the news page with Python
#Parse the html and extract the content with BeautifulSoup
#Convert it to readable format then send an E-mail to myself


import praw
import pprint
from twilio.rest import Client as twilio_client
import random


#twilio account
account_id = 'AC33a7892b43b1ff505f315d993bf05efe'
auth_token = '381320886ec3e065ea40b59f63300ef8'
tw_client = twilio_client(account_id, auth_token)

#reddit account
reddit = praw.Reddit(client_id='vVItrDIoaEtIYg',
                     client_secret='y1A91trMdu9JHzwGqGOijyQJ3S4',
                     grant_type='client_credentials',
                     user_agent='mytestscript/1.0')


submissions = reddit.subreddit('MBA').hot(limit=5)

list_of_links = [item.url for item in submissions]


_message = "Hello Fiona, here are some recent MBA news from Reddit: \n" + '\n'.join(list_of_links)
print(_message)

message = tw_client.messages.create(
        body= _message,
        from_='+18317099945',
        to='+14083483260')

