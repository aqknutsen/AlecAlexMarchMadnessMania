import urllib.request
import sqlite3
from string import digits
from bs4 import BeautifulSoup
import numpy as np

class ConstructTrainingExamples:
    def __init__(self):
        pass

    def construct_training_data(self):
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        games = []
        games2018 = []
        training_data = []
        testing_data = []
        output_data = []
        information_data_training = []
        information_data_testing = []
        for row in c.execute('SELECT * FROM NCAAGAMESDATA WHERE ROUND=?', (1,)):
            games.append(row)
        for row in c.execute('SELECT * FROM THISYEARSGAMES'):
            games2018.append(row)
        conn.close()

        for row in games:
            #print row
            information_data_training.append(row)
            data_vec1 = []
            self.lookup_stats(row[1], row[0],data_vec1)
            data_vec2 = []
            data_vec2 = self.lookup_stats(row[2], row[0],data_vec2)
            if row[7] == "True":
                output_data.append(1)
            else:
                output_data.append(0)

            for i in range(0,len(data_vec1)):
                data_vec1[i] = data_vec1[i] - data_vec2[i]
            training_data.append(data_vec1)

            #print(information_data[-1])
            #print(training_data[-1])
            #print(output_data[-1])

        for row in games2018:
            # print row
            information_data_testing.append(row)
            data_vec1 = []
            self.lookup_stats(row[1], row[0], data_vec1)
            data_vec2 = []
            data_vec2 = self.lookup_stats(row[2], row[0], data_vec2)
            print(row[1])
            print(len(data_vec1))
            print(len(data_vec2))
            print(row[2])
            for i in range(0, len(data_vec1)):
                data_vec1[i] = data_vec1[i] - data_vec2[i]
            testing_data.append(data_vec1)

        return([information_data_training,training_data,output_data,testing_data, information_data_testing])


    def lookup_stats(self, team, year, data_vec):
        # Do this instead
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        for row in c.execute("select Ranking, AdjEM, AdjO,ADJD,AdjT,Luck,SOSAdjEM,SOSOppO,SOSOppD,NCSOSAdjEm from KenpomData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:

                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)


        for row in c.execute("select APG,TOPG,AssistTurnoverRatio from EspnAssists where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select BLKPG from EspnBlocks where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select PPG,FGMPerGame,FGAPerGame,FGPer,TwoPointPercentage,PPS,AdjustedFieldGoalPer from EspnFieldGoalData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select FTA, FTPercentage from EspnFreeThrows where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select ORPG,DRPG,RPG from EspnReboundData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in  c.execute("select FGPer,THRPer from EspnScoringData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select STPG, TOPG, StealsTurnoverRation from EspnSteals where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select ThreesAttemptedPerGame, ThreePercentage from EspnThreePointData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)
        conn.close()

        return data_vec

