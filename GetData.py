from urllib2 import Request, urlopen, URLError
import sqlite3
from bs4 import BeautifulSoup

class GetData:


    def __init__(self):
        pass



    create_table_queries = ['''create table EspnScoringData
                               (YEAR integer, TEAM text, GP integer, PTS numeric, FGMvsFGA text, FGPer numeric, THRMvsTHRAA text
                              , THRPer numeric, FTMvsFTMA text, FTPer numeric)''',
                            '''create table EspnReboundData
                               (YEAR integer, TEAM text, GP integer, OFF integer, ORPG numeric, DEF integer, DRPG numeric
                              , REB integer, RPG numberic)''',
                            '''create table EspnFieldGoalData
                              (YEAR integer, TEAM text, GP integer, PPG numeric, FGMPerGame numeric, FGAPerGame numeric, FGM integer
                             , FGA integer, FGPer numeric, TwoPointersMade integer, TwoPointersAttempted integer,
                              TwoPointPercentage integer, PPS numeric, AdjustedFieldGoalPer numeric )''',
                            '''create table EspnFreeThrows
                              (YEAR integer, TEAM text, GP integer, PPG numeric, FTMPer numeric, FTAPer numeric, FTM integer
                             , FTA integer, FTPercentage numeric )''',
                            '''create table ThreePointData
                                 (YEAR integer, TEAM text, GP integer, PPG numeric, ThreesMadePerGame numeric, ThreesAttemptedPerGame numeric, ThreesMade integer
                                , ThreesAttempted integer, ThreePercentage numeric, TwoPointersMade integer, TwoPointersAttempted integer,
                                 TwoPointPercentage integer, PPS numeric, AdjustedFieldGoalPer numeric )''',
                            '''create table EspnAssists
                                  (YEAR integer, TEAM text, GP integer, AST integer, APG numeric, TO integer, TOPG numeric
                                 , AssistTurnoverRatio numeric)''',
                            '''create table EspnSteals
                                  (YEAR integer, TEAM text, GP integer, STL integer, STPG numeric, TO integer, TOPG numeric
                                 , PF integer, StealsTurnoverRation numeric, StealsPersonalFouls numeric)''',
                            '''create table EspnBlocks
                                  (YEAR integer, TEAM text, GP integer, BLK integer, PF integer, BLKPG numeric, BLKTOPF numeric)''',

    ]

    insert_queries = ['insert into ScoringData values (?,?,?,?,?,?,?,?,?,?)',
                      'insert into EspnReboundData values (?,?,?,?,?,?,?,?,?)',
                      'insert into EspnFieldGoalData values (?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?)',
                      'insert into EspnFreeThrows values (?,?,?,?,?,?,?,?,?)',
                      'insert into ThreePointData values (?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?)',
                      'insert into EspnAssists values (?,?,?,?,?,?,?,?)',
                      'insert into EspnSteals values (?,?,?,?,?,?,?,?,?,?)',
                      'insert into EspnBlocks values (?,?,?,?,?,?,?)'
    ]

    statslist = ['scoring-per-game', 'rebounds', 'field-goals', 'free-throws', '3-points', 'assists', 'steals',
                 'blocks']

    lengths = [9, 10, 14, 9, 14, 8, 10, 7]

    def espnpulls(self):
        fulllist = []
        print 'hello'

        for year in range(2002, 2017):
            for statitem in self.statslist:
                for count in range(1, 360, 40):
                    fulllist.append(
                        'http://www.espn.com/mens-college-basketball/statistics/team/_/stat/' + statitem + '/year/' + str(
                            year) + '/count/' + str(count))
        return fullist

    def get_scores(self):

        url_links = espnpulls

        conn = sqlite3.connect('ESPNDATA.db')
        c = conn.cursor()
        c.execute(self.create_table_queries[0])


        scoring_data = [[]]


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


        for i in range(1, len(scoring_data)):


            temp_tuple = (year, scoring_data[i][0],
                      scoring_data[i][1],scoring_data[i][2],scoring_data[i][3],scoring_data[i][4],scoring_data[i][5]
                   ,scoring_data[i][6],scoring_data[i][7],scoring_data[i][8])

            c.execute(self.insert_queries[0], temp_tuple )

        conn.commit()



        conn.close()


Instance = GetData()
Instance.get_scores()






