from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup

class GetRegularSeasonGames:


    def __init__(self):
        pass

    def get_games(self):
        url = 'http://www.espn.com/mens-college-basketball/teams'
        schedule_links = []
        team_name = []
        try:
            response = urlopen(url)
            soup = BeautifulSoup(response.read(), 'html.parser')

            for link in soup.find_all('a'):
                if link.get_text() == 'Stats':
                    id = link['href']
                    id = id[24:]
                    team_link = 'http://www.espn.com/mens-college-basketball/team/schedule/_/id/' + str(id)
                    schedule_links.append(team_link)
                if link['href'][0:49] == 'http://www.espn.com/mens-college-basketball/team/':
                    team_name.append(link.get_text())

            team_index = 0

            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute('''DROP TABLE  Games''')
            c.execute('''
                       create table Games (
                           Year integer,
                           Team text,
                           HomeTeam text,
                           AwayTeam text,
                           HomeTeamScore integer,
                           AwayTeamScore numeric,
                           OpponnentRank numeric,
                           TeamWin text)''')

            for link in schedule_links:
                for year in range(2002,2019):
                    response = urlopen(link + '/year/' + str(year))
                    soup = BeautifulSoup(response.read(), 'html.parser')

                    tables = soup.find_all('table')
                    table = tables[0]
                    rows = table.findChildren('tr')

                    for i in range(0,len(rows)):
                        if rows[i]['class'][0] == "stathead" or rows[i]['class'][0] == "colhead":
                            continue
                        if len(rows[i].find_all('td')) == 1:
                            break

                        entries = rows[i].findChildren('li')
                        data_vec = [year, team_name[team_index]]
                        home_team = True
                        won = True
                        opponent_rank = -1
                        status_index = 0

                        try:
                            for entry in entries:

                                if entry['class'][0] == "game-status" and status_index == 0:
                                    if entry.get_text() == '@':
                                        home_team = False
                                    status_index = status_index + 1
                                elif entry['class'][0] == 'game-status' and status_index == 1:
                                    status_index = 0
                                    if entry.get_text() == 'L':
                                        won = False
                                if entry['class'][0] == "team-name":
                                    text = entry.get_text()
                                    if text[0] == '#':
                                        text = text[3:]
                                    if home_team == True:
                                        data_vec.append(team_name[team_index])
                                        text = text.replace('*','')
                                        data_vec.append(text)
                                    else:
                                        text = text.replace('*', '')
                                        data_vec.append(text)
                                        data_vec.append(team_name[team_index])
                                    for row in c.execute(
                                        "select Ranking from KenpomData where YEAR=:year and TEAM=:team",
                                        {"year": year, "team": text}):
                                        for i in row:
                                            try:
                                                opponent_rank = float(i)
                                            except Exception:
                                                opponent_rank = i

                                if entry['class'][0] == 'score':
                                    text = entry.get_text().replace(' OT', '')
                                    index =text.index('-')
                                    if won and home_team:
                                        data_vec.append(text[0:index])
                                        data_vec.append(text[index+1:])
                                    elif won and not home_team:
                                        data_vec.append(text[index + 1:])
                                        data_vec.append(text[0:index])
                                    elif not won and home_team:
                                        data_vec.append(text[index + 1:])
                                        data_vec.append(text[0:index])
                                    else:
                                        data_vec.append(text[0:index])
                                        data_vec.append(text[index + 1:])


                            data_vec.append(opponent_rank)
                            if won == True:
                                data_vec.append("True")
                            else:
                                data_vec.append("False")

                            print(data_vec)
                            temp_tuple = tuple(data_vec)

                            c.execute('insert into Games values (?,?,?,?,?,?,?,?)', temp_tuple)
                            conn.commit()

                        except Exception:
                            continue
                team_index = team_index + 1
            conn.close()


        except sqlite3.Error:
            conn.close()
            self.output_exc()





Instance = GetRegularSeasonGames()
Instance.get_games()
