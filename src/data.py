from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from IPython.display import display

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
                        if sub_data[9] != '':
                            data.append(sub_data)
    return data, list_header

def createDataFrame(data, list_header):
    dataFrame = pd.DataFrame(data = data, columns = list_header)
    df = dataFrame.where(dataFrame['Name'].str.len() > 3).dropna()
    df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to', 'fga', 'fta', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'toV']] = df[['Value', 'pts', '3', 'reb', 'ast', 'stl', 'blk', 'fg%', 'ft%', 'to', 'fga', 'fta', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'toV']].apply(pd.to_numeric)
    df['FG'] = round(df['fga'] * df['fg%']).astype(int).astype(str) + "/" + df['fga'].astype(str)
    df['FT'] = round(df['fta'] * df['ft%']).astype(int).astype(str) + "/" + df['fta'].astype(str)
    df['Fantasy Points'] = round(df['pts'] + (df['reb'] * 1.2) + (df['ast'] * 1.5) + (df['blk'] * 3) + (df['stl'] * 3) - (df['to']) , 1) 
    df['STL Points'] = [df['sV'].values[x] if df['stl'].values[x] == 0 else df['stl'].values[x] * 3 * df['sV'].values[x] for x in range(len(df['stl']))]
    df['blk Points'] = [df['bV'].values[x] if df['blk'].values[x] == 0 else df['blk'].values[x] * 3 * df['bV'].values[x] for x in range(len(df['blk']))]
    df['to Points'] = [df['toV'].values[x] * 4 if df['to'].values[x] == 0 else df['to'].values[x] * df['toV'].values[x] for x in range(len(df['to']))]
    df['Score'] = round((round(df['fga'] * df['fg%']).astype(int)) * df['fg%V']
    + (round(df['fta'] * df['ft%']).astype(int) * df['ft%V']) 
    + (df['pts'] * df['pV']) 
    + (df['3'] * 1.75 * df['3V']) 
    + (df['reb'] * 1.2 * df['rV'])
    + (df['ast'] * 1.5 * df['aV']) 
    + (df['blk Points']) 
    + (df['STL Points']) 
    + (df['to Points']),1)
    df.sort_values(by = 'Value', ascending=True, inplace=True)
    df = renameColumns(df)
    return df

def renameColumns(dataFrame):
    return dataFrame.rename(columns = {"min": "Min", "3" : "3PM", "pts" : "PTS", "reb" : "REB", "ast" : "AST", "stl" : "STL", "blk" : "BLK", "to" : "TO",})

def getBestPlayers(dataFrame):
    dataFrame.sort_values(by = 'Score', ascending = False, inplace = True)
    dataFrame = dataFrame[['Name', 'Min', 'FG', 'FT', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'Fantasy Points', 'Value', 'Score']].dropna().head(10)
    dataFrame['rank'] = dataFrame['Score'].rank(ascending = False, method = 'first').astype(int)
    firstColumn = dataFrame.pop('rank')
    dataFrame.insert(0, 'Rank', firstColumn)
    dataFrame = dataFrame.astype(str)
    return dataFrame

def getWorstPlayers(dataFrame):
    dataFrame.sort_values(by = ['Score'], ascending=True, inplace=True)
    dataFrame = dataFrame[dataFrame['Min'] != '']
    dataFrame = dataFrame[['Name', 'Min', 'FG', 'FT', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'Fantasy Points', 'Value', 'Score']].where(dataFrame['Min'].str.split(':').str[0].astype(int) >= 24).dropna().head(10)
    dataFrame[['3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']] = dataFrame[['3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']].astype(int)
    dataFrame['rank'] = dataFrame['Score'].rank(ascending = True, method = 'first').astype(int)
    firstColumn = dataFrame.pop('rank')
    dataFrame.insert(0, 'Rank', firstColumn)
    dataFrame['Value'] = round(dataFrame['Value'], 2)
    dataFrame = dataFrame.astype(str)
    return dataFrame


def getWorstPlayersValue(dataFrame):
    dataFrame = dataFrame[dataFrame['Min'] != '']
    dataFrame = dataFrame[['Name', 'Min', 'FG', 'FT', '3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'Fantasy Points', 'Value']].where(dataFrame['Min'].str.split(':').str[0].astype(int) >= 24).dropna().head(10)
    dataFrame[['3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']] = dataFrame[['3PM', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TO']].astype(int)
    dataFrame['rank'] = dataFrame['Value'].rank(ascending = True, method = 'first').astype(int)
    firstColumn = dataFrame.pop('rank')
    dataFrame.insert(0, 'Rank', firstColumn)
    dataFrame.sort_values(by = ['Value'], ascending=True, inplace=True)
    dataFrame = dataFrame.astype(str)
    print(dataFrame['Name'])
    dataFrame['Name'] = dataFrame['Name'].str.replace("fouls", "").str.rstrip()
    return dataFrame

def printDataFrame(dataFrame):
    display(dataFrame.to_string())
