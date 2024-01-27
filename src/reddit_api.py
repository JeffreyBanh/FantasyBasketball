from data import *
import requests
import datetime
import praw

def getRedditAPI():
    # CLIENT_ID = 'eDX7DeW85uiRe6UJNCvl-A'
    # SECRET_KEY = 'tnlVQwNyWEMpQmQuWr8_OS4NV1uUZQ'
    # auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    # accInfo = {
    #     'grant_type' : 'password',
    #     'username': 'clowob',
    #     'password': 'Zsaber123!' 
    # }
    
    # headers = {'User-Agent' : 'RedditAPI/0.0.1'}
    # res = requests.post('https://www.reddit.com/api/v1/access_token', auth = auth, data = accInfo, headers = headers)

    # TOKEN = res.json()['access_token']
    # headers['Authorization'] = f'bearer {TOKEN}'

    reddit = praw.Reddit(
        client_id="eDX7DeW85uiRe6UJNCvl-A",
        client_secret="tnlVQwNyWEMpQmQuWr8_OS4NV1uUZQ",
        password="Zsaber123!",
        user_agent="Fantasybball user agent",
        username="clowob",
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
    output += "\n&#x200B;"
    output += "Players qualified if they played 25 mins or more.\n\n" + "Credits to Basketball Monster for the data!"
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
    # choices = list(subreddit.flair.link_templates.user_selectable())
    # template_id = next(x for x in choices if x["flair_text"] == "Discussion")["flair_template_id"]
    # res = subreddit.submit(title = title, selftext = text, flair_id = template_id)
    # # subreddit.submit("title", flair_id=template_id, url="https://www.news.com/")
    subreddit.submit(title = title, selftext = text)
    # print(subreddit.name)
    # resGet = requests.get('https://oauth.reddit.com/r/fantasybball/about')
    # res = requests.post('https://oauth.reddit.com/api/submit', headers = headers, data = json.dumps(obj))

    # print(res.json())

def main():
    reddit = getRedditAPI()
    data, list_header = getData()
    print(data)
    print(list_header)
    df = createDataFrame(data, list_header)
    worstPlayersDF = getWorstPlayers(df)
    bestPlayersDF = getBestPlayers(df)
    worstValues = worstPlayersDF.values.tolist()
    worstColumns = worstPlayersDF.columns.tolist()
    bestValues = bestPlayersDF.values.tolist()
    bestColumns = bestPlayersDF.columns.tolist()
    worstOutput = textWorseOutput(worstValues, worstColumns)
    today = datetime.date.today()
    d2 = today.strftime("%B %d, %Y")
    worstTitle = "Top 10 Worst Performances of the Night 🤢 {} Night 🤮 ({})".format(worstValues[0][1], d2)
    bestTitle = "Top 10 Performances of the Night 🥹 {} Night 🙌 ({})".format(bestValues[0][1], d2)

    bestOutput = textBestOutput(bestValues, bestColumns)
    # submitReddit(reddit, 'testingTables', bestTitle, bestOutput)
    print(worstPlayersDF)
    print(bestPlayersDF)

main()