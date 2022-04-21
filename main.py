from dotenv import load_dotenv
import os
import praw #Make sure you have Praw already, if not get it from here https://pypi.org/project/praw/ .
            #Also make sure to put the Text in the Quotes.

subreddit = "bottest"
keywords = ["what episode", "phrase bot"]

def bot_login():
    print ("Logging in...")
    r = praw.Reddit(username = os.environ.get("REDDIT_USERNAME"), #Insert Reddit Username here, must be an actual account.
    password = os.environ.get("REDDIT_PASSWORD"), #Insert Reddit Account's Password.
    client_id = os.environ.get("REDDIT_CLIENT_ID"), #Put the line below the personal use script text here.
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET"), #Put the secret here.
    user_agent = os.environ.get("REDDIT_USER_AGENT")) #Put whatever here.
    print ("Logged in!")

    return r

def run_bot(r):
    print ("Listening to subreddit " + subreddit)
    for comment in r.subreddit(subreddit).stream.comments(skip_existing=True):
        if determine_need(comment) == True:
            print ("should reply now")
            comment.reply("this is working -robot")
        else:
            print ("need determined false for " + comment.body)

def determine_need(c):
    if any(word in c.body for word in keywords):
        return True
    else:
        return False

load_dotenv()

r = bot_login()
run_bot(r)