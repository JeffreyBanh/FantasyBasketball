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

res2 = requests.get("https://basketballmonster.com/boxscores.aspx")
res2_text = res2.text
bs_res2 = BeautifulSoup(res2_text, "html.parser")
tables = bs_res2.find_all("table")
data = []
for table in tables:
    prev = table.parent.previous_sibling
    if prev != None:
        if "@" in prev.text:
            # empty list
            
            # for getting the header from
            # the HTML file
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

dataFrame = pd.DataFrame(data = data, columns = list_header)
df = dataFrame.where(dataFrame['Name'].str.len() > 3).dropna()
df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to', 'fga', 'fta']] = df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to' ,'fga', 'fta']].apply(pd.to_numeric)
df['FG'] = round(df['fga'] * df['fg%']).astype(int).astype(str) + "/" + df['fga'].astype(str)
df['FT'] = round(df['fta'] * df['ft%']).astype(int).astype(str) + "/" + df['fta'].astype(str)
df['Total Fantasy Points'] = df['pts'] + (df['reb'] * 1.2) + (df['ast'] * 1.5) + (df['blk'] * 3) + (df['stl'] * 3) - (df['to']) 
df.sort_values(by = 'Value', ascending=True, inplace=True)
# display(df.to_string())

# topTen = df[['Name', 'FG', 'FT', 'min', '3', 'pts', 'reb', 'ast', 'stl', 'blk', 'to', 'Total Fantasy Points', 'Value']].head(10)
topTen = df[['Name', 'FG', 'FT', 'min', '3', 'pts', 'reb', 'ast', 'stl', 'blk', 'to', 'Total Fantasy Points', 'Value']].where(df['min'].str.split(':').str[0].astype(int) >= 25).dropna().head(10)

display(topTen.to_string())
            
            # for tr in trs:
            #     ths = tr.find_all("th")
            #     tds = tr.find_all("td")
            #     print(",".join([th.text.strip() for th in ths if th.text != ""]))
            #     print(",".join([td.text.strip() for td in tds]))
