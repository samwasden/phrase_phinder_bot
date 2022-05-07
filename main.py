from dotenv import load_dotenv
import os
import requests
import datetime
import praw 
from praw.models import Comment

shownames = {
    "bottest": "The Office",
    "theofficegifs": "The Office"
}

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
    for message in r.inbox.stream():
        try:
            if message in r.inbox.unread(limit=None):
                if isinstance(message, Comment):
                    subreddit = message.subreddit.display_name
                    res = request_episodes(message.body, message.subreddit.display_name)
                    search = message.body.split()
                    search.pop(0)
                    phrase = ' '.join(search)
                    occurances = res['Occurences']
                    total_occurances = len(occurances)
                    occurance_text = "I found **" + str(total_occurances) + '** occurances of "*' + phrase + '*" in **' + shownames[subreddit] + "**. ";
                    true_link = "(http://phrasephinder.com/" + under_scored(subreddit) + "/" + plus_scored(phrase) + ")"
                    link_text = "find more of your favorite phrases at [http://phrasephinder.com]" + true_link + "."
                    if total_occurances > 1:
                        link_text = "See the other **" + str(total_occurances - 1) + "** results and " + link_text
                    if total_occurances > 0:
                        result = occurances[0]
                        episode_text = "> season " + str(result["Season"]) + " episode " + str(result["Episode"]);
                        name_text = "> **" + result["EpisodeName"] + "** ";
                        time_text = "> Found between " + str(datetime.timedelta(seconds = result["Start"])) + " and " + str(datetime.timedelta(seconds = result["End"])) + ". ";
                        reply_text = occurance_text + "\n\n" + episode_text + "  \n" + name_text + "\n" + time_text + "\n\n" + link_text;
                        message.reply(reply_text)
                        print(reply_text)
                    else:
                        reply_text = "I was unnable to find any matching phrases in ***" + shownames[subreddit] + "***." + "\n" + link_text
                        message.reply(reply_text)
                        print(reply_text)
                    message.mark_read()
                else:
                    message.mark_read()
                    print ("was not a comment mention: " + message.body)
            else:
                print ("need determined false for: " + message.body)
                message.mark_read()
        except praw.exceptions.APIException:
            print("probably a rate limit...")


def under_scored(s):
    show = shownames[s].split()
    if len(show) > 1:
        scored_show = '_'.join(show)
        return scored_show
    else:
        return show

def plus_scored(p):
    arr = p.split()
    if len(arr) > 1:
        plus_phrase = '+'.join(arr)
        return plus_phrase
    else:
        return p

def request_episodes(p, s):
    phrase = p.split()
    phrase.pop(0)
    search = '+'.join(phrase)
    show = under_scored(s)
    response = requests.get(os.environ.get("API_URL") + show + "/?phrase=" + search)
    return response.json()

load_dotenv()

r = bot_login()
run_bot(r)