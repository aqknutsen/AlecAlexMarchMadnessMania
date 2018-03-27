from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup
import re

class GetNCAAOpponents:
    create_table_queries = ['''create table NCAAGAMESDATA
                                   (YEAR integer, Team1 text, Team2 text,Seed1 integer, Seed2 integer, PTS1 numeric, PTS2 numeric, Team1Win text, Round integer)''']
    insert_queries = ['insert into NCAAGAMESDATA values (?,?,?,?,?,?,?,?,?)']

    pattern = []
    pattern1 = [1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,1,2,1,3,1,2,1,4,1,2,1,3,1,2,1,5,6,5]
    pattern2 = [0,1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1,
               2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 5, 6, 5]
    pattern3 = [0,0,0,0,1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1,
               2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1, 5, 6, 5]

    pattern_index = 0;
    def __init__(self):
        pass

    def find_opponents(self):
        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('''DROP TABLE NCAAGAMESDATA''')
        c = conn.cursor()
        c.execute(self.create_table_queries[0])
        for year in range(2002,2018):
            data = []
            pattern = self.pattern1;
            if year < 2004:
                self.pattern = self.pattern1
            elif year < 2011:
                self.pattern = self.pattern2
            else:
                self.pattern = self.pattern3
            self.pattern_index = 0;
            try:
                response = urlopen('https://en.wikipedia.org/wiki/' + str(year) +'_NCAA_Division_I_Men%27s_Basketball_Tournament')
                soup = BeautifulSoup(response.read(), 'html.parser')
                td_list = soup.find_all('td', attrs={'style':'background-color:#f9f9f9;border-color:#aaa;border-style:solid;border-top-width:1px;border-left-width:1px;border-right-width:1px;border-bottom-width:1px;padding:0 2px'})
                seeds_list = soup.find_all('td',attrs={'style':'text-align:center;background-color:#f2f2f2;border-color:#aaa;border-style:solid;border-top-width:1px;border-left-width:1px;border-right-width:1px;border-bottom-width:1px'})
                scores_list = soup.find_all('td',attrs={'style':'text-align:center;border-color:#aaa;border-style:solid;border-top-width:1px;border-left-width:1px;border-right-width:1px;border-bottom-width:1px;background-color:#f9f9f9'})

                i = 0
                while i < len(td_list)-1:

                    temp1 = re.sub("\D", "", seeds_list[i].get_text())
                    temp2 = re.sub("\D", "", seeds_list[i+1].get_text())

                    one_won = True
                    if float(scores_list[i].get_text().replace('*','')) > float(scores_list[i+1].get_text().replace('*','')):
                        one_won = True
                    else:
                        one_won = False
                    teamname1 = td_list[i].get_text()
                    teamname2 = td_list[i+1].get_text()
                    if teamname1[len(teamname1) - 3] == 'S' and teamname1[len(teamname1) - 2] == 't' and teamname1[
                                len(teamname1) - 1] == '.':
                        teamname1 = teamname1.replace('St.', 'State')
                        teamname1 = teamname1.strip()
                    if teamname1[len(teamname1) - 2] == 'S' and teamname1[len(teamname1) - 1] == 't':
                        teamname1 = teamname1.replace('St', 'State')
                        teamname1 = teamname1.strip()
                    if "A&M" in teamname1 and not teamname1 == "Texas A&M-CC":
                        teamname1 = teamname1.replace('A&M', 'A&M;')
                    if "A&T" in teamname1:
                        teamname1 = teamname1.replace('A&T', 'A&T;')
                    if "McNeese" in teamname1:
                        teamname1 = teamname1.replace('State', '')
                    if "Central Connecticut State" == teamname1 or "Troy State" == teamname1:
                        teamname1 = teamname1.replace('State', '')
                        teamname1 = teamname1.strip()
                    if "Penn" in teamname1 and "State" not in teamname1 and "Pennsylvania" not in teamname1:
                        teamname1 = teamname1.replace('Penn', 'Pennsylvania')
                    if teamname1 == "Mississippi":
                        teamname1 = teamname1.replace('Mississippi', 'Ole Miss')
                    if teamname1 == "UC-Santa Barbara":
                        teamname1 = teamname1.replace('UC-Santa', 'UC Santa')
                    if teamname1 == "Hawaii":
                        teamname1 = teamname1.replace('ii', 'i\'i')
                    if teamname1 == "Illinois-Chicago":
                        teamname1 = teamname1.replace('Illinois-Chicago', 'UIC')
                    if teamname1 == "North Carolina State":
                        teamname1 = teamname1.replace('North Carolina', 'NC')
                    if teamname1 == "UNC-Asheville" or "UNC-Wilmington":
                        teamname1 = teamname1.replace('-', ' ')
                    if teamname1 == "UW–Milwaukee":
                        teamname1 = teamname1.replace('UW–', '')
                    if teamname1 == "Central Florida":
                        teamname1 = teamname1.replace('Central Florida', 'UCF')
                    if teamname1 == "UTSA":
                        teamname1 = teamname1.replace('UTSA', 'UT San Antonio')
                    if teamname1 == "Texas San Antonio":
                        teamname1 = teamname1.replace('Texas San Antonio', 'UT San Antonio')
                    if teamname1 == "Louisiana–Lafayette":
                        teamname1 = teamname1.replace('Louisiana–Lafayette', 'Louisiana')
                    if teamname1 == "Louisiana Lafayette":
                        teamname1 = teamname1.replace('Louisiana Lafayette', 'Louisiana')
                    if teamname1 == "St. Mary's":
                        teamname1 = teamname1.replace('St. ', 'Saint ')
                    if teamname1 == "UT Chattanooga":
                        teamname1 = teamname1.replace('UT ', '')
                    if teamname1 == "Southeastern Louisiana":
                        teamname1 = teamname1.replace('Southeastern', 'SE')
                    if teamname1 == "Miami (Ohio)":
                        teamname1 = teamname1.replace('(Ohio)', '(OH)')
                    if teamname1 == "Miami (FL)":
                        teamname1 = teamname1.replace(' (FL)', '')
                    if teamname1 == "Texas A&M CC":
                        teamname1 = teamname1.replace('Texas A&M CC', 'Texas A&M-CC;')
                    if teamname1 == "Mount St. Mary's":
                        teamname1 = teamname1.replace('Mount', 'Mt.')
                    if teamname1 == "St. Joseph's":
                        teamname1 = teamname1.replace('St.', 'Saint')
                    if teamname1 == "Portland State":
                        teamname1 = teamname1.replace('State', 'St')
                    if teamname1 == "Cal State Fullerton":
                        teamname1 = teamname1.replace('Cal State', 'CS')
                    if teamname1 == "Cal State Northridge":
                        teamname1 = teamname1.replace('Cal State', 'Cs')
                    if teamname1 == "Cal State Bakersfield":
                        teamname1 = teamname1.replace('Cal State', 'CSU')
                    if teamname1 == "Texas–Arlington":
                        teamname1 = teamname1.replace('Texas\-', 'UT ')
                        teamname1 = teamname1.replace('–', ' ')
                    if teamname1 == "WKU":
                        teamname1 = teamname1.replace('WKU', 'Western Kentucky')
                    if teamname1 == "Miss Valley State":
                        teamname1 = teamname1.replace('Miss', 'Mississippi')
                    if teamname1 == "Arkansas Pine Bluff":
                        teamname1 = teamname1.replace('Arkansas Pine', 'Arkansas-Pine')
                    if teamname1 == "Long Island":
                        teamname1 = teamname1.replace('Long Island', 'LIU Brooklyn')
                    if teamname1 == "Detroit":
                        teamname1 = teamname1.replace('Detroit', 'Detroit Mercy')
                    if teamname1 == "NC Central":
                        teamname1 = teamname1.replace('NC', 'North Carolina')
                    if teamname1 == "Cal Poly SLO":
                        teamname1 = teamname1.replace(' SLO', '')
                    if teamname1 == "Southern California":
                        teamname1 = teamname1.replace('Southern California', 'USC')
                    if teamname1 == "Connecticut":
                        teamname1 = teamname1.replace('Connecticut', 'UConn')
                    if teamname1 == "Loyola-Chicago":
                        teamname1 = teamname1.replace('Loyola-Chicago', 'Loyola (Chi)')
                    if teamname1 == "College of Charleston":
                        teamname1 = teamname1.replace('College of ', '')
                    if teamname2[len(teamname2) - 3] == 'S' and teamname2[len(teamname2) - 2] == 't' and teamname2[
                                len(teamname2) - 1] == '.':
                        teamname2 = teamname2.replace('St.', 'State')
                    if teamname2[len(teamname2) - 2] == 'S' and teamname2[len(teamname2) - 1] == 't':
                        teamname2 = teamname2.replace('St', 'State')
                        teamname2 = teamname2.strip()
                    if "A&M" in teamname2 and not teamname2 == "Texas A&M-CC":
                        teamname2 = teamname2.replace('A&M', 'A&M;')
                    if "A&T" in teamname2:
                        teamname2 = teamname2.replace('A&T', 'A&T;')
                    if "McNeese" in teamname2:
                        teamname2 = teamname2.replace('State', '')
                        teamname2 = teamname2.strip()
                    if "Central Connecticut State" == teamname2  or "Troy State" == teamname2 :
                        teamname2 = teamname2.replace('State', '')
                        teamname2 = teamname2.strip()
                    if "Penn" in teamname2 and "State" not in teamname2 and "Pennsylvania" not in teamname2:
                        teamname2 = teamname2.replace('Penn', 'Pennsylvania')
                    if teamname2 == "Mississippi":
                        teamname2 = teamname2.replace('Mississippi', 'Ole Miss')
                    if teamname2 == "UC-Santa Barbara":
                        teamname2 = teamname2.replace('UC-Santa', 'UC Santa')
                    if teamname2 == "Hawaii":
                        teamname2 = teamname2.replace('ii', 'i\'i')
                    if teamname2 == "Illinois-Chicago":
                        teamname2 = teamname2.replace('Illinois-Chicago', 'UIC')
                    if teamname2 == "North Carolina State":
                        teamname2 = teamname2.replace('North Carolina', 'NC')
                    if teamname2 == "UNC-Asheville" or "UNC-Wilmington":
                        teamname2 = teamname2.replace('-', ' ')
                    if teamname2 == "UW–Milwaukee":
                        teamname2 = teamname2.replace('UW–', '')
                    if teamname2 == "Central Florida":
                        teamname2 = teamname2.replace('Central Florida', 'UCF')
                    if teamname2 == "UTSA":
                        teamname2 = teamname2.replace('UTSA', 'UT San Antonio')
                    if teamname2 == "Texas San Antonio":
                        teamname2 = teamname2.replace('Texas San Antonio', 'UT San Antonio')
                    if teamname2 == "Louisiana–Lafayette":
                        teamname2 = teamname2.replace('Louisiana–Lafayette', 'Louisiana')
                    if teamname2 == "Louisiana Lafayette":
                        teamname2 = teamname2.replace('Louisiana Lafayette', 'Louisiana')
                    if teamname2 == "St. Mary's":
                        teamname2 = teamname2.replace('St. ', 'Saint ')
                    if teamname2 == "UT Chattanooga":
                        teamname2 = teamname2.replace('UT ', '')
                    if teamname2 == "Southeastern Louisiana":
                        teamname2 = teamname2.replace('Southeastern', 'SE')
                    if teamname2 == "Miami (Ohio)":
                        teamname2 = teamname2.replace('(Ohio)', '(OH)')
                    if teamname2 == "Miami (FL)":
                        teamname2 = teamname2.replace(' (FL)', '')
                    if teamname2 == "Texas A&M CC":
                        teamname2 = teamname2.replace('Texas A&M CC', 'Texas A&M-CC;')
                    if teamname2 == "Mount St. Mary's":
                        teamname2 = teamname2.replace('Mount', 'Mt.')
                    if teamname2 == "St. Joseph's":
                        teamname2 = teamname2.replace('St.', 'Saint')
                    if teamname2 == "Portland State":
                        teamname2 = teamname2.replace('State', 'St')
                    if teamname2 == "Cal State Fullerton":
                        teamname2 = teamname2.replace('Cal State', 'CS')
                    if teamname2 == "Cal State Northridge":
                        teamname2 = teamname2.replace('Cal State', 'Cs')
                    if teamname2 == "Cal State Bakersfield":
                        teamname2 = teamname2.replace('Cal State', 'CSU')
                    if teamname2 == "Texas–Arlington":
                        teamname2 = teamname2.replace('Texas', 'UT')
                        teamname2 = teamname2.replace('–', ' ')
                    if teamname2 == "WKU":
                        teamname2 = teamname2.replace('WKU', 'Western Kentucky')
                    if teamname2 == "Miss Valley State":
                        teamname2 = teamname2.replace('Miss', 'Mississippi')
                    if teamname2 == "Arkansas Pine Bluff":
                        teamname2 = teamname2.replace('Arkansas Pine', 'Arkansas-Pine')
                    if teamname2 == "Long Island":
                        teamname2 = teamname2.replace('Long Island', 'LIU Brooklyn')
                    if teamname2 == "Detroit":
                        teamname2 = teamname2.replace('Detroit', 'Detroit Mercy')
                    if teamname2 == "NC Central":
                        teamname2 = teamname2.replace('NC', 'North Carolina')
                    if teamname2 == "Cal Poly SLO":
                        teamname2 = teamname2.replace(' SLO', '')
                    if teamname2 == "Southern California":
                        teamname2 = teamname2.replace('Southern California', 'USC')
                    if teamname2 == "Connecticut":
                        teamname2 = teamname2.replace('Connecticut', 'UConn')
                    if teamname2 == "Loyola-Chicago":
                        teamname2 = teamname2.replace('Loyola-Chicago', 'Loyola (Chi)')
                    if teamname2 == "College of Charleston":
                        teamname2 = teamname2.replace('College of ', '')

                    data = (year, teamname1,teamname2,temp1,temp2,scores_list[i].get_text(), scores_list[i+1].get_text(), str(one_won),self.pattern[self.pattern_index])
                    c.execute(self.insert_queries[0], data)
                    conn.commit()
                    i += 2
                    self.pattern_index = self.pattern_index + 1
            except Exception:
                    print('here')
        conn.close()

    def print_opponents(self, list):
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                print (list[i][j] + " ")
            print ("")

g = GetNCAAOpponents();
g.find_opponents()

