import pandas as pd
import requests
ChampURL = "https://ddragon.leagueoflegends.com/cdn/14.24.1/data/en_US/champion.json"
ChampResponces = requests.get(ChampURL)
ChampData = ChampResponces.json()
def determine_lane(tags):
    if "Support" in tags:
        return "Bot Lane"
    elif "Mage" in tags or "Assassin" in tags:
        return "Mid Lane"
    elif "Tank" in tags or "Fighter" in tags:
        return "Top Lane"
    elif "Marksman" in tags:
        return "Bot Lane"
    elif "Bruiser" in tags:
        return "Top Lane"
    elif "Jungler" in tags:
        return "Jungle"
    else:
        return "Unknown Lane"
champions = [
    {
        "name": ChampName,
        "roles": ", ".join(ChampInfo["tags"]),
        "lane": determine_lane(ChampInfo["tags"]),
        "attack": ChampInfo["info"]["attack"],
        "defense": ChampInfo["info"]["defense"],
        "magic": ChampInfo["info"]["magic"],
        "difficulty": ChampInfo["info"]["difficulty"]
    }
    for ChampName, ChampInfo in ChampData["data"].items()
]
ChampDF = pd.DataFrame(champions)

ChampDF.to_excel("champions_data.xlsx", index=False)
print("Champion data exported to Excel.")