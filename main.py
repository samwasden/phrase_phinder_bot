import sre_compile
from dotenv import load_dotenv
import os
import requests
import datetime
import praw 
from praw.models import Comment

showref = {
    # dave chappelle
    "dave chappelle": "Dave Chappelle",
    # austin powers the spy who shagged me
    "austin powers the spy who shagged me": "Austin Powers The Spy Who Shagged Me",
    #bad trip
    "bad trip": "Bad Trip",
    # bee movie
    "bee movie": "Bee Movie",
    # due date
    "due date": "Due Date",
    # hot rod
    "hot rod": "Hot Rod",
    # madagascar 2
    "madagascar 2": "Madagascar 2",
    # nacho libre
    "nacho libre": "Nacho Libre",
    # no strings attached
    "no strings attached": "No Strings Attached",
    # superbad
    "superbad": "Superbad",
    # talladega nights
    "talladega nights": "Talladega Nights",
    # the other guys
    "the other guys": "The Other Guys",
    # year one
    "year one": "Year One",
    # yes man
    "yes man": "Yes Man",
    # all american
    "all american": "All American",
    # arrested development
    "arrested development": "Arrested Development",
    # avatar the last air bender
    "avatar the last air bender": "Avatar the Last Air Bender",
    # better call saul 
    "better call saul": "Better Call Saul",
    # big mouth 
    "big mouth": "Big Mouth",
    # breaking bad 
    "breaking bad": "Breaking Bad",
    # brooklyn nine nine 
    "brooklyn nine nine": "Brooklyn Nine Nine",
    # chappelles show 
    "chappelles show": "Chappelles Show",
    # comedians in cars getting coffee 
    "comedians in cars getting coffee": "Comedians in Cars Getting Coffee",
    # community 
    "community": "Community",
    # how i met your mother 
    "how i met your mother": "How I Met Your Mother",
    # money heist 
    "money heist": "Money Heist",
    # narcos 
    "narcos": "Narcos",
    # new girl 
    "new girl": "New Girl",
    # outer banks 
    "outer banks": "Outer Banks",
    # ozark 
    "ozark": "Ozark",
    # queens gambit 
    "queens gambit": "Queens Gambit",
    # schitts creek 
    "schitts creek": "Schitts Creek",
    # shameless 
    "shameless": "Shameless",
    # stranger things 
    "stranger things": "Stranger Things",
    # the last dance 
    "the last dance": "The Last Dance",
    # the office 
    "office": "The Office",
    "the office": "The Office",
    "theofficegifs": "The Office",
    # the walking dead 
    "the walking dead": "The Walking Dead"
}


def bot_login():
    print ("Logging in...")
    r = praw.Reddit(username = os.environ.get("REDDIT_USERNAME"), #Insert Reddit Username here, must be an actual account.
    password = os.environ.get("REDDIT_PASSWORD"), #Insert Reddit Account's Password.
    client_id = os.environ.get("REDDIT_CLIENT_ID"), #Put the line below the personal use script text here.
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET"), #Put the secret here.
    user_agent = os.environ.get("REDDIT_USER_AGENT")) #Put whatever here.
    print ("Logged in!")
    print()

    return r


def run_bot(r):
    for message in r.inbox.stream():
        try:
            if message in r.inbox.unread(limit=None):
                if isinstance(message, Comment):
                    res = request_episodes(message.body, message.subreddit.display_name)
                    if res[0] == False:
                        reply = res[1] + "\n\n" + "find more of your favorite phrases at [" + os.environ.get("WEB_URL") + "](" + os.environ.get("BASE_URL") + ")."
                        message.reply(reply)
                        message.mark_read()
                        print(reply)
                        print()
                    else:
                        re = res[1]
                        sp = res[2]
                        sn = res[3]
                        o = re['Occurences']
                        reply = reply_text(o, sp, sn)

                        message.reply(reply)
                        message.mark_read()
                        print(reply)
                        print()
                else:
                    message.mark_read()
                    print("Not a comment mention: " + message.body)
                    print()
            else:
                message.mark_read()
                print("Not an unread message: " + message.body)
                print()

        except praw.exceptions.APIException:
            print("probably a rate limit...")
            print()


def reply_text(o, sp, sn):
    to = len(o)
    if to > 1:
        occs = "s"
        nf = "f"
    else:
        occs = ""
        nf = "F"
    ot = "I found **" + str(to) + '** occurance' + occs + ' of "*' + sp + '*" in **' + showref[sn] + "**. ";
    tl = "(" + os.environ.get("BASE_URL") + ")"
    if to > 1:
        tl = "(" + os.environ.get("BASE_URL") + scored(showref[sn], '_') + "/" + scored(sp, '+') + ")"
    lt = nf + "ind more of your favorite phrases at [" + os.environ.get("WEB_URL") + "]" + tl + "."
    if to > 1:
        lt = "See the other **" + str(to - 1) + "** results and " + lt
    reply = "I was unnable to find any matching phrases in ***" + showref[sn] + "***." + "\n\n" + lt
    if to > 0:
        r = o[0]
        if r["Season"] > 0 or r["Episode"] > 0:
            et = "> season " + str(r["Season"]) + " episode " + str(r["Episode"]) + "  \n";
        else:
            et = ""
        nt = "> **" + r["EpisodeName"] + "** ";
        tt = "> Found between " + time_str(r["Start"]) + " and " + time_str(r["End"]) + ". ";
        reply = ot + "\n\n" + et + nt + "  \n" + tt + "\n\n" + lt;

    return reply


def scored(s, j):
    p = s.split()
    sp = j.join(p)
    return sp


def unscored(s, j):
    p = s.split(j)
    sp = (' ').join(p)
    return sp


def time_str(t):
    return str(datetime.timedelta(seconds = t))


def request_episodes(p, s):
    if "*" in p:
        sa = p.split("*")
        sn = sa[1].lower()
        if sn in showref:
            show = scored(showref[sn], '_')
            sa.pop(1)
            if sa[1] != '':
                pa = sa[1]
                np = pa.split()
            else:
                np = sa[0].split()
                np.pop(0)
        else:
            return [False, "I am sorry to say I have not seen this show yet. I'll try to get it added as soon as possible!"]
    else:
        np = p.split()
        np.pop(0)
        if s in showref:
            show = scored(showref[s], '_')
        else:
            return [False, "Hmm I'm not sure what show you are interested in, please specify the show name inside a pair of asterisks!"]
    if len(np) <= 1:
        return [False, "Sorry I need at least two words to make a search for that phrase."]
    search = '+'.join(np)
    url = os.environ.get("API_URL") + show + "/?phrase=" + search
    res = requests.get(url)
    if res.status_code == 200:
        sn = unscored(show.lower(), '_')
        return [True, res.json(), ' '.join(np), sn]

    elif res.status_code == 303:
        url = res.headers.location
        nres = requests.get(url)
        if nres.status_code == 200:
            sn = unscored(show.lower(), '_')
            return [True, nres.json(), ' '.join(np), sn]

        else:
            return [False, "Hmmm I wasn't able to find anything for this request. Maybe try again at [" + os.environ.get("WEB_URL") + "](" + os.environ.get("BASE_URL") + ")."]

    else:
        return [False, "Hmmm I wasn't able to find anything for this request. Maybe try again at [" + os.environ.get("WEB_URL") + "](" + os.environ.get("BASE_URL") + ")."]


load_dotenv()
r = bot_login()
run_bot(r)