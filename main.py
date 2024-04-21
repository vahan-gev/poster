import google.generativeai as genai
from dotenv import load_dotenv
import os
import tweepy
import schedule
import time
import pyfiglet

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-latest')
name = "POSTER"
api_key = os.getenv('TWITTER_API_KEY')
api_key_secret = os.getenv('TWITTER_API_KEY_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with X (Twitter)
client = tweepy.Client(consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# Make final post


def make_post():
    try:
        if create_post("This is a post created with X API."):
            print("[make_post] > Post Created Successfully.")

    except Exception as error:
        print('[make_post] Something went wrong: {error}'.format(error=error))


# Function to create a post in Twitter
def create_post(text):
    try:
        client.create_tweet(text=text)
        return True
    except Exception as error:
        print('[create_post] Something went wrong: {error}, The text is {text}'.format(
            error=error, text=text))
        return False


banner = pyfiglet.figlet_format(name)
print(banner)
print("[{name}] IS RUNNING...".format(name=name))
schedule.every(1).minutes.do(make_post)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    pass
