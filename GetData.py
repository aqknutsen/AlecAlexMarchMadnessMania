from urllib2 import Request, urlopen, URLError
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup

class GetData:


    def __init__(self):
        pass

    def get_scores(self):

        year = 2017


        conn = sqlite3.connect('ESPNDATA.db')
        c = conn.cursor()
        c.execute('''create table ScoringData
                               (YEAR integer, TEAM text, GP integer, PTS numeric, FGMvsFGA text, FGPer numeric, THRMvsTHRAA text
                              , THRPer numeric, FTMvsFTMA text, FTPer numeric)''')

        while year != 2002:

            count = 1
            scoring_data = [[]]

            while count <= 351:

                if year != 2017:
                    url = 'http://www.espn.com/mens-college-basketball/statistics/team/_' \
                          '/stat/scoring-per-game/sort/avgPoints/year/'+str(year)+'/count/' + str(count)
                else:
                    url = 'http://www.espn.com/mens-college-basketball/statistics/team/_' \
                          '/stat/scoring-per-game/sort/avgPoints/count/' + str(count)

                request = Request(url)

                try:
                    response = urlopen(request)
                    soup = BeautifulSoup(response.read(), 'html.parser')

                    for link in soup.find_all('a'):
                        if 'mens-college-basketball/team/' in link.get('href'):
                            row = link.find_parent('tr')
                            temp_list = []
                            for i in range(1,len(row.contents)):
                                temp_list.append(row.contents[i].get_text())
                            scoring_data.append(temp_list)


                except URLError, e:
                    print 'Error Code'

                count = count + 40

            for i in range(1, len(scoring_data)):


                temp_tuple = (year, scoring_data[i][0],
                          scoring_data[i][1],scoring_data[i][2],scoring_data[i][3],scoring_data[i][4],scoring_data[i][5]
                       ,scoring_data[i][6],scoring_data[i][7],scoring_data[i][8])

                c.execute('insert into ScoringData values (?,?,?,?,?,?,?,?,?,?)', temp_tuple )

            conn.commit()

            year -= 1

        conn.close()




Instance = GetData()
Instance.get_scores()
