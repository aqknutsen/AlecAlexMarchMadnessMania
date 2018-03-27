from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup

class GetIndividualStats:


    def __init__(self):
        pass

    def get_stats(self):
        url = 'http://www.espn.com/mens-college-basketball/teams'
        stats_links = []
        team_name = []
        try:
            response = urlopen(url)
            soup = BeautifulSoup(response.read(), 'html.parser')

            for link in soup.find_all('a'):
                if link.get_text() == 'Stats':
                    id = link['href']
                    id = id[24:]
                    team_link = 'http://www.espn.com/mens-college-basketball/team/stats/_/id/' + str(id)
                    stats_links.append(team_link)
                if link['href'][0:49] == 'http://www.espn.com/mens-college-basketball/team/':
                    team_name.append(link.get_text())

            index = 0
            conn = sqlite3.connect('Database.db')
            c = conn.cursor()
            c.execute('''DROP TABLE  PlayerStatistics''')
            c.execute('''
                       create table PlayerStatistics (
                           Year integer,
                           Team text,
                           Name text,
                           GP integer,
                           MINPG numeric,
                           PPG numeric,
                           RPG numeric,
                           APG numeric,
                           SPG numeric,
                           BPG numeric,
                           TPG numeric,
                           FGPer numeric,
                           FTPer numeric,
                           ThreePer numeric,
                           MIN integer,
                           FGM integer,
                           FGA integer,
                           FTM integer,
                           FTA integer,
                           ThreePM integer,
                           ThreePA integer,
                           PTS integer,
                           OFFR integer,
                           DEFR integer,
                           REB integer,
                           AST integer,
                           Turnovers integer,
                           STL integer,
                           BLK integer)''')

            for link in stats_links:
                for year in range(2002,2019):
                    response = urlopen(link + '/year/' + str(year))
                    soup = BeautifulSoup(response.read(), 'html.parser')

                    tables = soup.find_all('table')
                    table1 = tables[0]
                    table2 = tables[1]
                    rows1 = table1.findChildren('tr')
                    rows2 = table2.findChildren('tr')
                    for i in range(0,len(rows1)):

                        if rows1[i]['class'][0] == 'stathead' or rows1[i]['class'][0] == 'colhead' or rows1[i]['class'][0] == 'total':
                            continue
                        entry1 = rows1[i].findAll('td')
                        data_vec = [year, team_name[index]]
                        for entry in entry1:
                            data_vec.append(entry.get_text())

                        entry2 = rows2[i+1].findAll('td')
                        j = 0
                        for entry in entry2:
                            if j == 0:
                                j = 1
                                continue
                            data_vec.append(entry.get_text())
                        print(temp_tuple)
                        temp_tuple = tuple(data_vec)
                        c.execute('insert into PlayerStatistics values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp_tuple)
                        conn.commit()
                index = index + 1
            conn.close()


        except sqlite3.Error:
            conn.close()
            self.output_exc()





Instance = GetIndividualStats()
Instance.get_stats()


