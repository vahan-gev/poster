import google.generativeai as genai
from dotenv import load_dotenv
import os
import tweepy
import schedule
import time
import pyfiglet

load_dotenv()
name = "JOKER"
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.0-pro-latest')
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
    print("[make_post] > GENERATING TWEET")
    suggestion = model.generate_content(
        "Suggest me a popular video game, give only the name")
    answer = model.generate_content(
        "Write a small joke about {suggestion}. Be really creative. Do not use cliche jokes. Add hashtags for a twitter post.".format(suggestion=suggestion.text.replace("\\", "")))
    try:
        if create_post(answer.text):
            print("[make_post] > POST CREATED SUCCESSFULLY.")

    except Exception as error:
        print('[make_post] > SOMETHING WENT WRONG: {error}'.format(
            error=error))


# Function to create a post in Twitter
def create_post(text):
    try:
        client.create_tweet(text=text)
        return True
    except Exception as error:
        print('[create_post] > SOMETHING WENT WRONG: {error}, THE TEXT IS: {text}'.format(
            error=error, text=text))
        return False


banner = pyfiglet.figlet_format(name)
print(banner)
print("[{name}] IS RUNNING...".format(name=name))
schedule.every(60).minutes.do(make_post)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    pass
