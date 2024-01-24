from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from IPython.display import display

# res = requests.get("https://www.nba.com/games")

# res_str = str(res.text)

# bs_str = BeautifulSoup(res_str, "html.parser")

# scripts = bs_str.find_all("script")[-2]
# info = json.loads(scripts.text)

# gamecards = info['props']['pageProps']['gameCardFeed']

# cards = gamecards['modules'][0]['cards']
# for card in cards:
#     card_data = card['cardData']
#     gametime_utc = card_data['gameTimeUtc']
#     home_team = card_data['homeTeam']['teamTricode']
#     away_team = card_data['awayTeam']['teamTricode']
#     game_id = card_data['gameId']
#     print("{}: {} - {} @ {}".format(game_id, home_team, away_team, gametime_utc))
#     player_stats = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id).player_stats.get_json()
#     print(player_stats)
#     denver = "0022300614"
#     print(boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=denver).player_stats.get_json())

def getData():
    res2 = requests.get("https://basketballmonster.com/boxscores.aspx")
    res2_text = res2.text
    bs_res2 = BeautifulSoup(res2_text, "html.parser")
    tables = bs_res2.find_all("table")
    data = []
    for table in tables:
        prev = table.parent.previous_sibling
        if prev != None:
            if "@" in prev.text:
                list_header = []
                header = table.find("tr")
                for items in header:
                    try:
                        list_header.append(items.get_text())
                    except:
                        continue
                HTML_data = table.find_all("tr")[1:]
                for element in HTML_data:
                    sub_data = []
                    for sub_element in element:
                        try:
                            if "Team" not in sub_element.get_text() and "Rank" not in sub_element.get_text():
                                sub_data.append(sub_element.get_text())
                        except:
                            continue
                    if "Totals" not in sub_data and sub_data != [] and "Team" not in sub_data and "Rank" not in sub_data:
                        data.append(sub_data)
    return data, list_header

def createDataFrame(data, list_header):
    dataFrame = pd.DataFrame(data = data, columns = list_header)
    df = dataFrame.where(dataFrame['Name'].str.len() > 3).dropna()
    df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to', 'fga', 'fta']] = df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to' ,'fga', 'fta']].apply(pd.to_numeric)
    df['FG'] = round(df['fga'] * df['fg%']).astype(int).astype(str) + "/" + df['fga'].astype(str)
    df['FT'] = round(df['fta'] * df['ft%']).astype(int).astype(str) + "/" + df['fta'].astype(str)
    df['Fantasy Points'] = df['pts'] + (df['reb'] * 1.2) + (df['ast'] * 1.5) + (df['blk'] * 3) + (df['stl'] * 3) - (df['to']) 
    df.sort_values(by = 'Value', ascending=True, inplace=True)
    df = renameColumns(df)
    return df

def renameColumns(dataFrame):
    return dataFrame.rename(columns = {"min": "Min", "3" : "3M", "pts" : "PTS", "reb" : "REB", "ast" : "AST", "stl" : "STL", "blk" : "BLK", "to" : "TO"})
    

def getBestPlayers(dataFrame):
    dataFrame.sort_values(by = 'Value', ascending = False, inplace = True)
    dataFrame = dataFrame[['Name', 'Min', 'FG', 'FT', '3M', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'Fantasy Points', 'Value']].dropna().head(10)
    dataFrame['rank'] = dataFrame['Value'].rank(ascending = False, method = 'first').astype(int)
    firstColumn = dataFrame.pop('rank')
    dataFrame.insert(0, 'Rank', firstColumn)
    return dataFrame

def getWorstPlayers(dataFrame):
    dataFrame.sort_values(by = 'Value', ascending=True, inplace=True)
    dataFrame = dataFrame[['Name', 'Min', 'FG', 'FT', '3M', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'Fantasy Points', 'Value']].where(df['Min'].str.split(':').str[0].astype(int) >= 25).dropna().head(10)
    dataFrame[['3M', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']] = dataFrame[['3M', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']].astype(int)
    dataFrame['rank'] = dataFrame['Value'].rank(ascending = True, method = 'first').astype(int)
    firstColumn = dataFrame.pop('rank')
    dataFrame.insert(0, 'Rank', firstColumn)
    return dataFrame

def printDataFrame(dataFrame):
    display(dataFrame.to_string())

data, list_header = getData()
df = createDataFrame(data, list_header)
worstPlayersDF = getWorstPlayers(df)
printDataFrame(worstPlayersDF)
bestPlayersDF = getBestPlayers(df)
printDataFrame(bestPlayersDF)