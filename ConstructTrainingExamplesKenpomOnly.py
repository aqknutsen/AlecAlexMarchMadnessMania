import urllib.request
import sqlite3
from string import digits
from bs4 import BeautifulSoup
import numpy as np

class ConstructTrainingExamplesKenpomOnly:
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
        for row in c.execute('SELECT * FROM NCAAGAMESDATA WHERE ROUND=? AND YEAR>=?', (1,2010)):
            games.append(row)
        for row in c.execute('SELECT * FROM THISYEARSGAMES'):
            games2018.append(row)
        conn.close()

        for row in games:
            information_data_training.append(row)
            data_vec1 = []
            self.lookup_stats(row[1], row[0],data_vec1)
            data_vec2 = []
            data_vec2 = self.lookup_stats(row[2], row[0],data_vec2)
            if row[7] == "True":
                output_data.append(1)
            else:
                output_data.append(0)

            print(data_vec1)
            print(data_vec2)
            for i in range(0,len(data_vec1)):
                data_vec1[i] = data_vec1[i] - data_vec2[i]
            print(row)
            print(len(data_vec1))
            training_data.append(data_vec1)

            #print(information_data[-1])
            #print(training_data[-1])
            #print(output_data[-1])

        for row in games2018:
            # print row
            information_data_testing.append(row)
            data_vec1.append(row[3])
            self.lookup_stats(row[1], row[0], data_vec1)
            data_vec2.append(row[4])
            data_vec2 = self.lookup_stats(row[2], row[0], data_vec2)
            for i in range(0, len(data_vec1)):
                data_vec1[i] = data_vec1[i] - data_vec2[i]
            testing_data.append(data_vec1)

        return([information_data_training,training_data,output_data,testing_data, information_data_testing])


    def lookup_stats(self, team, year, data_vec):
        # Do this instead
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()

        for row in c.execute("select Ranking, AdjEM,Luck,SOSAdjEM,SOSOppO,SOSOppD,NCSOSAdjEm "
                             "from KenpomData where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:

                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)


        for row in c.execute("select AdjustedTempo, AdjustedTempoRank, AvgPossLength, AvgPossLengthRank, "
                             "AvgPossLengthDefense, AvgPossLengthDefenseRank, OffEffAdjusted, "
                             "OffEffAdjustedRank, DefEffAdjusted, DefEffAdjustedRank from KenpomEfficiencyAndTempo where "
                             "YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select eFGPerOff, eFGPerRankOff, TOPerOff, TOPerRankOff, ORPerOff, ORPerRankOff, "
                             "FTRateOff, FTRateRankOff, ADjDe, AdjDeRank, eFGPerDeff, eFGPerRankDeff, TOPerDeff, "
                             "TOPerRankDeff, ORPerDeff, ORPerRankDeff, FTRateDeff, "
                             "FTRateRankDeff from KenpomFourFactors where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select  FTOffense, FTRankOffense, TwoPointOffense, TwoPointRankOffense, "
                             "ThreePointOffense, ThreePointRankOffense, FTDefense, FTRankDefense, "
                             "TwoPointDefense, TwoPointRankDefense, ThreePointDefense, "
                             "ThreePointRankDefense from KenpomPointDistribution where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select AvgHeight, AvgHeightRank, EffHeight, EffHeightRank, CHeight, CHeightRank, "
                             "PFHeight, PFHeightRank, SFHeight, SFHeightRank, SGHeight, SGHeightRank, "
                             "PGHeight, PGHeightRank, Experience, ExperienceRank, Bench, BenchRank, "
                             "Continuity, ContinuityRank from KenpomHeightExperience where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        for row in c.execute("select ThreePer, ThreeRank, TwoPer, TwoRank, FreeThrowPer, "
                             "FreeThrowRank, BlockPer, BlockRank, StealPer, StealRank, "
                             "AssistPer, AssistRank, ThreePointAttemptedPer, "
                             "ThreePointAttemptedRank from KenpomMiscTeamStats  "
                             "where YEAR=:year and TEAM=:team", {"year": year, "team": team}):
            for i in row:
                try:
                    data_vec.append(float(i))
                except Exception:
                    data_vec.append(i)

        conn.close()

        return data_vec
