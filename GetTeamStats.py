from urllib.request import urlopen
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
                            '''create table EspnThreePointData
                                 (YEAR integer, TEAM text, GP integer, PPG numeric, ThreesMadePerGame numeric, ThreesAttemptedPerGame numeric, ThreesMade integer
                                , ThreesAttempted integer, ThreePercentage numeric, TwoPointersMade integer, TwoPointersAttempted integer,
                                 TwoPointPercentage integer, PPS numeric, AdjustedFieldGoalPer numeric )''',
                            '''create table EspnAssists
                                  (YEAR integer, TEAM text, GP integer, AST integer, APG numeric, Turnovers integer, TOPG numeric
                                 , AssistTurnoverRatio numeric)''',
                            '''create table EspnSteals
                                  (YEAR integer, TEAM text, GP integer, STL integer, STPG numeric, Turnovers integer, TOPG numeric
                                 , PF integer, StealsTurnoverRation numeric, StealsPersonalFouls numeric)''',
                            '''create table EspnBlocks
                                  (YEAR integer, TEAM text, GP integer, BLK integer, PF integer, BLKPG numeric, BLKTOPF numeric)''',
                            '''DROP TABLE EspnScoringData''',
                            '''DROP TABLE EspnReboundData''',
                            '''DROP TABLE EspnFieldGoalData''',
                            '''DROP TABLE EspnFreeThrows''',
                            '''DROP TABLE EspnThreePointData''',
                            '''DROP TABLE EspnAssists''',
                            '''DROP TABLE EspnSteals''',
                            '''DROP TABLE EspnBlocks'''

    ]

    insert_queries = ['insert into EspnScoringData values (?,?,?,?,?,?,?,?,?,?)',
                      'insert into EspnReboundData values (?,?,?,?,?,?,?,?,?)',
                      'insert into EspnFieldGoalData values (?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?)',
                      'insert into EspnFreeThrows values (?,?,?,?,?,?,?,?,?)',
                      'insert into EspnThreePointData values (?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?)',
                      'insert into EspnAssists values (?,?,?,?,?,?,?,?)',
                      'insert into EspnSteals values (?,?,?,?,?,?,?,?,?,?)',
                      'insert into EspnBlocks values (?,?,?,?,?,?,?)'
    ]

    statslist = ['scoring-per-game', 'rebounds', 'field-goals', 'free-throws', '3-points', 'assists', 'steals',
                 'blocks']

    lengths = [9, 10, 14, 9, 14, 8, 10, 7]

    def espnpulls(self):
        fulllist = []
        for year in range(2002, 2019):
            for statitem in self.statslist:
                for count in range(1, 360, 40):
                    fulllist.append(
                        ['http://www.espn.com/mens-college-basketball/statistics/team/_/stat/' + statitem + '/year/' + str(
                            year) + '/count/' + str(count), statitem, year])

        return fulllist

    def get_scores(self):

        url_links = self.espnpulls()

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute(self.create_table_queries[8])
        c.execute(self.create_table_queries[9])
        c.execute(self.create_table_queries[10])
        c.execute(self.create_table_queries[11])
        c.execute(self.create_table_queries[12])
        c.execute(self.create_table_queries[13])
        c.execute(self.create_table_queries[14])
        c.execute(self.create_table_queries[15])

        prev_stat = url_links[0][1]

        c.execute(self.create_table_queries[0])

        indices_for_database = 0

        all_tables_created = False

        for url in range(0, len(url_links)):

            scoring_data = [[]]

            current_stat = url_links[url][1]

            if all_tables_created:
                if not current_stat == prev_stat:

                    if prev_stat == 'blocks':

                        indices_for_database = 0

                    else:
                        indices_for_database += 1


            else:
                if not current_stat == prev_stat:

                    if prev_stat == 'blocks':
                        indices_for_database = 0
                        all_tables_created = True

                    else:
                        indices_for_database +=1
                        c.execute(self.create_table_queries[indices_for_database])



            try:
                response = urlopen(url_links[url][0])
                soup = BeautifulSoup(response.read(), 'html.parser')

                for link in soup.find_all('a'):

                    if 'mens-college-basketball/team/' in link.get('href'):

                        row = link.find_parent('tr')

                        temp_list = []
                        for i in range(1,len(row.contents)):
                            temp_list.append(row.contents[i].get_text())

                        scoring_data.append(temp_list)

            except Exception:
                print ('Error Code');

            for i in range(1, len(scoring_data)):
                temp_tuple =[url_links[url][2]]
                for j in range(0, len(scoring_data[i])):
                    temp_tuple.append(scoring_data[i][j])
                    temp_tuple = tuple(temp_tuple)
                    temp_tuple = list(temp_tuple)
                print(temp_tuple)
                c.execute(self.insert_queries[indices_for_database], temp_tuple )

            prev_stat = current_stat

            conn.commit()



        conn.close()


Instance = GetData()
Instance.get_scores()
