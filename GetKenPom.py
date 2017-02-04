from urllib2 import Request, urlopen, URLError
import sqlite3
from bs4 import BeautifulSoup

class GetData:


    def __init__(self):
        pass

    def get_scores(self):

        year = 2017

        conn = sqlite3.connect('KenPom.db')
        c = conn.cursor()
        c.execute('''
            create table ScoringData (
                Year integer,
                Team text,
                Conf text,
                WL text,
                AdjEM text,
                AdjO numeric,
                ADJD numeric,
                AdjT numeric,
                Luck text,
                SOSAdjEM text,
                SOSOppO numeric,
                SOSOppD numeric,
                NCSOSAdjEm text)''')


        while year != 2001:

            scoring_data = [[]]


            url = 'http://kenpom.com/index.php?y=' + str(year)

            request = Request(url)

            try:
                response = urlopen(request)
                soup = BeautifulSoup(response.read(), 'html.parser')

                for link in soup.find_all('a'):
                    if 'team.php?team=' in link.get('href'):
                        row = link.find_parent('tr')
                        temp_list = []
                        for i in range(1,len(row.contents)):
                                temp_list.append(row.contents[i].get_text())
                        scoring_data.append(temp_list)


            except URLError, e:
                print 'Error Code'

            for i in range(1, len(scoring_data)):

                # don't want 6,8,10,12,14,16,18
                temp_tuple = (year, scoring_data[i][0],
                          scoring_data[i][1],scoring_data[i][2],scoring_data[i][3],scoring_data[i][4],scoring_data[i][6]
                       ,scoring_data[i][8],scoring_data[i][10],scoring_data[i][12], scoring_data[i][14], scoring_data[i][16],
                       scoring_data[i][18])

                c.execute('insert into ScoringData values (?,?,?,?,?,?,?,?,?,?,?,?,?)', temp_tuple )

            conn.commit()

            year -= 1

        conn.close()




Instance = GetData()
Instance.get_scores()
