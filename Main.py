import requests
from bs4 import BeautifulSoup

import time
from datetime import timedelta


class NHLTeam:
    def __init__(self, name, roster_url):
        self.name = name
        self.roster_url = roster_url
        self.roster = {}

    def fetch_roster(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        r = requests.get(self.roster_url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser") 
        roster = self.extract_roster(soup) #Call next function
        self.roster = roster

    def extract_roster(self, soup):
        roster = {}
        management_list = {
            'ResponsiveTable Centers Roster__MixedTable': 'Centers',
            'ResponsiveTable Left Wings Roster__MixedTable': 'Left Wings',
            'ResponsiveTable Right Wings Roster__MixedTable': 'Right Wings',
            'ResponsiveTable Defense Roster__MixedTable': 'Defense',
            'ResponsiveTable Goalies Roster__MixedTable': 'Goalies'
        }

        roster_section = soup.find(class_="Roster")
        for key, value in management_list.items():
            players_positions = roster_section.find(class_=key)
            players_list = players_positions.find_all(class_="Table__TR Table__TR--lg Table__even")
            position_roster = {}
            for player_info in players_list:
                player_name = player_info.find_all(class_="Table__TD")[1].a.get_text()
                player_details = [player_info.find_all(class_="Table__TD")[1].a['href'],{
                    "Player Info": {
                        "Age": player_info.find_all(class_="Table__TD")[2].get_text()
                    },
                    "Game Log": {},
                    "Career": {}
                }]
                position_roster[player_name] = player_details
            roster[value] = position_roster
        return roster


    def fetch_player_game_log(self, player_name, player_url, year):
        player_url = player_url.split('/')
        player_url.insert(player_url.index('player') + 1, 'gamelog')
        player_url = '/'.join(player_url) + f'/year/{year}'
    
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        r = requests.get(player_url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        
        Format = soup.find(class_="gamelog br-4 pa4 mb3 bg-clr-white")
        seasons = soup.find_all(class_='mb5')
        
        if not seasons[1:]:
            seasons = soup.find_all(class_='mb4')
        
        game_log = {}
    
    
        for season in seasons[1:]:  # Skip first season as it contains overall stats
            x=2
            Check={}
            games = season.find(class_='Table__TBODY')
            season_name = games.find(class_="totals_row fw-bold ttu Table__TR Table__TR--sm Table__even").find(class_="Table__TD").get_text()
    
            game_log[season_name] = {}
    
            for game in games.children: 
                if game.name != 'tr':
                    continue
                
                columns = game.find_all('td')
                
                if player_name in self.roster['Goalies'].keys():
                    try:
                        columns[14]
                    except:
                        continue
                    
                    goalies_game_details = {
                        "Date": columns[0].get_text(),
                        "Location": "Away" if columns[1].get_text().startswith('@') else "Home",
                        "Opponent": columns[1].get_text(),
                        "Result": columns[2].get_text(),
                        "Games Started": columns[3].get_text(),
                        "Time on Ice per Game": columns[4].get_text(),
                        "Wins": int(columns[5].get_text()),
                        "Losses": int(columns[6].get_text()),
                        "Ties": int(columns[7].get_text()),
                        "Overtime Losses": int(columns[8].get_text()),
                        "Goals Against": int(columns[9].get_text()),
                        "Goals Against Average": columns[10].get_text(), 
                        "Shots Against": int(columns[11].get_text()),
                        "Saves": int(columns[12].get_text()),
                        "Save Percentage": columns[13].get_text(),
                        "Shutouts": int(columns[14].get_text()),
                    }
                    
                    Team_Name = columns[1].get_text().lstrip('@').lstrip('vs')
                    if Team_Name in game_log[season_name]:
                        
                        if Team_Name in Check:
                            Check[Team_Name] = x + 1
                            game_log[season_name][f"{Team_Name}-{Check[Team_Name]}x"] = goalies_game_details
                            x = 2
                            
                        game_log[season_name][f"{Team_Name}-{x}x"] = goalies_game_details 
                        Check[Team_Name] = x
                        x = 2 
                    else:
                        game_log[season_name][Team_Name] = goalies_game_details
                        
                else:
                    try:
                        columns[16]
                    except:
                        continue
                    #GOALIES HAVE DIFF SETTS https://www.espn.com/nhl/player/gamelog/_/id/3634/jonathan-quick
                    skaters_game_details = {
                        "Date": columns[0].get_text(),
                        "Location": "Away" if columns[1].get_text().startswith('@') else "Home",
                        "Result": columns[2].get_text(),
                        "Goals": int(columns[3].get_text()),
                        "Assists": int(columns[4].get_text()),
                        "Points": int(columns[5].get_text()),
                        "Plus/Minus": int(columns[6].get_text()),
                        "Penalty Minutes": int(columns[7].get_text()),
                        "Shots": int(columns[8].get_text()),
                        #"Shot Percentage": columns[9].get_text(),
                        "Powerplay Goals": int(columns[10].get_text()),
                        "Powerplay Assists": int(columns[11].get_text()),
                        "Shorthanded Goals": int(columns[12].get_text()),
                        "Shorthanded Assists": int(columns[13].get_text()),
                        "Game-Winning Goals": int(columns[14].get_text()),   
                        "Time on Ice Per Game": columns[15].get_text(),
                        "Time on Ice Prod": columns[16].get_text(),
                    }
                    
                    Team_Name = columns[1].get_text().lstrip('@').lstrip('vs')
                    if Team_Name in game_log[season_name]:
                        
                        if Team_Name in Check:
                            Check[Team_Name] = x + 1
                            game_log[season_name][f"{Team_Name}-{Check[Team_Name]}x"] = skaters_game_details
                            x = 2
                            
                        game_log[season_name][f"{Team_Name}-{x}x"] = skaters_game_details 
                        Check[Team_Name] = x
                        x = 2 
                    else:
                        game_log[season_name][Team_Name] = skaters_game_details
    
        return game_log
    

def main():
    team_1_url = 'https://www.espn.com/nhl/team/roster/_/name/nyr/new-york-rangers'
    team_2_url = 'https://www.espn.com/nhl/team/roster/_/name/bos/boston-bruins'

    team_1 = NHLTeam("New York Rangers", team_1_url)
    team_2 = NHLTeam("Boston Bruins", team_2_url)

    for team in [team_1,team_2]:
        team.fetch_roster()
        for position, players in team.roster.items():
            for player, details in players.items():
                game_log = team.fetch_player_game_log(player, details[0])
                team.roster[position][player][1]['Game Log'] = game_log
                


if __name__ == "__main__":
    main()
