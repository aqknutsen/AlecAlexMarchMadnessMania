from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup

class GetIndividualStats:


    def __init__(self):
        pass

    def get_stats(self):
        url = 'http://www.espn.com/mens-college-basketball/teams'
        player_links = []
        team_name = []
        try:
            response = urlopen(url)
            soup = BeautifulSoup(response.read(), 'html.parser')

            for link in soup.find_all('a'):
                if link.get_text() == 'Stats':
                    id = link['href']
                    id = id[24:]
                    team_link = 'http://www.espn.com/mens-college-basketball/team/roster/_/id/' + str(id)
                    player_links.append(team_link)
                if link['href'][0:49] == 'http://www.espn.com/mens-college-basketball/team/':
                    team_name.append(link.get_text())

            index = 0

            conn = sqlite3.connect('Database.db')
            c = conn.cursor()


            for link in player_links:
                for year in range(2002,2019):
                    response = urlopen(link + '/year/' + str(year))
                    soup = BeautifulSoup(response.read(), 'html.parser')

                    table = soup.find_all('table')[0]
                    rows = table.findChildren('tr')
                    for i in range(0,len(rows)):

                        if rows[i]['class'][0] == 'stathead' or rows[i]['class'][0] == 'colhead':
                            continue
                        entries = rows[i].findAll('td')
                        data_vec = []
                        j=0
                        name = ""

                        for entry in entries:
                            if j == 0 or j == 6:
                                j = j + 1
                            elif j == 1:
                                name = entry.get_text()
                                j = j + 1
                            else:
                                data_vec.append(entry.get_text())
                                j = j + 1

                        print(name)
                        print(year)
                        data_vec.append(year)
                        data_vec.append(team_name[index])
                        data_vec.append(name)
                        print(data_vec)
                        temp_tuple = tuple(data_vec)
                        print('executing')
                        c.execute('UPDATE PlayerStatistics SET Position = ?, Height = ?, Weight = ?, Class = ? WHERE Year=? and Team=? and Name=?', temp_tuple)
                        conn.commit()
                index = index + 1
            conn.close()


        except sqlite3.Error:
            conn.close()
            self.output_exc()





Instance = GetIndividualStats()
Instance.get_stats()
