import os
from collections import defaultdict
import requests
import pandas as pd
import pyodbc
from dotenv import load_dotenv
load_dotenv()

conn = pyodbc.connect(
     r"Driver={ODBC Driver 17 for SQL Server};"
        r"Server=DESKTOP-JAB9N5J\SQLEXPRESS;"
        "Database=LOLChamps;"
        "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.execute("select * from LOLServers")
servers = cursor.fetchall()
APIKey = os.getenv("RIOT_API_KEY")

def close_connection():
    if conn:
        conn.close()
        print("Database connection closed.")

def fetch_ChampionsData():
    cursor.execute("select * from ChampionsData")
    ChampionData = pd.read_sql(cursor, conn)
    return ChampionData

def fetch_PlayerData(region,PlayerName,TagLine,apiKey):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{PlayerName}/{TagLine}?api_key={APIKey}"
    response = requests.get(url)

    if response.status_code == 200:
      return response.json()
    elif response.status_code == 400:
     print("Bad Request: Check the data you entered")
    elif response.status_code == 401:
      print("Unauthorized:Check your API")
    else:
      print(f"Error {response.status_code}: {response.text}")
    return None


def getpuuid(region, sumName, TagLine, APIKey):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{sumName}/{TagLine}?api_key={APIKey}"
    response = requests.get(url)
    return response.json().get('puuid')

def getMatchID (region, puuid, APIKey):
    count = 50
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={APIKey}"
    response = requests.get(url)
    return response.json()

def fetchMatchData(region, matchIDs, puuid, APIKey,RiotName):
    AllData = []  # To store data from all matches

    for matchID in matchIDs:
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={APIKey}"
        response = requests.get(url)

        if response.status_code == 200:
            matchData = response.json()
            players = []
            for participant in matchData['info']['participants']:
              if participant['puuid'] == puuid:
                players.append({
                    'Name': participant.get('riotIdGameName', f'{RiotName}'),
                    'Champion': participant.get('championName', 'Unknown'),
                    'Role': participant.get('teamPosition', 'Unknown'),
                    'Win': participant.get('win', False)
                })
                AllData.append(players)
        else:
            print(f"Error fetching data for match {matchID}: {response.status_code}")
            return None
    return  AllData
def recommendChampions(playerData):
    champState = defaultdict(lambda: {'wins': 0, 'total': 0})
    flattenData = [item for sublist in playerData for item in sublist]
    for data in flattenData:
        champion = data['Champion']
        win = data['Win']


        champState[champion]['total'] += 1
        if win:
            champState[champion]['wins'] += 1

    champWinRate = []
    for champion , stats in champState.items():
        if stats['total'] >= 5:
            winRate = stats['wins'] / stats['total'] if stats['total'] > 0 else 0
            champWinRate.append({'Champion': champion, 'WinRate': winRate})

    champWinRate.sort(key=lambda x: x['WinRate'], reverse=True)
    topChamp = champWinRate[:3]
    return topChamp


def main():
    sumName = input('Enter your Riot ID (e.g., player): ').strip()
    TagLine = input('Enter your TagLine (e.g., #1234): ').strip()
    print("Available Servers : ")
    for server in servers:
        print(f"- {server[0]} - {server[1]} ")

    try:
        selectedServer = int(input("Select server number: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
    region = None

    for server in servers:
        if server[0] == selectedServer:
            region = server[2]
            break
    if not region:
        print("Server Not Available... ")
    else:
        fetch_PlayerData(region, sumName, TagLine, APIKey)
    puuid = getpuuid(region, sumName, TagLine, APIKey)
    if puuid:
        matchID = getMatchID(region, puuid, APIKey)
        playerData = fetchMatchData(region, matchID, puuid, APIKey, sumName)
        recommend = recommendChampions(playerData)
        print("Recommended Champions:\n")
        for suggestion in recommend:
            print(f"Champion: {suggestion['Champion']} | Win Rate: {suggestion['WinRate'] * 100:.2f}%")
    else:
        print("Failed to fetch PUUID!!!")

main()
close_connection()