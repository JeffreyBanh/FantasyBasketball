from data import *
import requests
import datetime
import praw
import argparse
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env into os.environ

def getRedditAPI():

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        password=os.environ["PASSWORD"],
        user_agent="fantasy_sports_stats",
        username="kdeezburner",
    )
    return reddit

def textWorseOutput(values, columns):
    output = "&#x200B;\n\n"
    pipeColumns = "|" + "|".join(columns) + "|" + "\n"
    output += pipeColumns
    output += "|:-" * len(columns) + "|" + "\n"
    for value in values:
        pipeStats = "|" + "|".join(value) + "|" + "\n"
        output += pipeStats
    output += "\n&#x200B;\n"
    output += "Players qualified if they played 24 mins or more.\n\n" + "Credits to Basketball Monster for the data!"
    return output

def textBestOutput(values, columns):
    output = "&#x200B;\n\n"
    pipeColumns = "|" + "|".join(columns) + "|" + "\n"
    output += pipeColumns
    output += "|:-" * len(columns) + "|" + "\n"
    for value in values:
        pipeStats = "|" + "|".join(value) + "|" + "\n"
        output += pipeStats
    output += "\n&#x200B;"
    output += "Credits to Basketball Monster for the data!\n\n" + "Disclaimer: I'm tweaking the scoring system so any feedback is appreciated"
    return output


def submitReddit(reddit, subreddit, title, text):
    subreddit = reddit.subreddit(subreddit)
    choices = list(subreddit.flair.link_templates.user_selectable())
    template_id = next(x for x in choices if x["flair_text"] == "Discussion")["flair_template_id"]
    res = subreddit.submit(title = title, selftext = text, flair_id = template_id)
    print(res)
    # # subreddit.submit("title", flair_id=template_id, url="https://www.news.com/")
    #subreddit.submit(title = title, selftext = text)
    # print(subreddit.name)
    # resGet = requests.get('https://oauth.reddit.com/r/fantasybball/about')
    # res = requests.post('https://oauth.reddit.com/api/submit', headers = headers, data = json.dumps(obj))

    # print(res.json())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-dr',
        '--dryrun',
        default='1'
    )         
    parser.add_argument(
        '-ot',
        '--output_type',
        help="Output type to use. ie: -ot 'best' | -ot 'worst' | -ot 'both'",
        default='worst'
    )
    args = parser.parse_args()
    dryrun = int(args.dryrun)
    output_type = args.output_type


    # Get reddit obj
    reddit = getRedditAPI()
    # Parse data
    data, list_header = getData()
    
    # Format data
    df = createDataFrame(data, list_header)
    worstPlayersDF = getWorstPlayersValue(df)
    worstValues = worstPlayersDF.values.tolist()
    worstColumns = worstPlayersDF.columns.tolist()
    
    bestPlayersDF = getBestPlayers(df)
    bestValues = bestPlayersDF.values.tolist()
    bestColumns = bestPlayersDF.columns.tolist()
    
    # Outputs
    worstOutput = textWorseOutput(worstValues, worstColumns)
    bestOutput = textBestOutput(bestValues, bestColumns)

    # Get date
    today = datetime.date.today()
    d2 = today.strftime("%B %d, %Y")

    # Format titles
    worstTitle = "Top 10 Worst Performances of the Night 🤢 {} Night 🤮 ({})".format(worstValues[0][1], d2)
    bestTitle = "Top 10 Performances of the Night 🥹 {} Night 🙌 ({})".format(bestValues[0][1], d2)

    if output_type == 'worst':
        if dryrun:
            print(worstOutput)
        else:
            submitReddit(reddit, 'fantasybball', worstTitle, worstOutput)
    elif output_type == 'best':
        if dryrun:
            print(bestOutput)
        else:
            pass
            #submitReddit(reddit, 'fantasybball', bestTitle, bestOutput)
    elif output_type == 'both':
        pass
    else:
        raise SystemExit("-ot {} not valid".format(output_type))


if __name__ == "__main__":
    # python3 reddit_api.py -dr 0 -ot worst to post
    # python3 reddit_api.py -dr 1 -ot worst to print
    main()