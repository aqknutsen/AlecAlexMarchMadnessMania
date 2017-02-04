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
                            '''DROP TABLE EspnScoringData'''
                            '''DROP TABLE EspnReboundData'''
                            '''DROP TABLE EspnFieldGoalData'''
                            '''DROP TABLE EspnFreeThrows'''
                            '''DROP TABLE ThreePointData'''
                            '''DROP TABLE EspnAssists'''
                            '''DROP TABLE EspnSteals'''
                            '''DROP TABLE EspnBlocks'''

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
                        ['http://www.espn.com/mens-college-basketball/statistics/team/_/stat/' + statitem + '/year/' + str(
                            year) + '/count/' + str(count), statitem, year])
        return fulllist

    def get_scores(self):

        url_links = self.espnpulls()

        conn = sqlite3.connect('ESPNDATA.db')
        c = conn.cursor()

        prev_stat = ''

        indices_for_database = 0

        for url in range(0, len(url_links)):

            scoring_data = [[]]

            current_stat = url_links[url][1]

            if not current_stat == prev_stat:

                c.execute(self.create_table_queries[indices_for_database])
                indices_for_database+=indices_for_database+1

            request = Request(url_links[url][0])

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
                temp_tuple = (year)
                for j in range(0, len(self.lengths[indices_for_database])):
                    temp_tuple = list(temp_tuple)
                    temp_tuple.insert(scoring_data[i][j+1])
                    temp_tuple= tuple(temp_tuple)

                c.execute(self.insert_queries[indices_for_database], temp_tuple )

            prev_stat = current_stat

            conn.commit()



        conn.close()


Instance = GetData()
Instance.get_scores()
