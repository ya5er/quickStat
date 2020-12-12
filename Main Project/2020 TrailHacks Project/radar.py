import requests
from bs4 import BeautifulSoup, Comment

def fetch_player_stats(player_name):
    name = player_name.split()
    if not len(name[1]) <= 5:
        name[1] = name[1][:5]
    name[0] = name[0][:2]
    add_to_url = name[1] + name[0] + "01.html"
    url = "https://www.basketball-reference.com/players/" + name[1][0] + "/" + add_to_url

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tagName = 'table'
    className = 'row_summable sortable stats_table now_sortable'
    idName = "per_game"
    result = soup.find(tagName, id=idName)

    tagName = 'tbody'
    result = soup.find(tagName)
    per_game_stats = result.find_all()

    statList = []
    for stat in per_game_stats:
        statList.append(stat.getText(separator=' '))

    comments = soup.find_all(string=lambda text:isinstance(text,Comment))
    tfoots = []
    for comment in comments:
        comment = BeautifulSoup(str(comment), 'html.parser')
        tfoot = comment.find('tfoot')
        if tfoot:
            tfoots.append(tfoot)

    advanced_stats = tfoots[3].getText(separator=' ').split()
    print(advanced_stats)

    ts_percent = advanced_stats[5]
    ast = advanced_stats[11]
    orb = advanced_stats[8]
    tov = advanced_stats[14]

    ppg = statList[-1]
    ast = statList[-6]
    trb = statList[-7]
    efg1 = statList[-83]
    efg2 = statList[-13]

fetch_player_stats("stephen curry")