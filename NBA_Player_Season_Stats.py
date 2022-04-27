import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd

def get_player_season_stats():
    year = input("Which NBA season do you want to look at? (e.g. 2010): ")
    player = input("Which player do you want to see stats from?: ")
    
    url = "http://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    r = session.get(url)
    #r = requests.get(url, allow_redirects=False)
    r_html = r.text
    soup = BeautifulSoup(r_html, 'html.parser')
    
    table = soup.find_all(class_="full_table")
    
    head = soup.find(class_="thead")
    column_names_raw = [head.text for item in head][0]
    column_names_final = column_names_raw.replace("\n", ",").split(",")[2:-1]
    
    players = []
    
    for i in range(len(table)):
        player_ = []
        
        for td in table[i].find_all("td"):
            player_.append(td.text)
            
        players.append(player_)
        
    df = pd.DataFrame(players, columns=column_names_final).set_index("Player")
    df.index = df.index.str.replace("*", "")
    
    print(df.loc[player])
    
if __name__ == "__main__":
    get_player_season_stats()
        
    