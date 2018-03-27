from urllib.request import urlopen
import sqlite3
from bs4 import BeautifulSoup

class GetData:


    def __init__(self):
        pass

    def get_scores(self):

        year = 2018

        conn = sqlite3.connect('Database.db')
        c = conn.cursor()
        c.execute('''DROP TABLE  KenpomData''')
        c.execute('''
            create table KenpomData (
                Year integer,
                Team text,
                Conf text,
                Ranking integer,
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

            try:
                response = urlopen('http://kenpom.com/index.php?y=' + str(year))
                soup = BeautifulSoup(response.read(), 'html.parser')


                for link in soup.find_all('a'):
                    if 'team.php?team=' in link.get('href'):
                        row = link.find_parent('tr')
                        temp_list = []
                        for i in range(1,len(row.contents)):
                                temp_list.append(row.contents[i].get_text())
                        scoring_data.append(temp_list)


            except Exception:
                print ('Error Code')

            ranking = 1
            for i in range(1, len(scoring_data)):
                l = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                st_res = ""
                for ch in  scoring_data[i][0]:
                    if ch not in l:
                        st_res += ch
                # don't want 6,8,10,12,14,16,18
                st_res = st_res.strip()
                if st_res[len(st_res)-3] == 'S' and st_res[len(st_res)-2] ==  't' and st_res[len(st_res)-1] == '.':
                    st_res = st_res.replace('St.', 'State')
                st_res = st_res.strip()
                if "McNeese" in st_res:
                    st_res = st_res.replace('State', '')
                    st_res = st_res.strip()
                if "Central Connecticut State" in st_res  or "Troy State" == st_res:
                    st_res = st_res.replace('State', '')
                    st_res = st_res.strip()
                if "Penn" in st_res and "State" not in st_res:
                    st_res = st_res.replace('Penn', 'Pennsylvania')
                if st_res == "Mississippi":
                    st_res = st_res.replace('Mississippi', 'Ole Miss')
                if st_res == "Hawaii":
                    st_res = st_res.replace('ii', 'i\'i')
                if st_res == "Illinois Chicago":
                    st_res = st_res.replace('Illinois Chicago', 'UIC')
                if st_res == "North Carolina State":
                    st_res = st_res.replace('North Carolina', 'NC')
                if st_res == "UTSA":
                    st_res = st_res.replace('UTSA', 'UT San Antonio')
                if st_res == "Louisiana Lafayette":
                    st_res = st_res.replace('Louisiana Lafayette', 'Louisiana')
                if st_res == "Southeastern Louisiana":
                    st_res = st_res.replace('Southeastern', 'SE')
                if st_res == "Miami OH":
                    st_res = st_res.replace('OH', '(OH)')
                if st_res == "Miami FL":
                    st_res = st_res.replace('FL', '')
                if st_res == "Texas A&M; Corpus Chris":
                    st_res = st_res.replace('Texas A&M; Corpus Chris', 'Texas A&M-CC;')
                if st_res == "Mount St. Mary's":
                    st_res = st_res.replace('Mount', 'Mt.')
                if st_res == "Mount St. Mary's":
                    st_res = st_res.replace('Mount', 'Mt.')
                if st_res == "Portland State":
                    st_res = st_res.replace('State', 'St')
                if st_res == "Cal St. Fullerton":
                    st_res = st_res.replace('Cal St.', 'CS')
                if st_res == "Cal St. Northridge":
                    st_res = st_res.replace('Cal St.', 'Cs')
                if st_res == "Cal St. Bakersfield":
                    st_res = st_res.replace('Cal St.', 'CSU')
                if st_res == "Arkansas Pine Bluff":
                    st_res = st_res.replace('Arkansas Pine', 'Arkansas-Pine')
                if st_res == "Loyola MD":
                    st_res = st_res.replace('MD', '(MD)')
                if st_res == "Detroit":
                    st_res = st_res.replace('Detroit', 'Detroit Mercy')
                if st_res == "Arkansas Little Rock":
                    st_res = st_res.replace('Arkansas ', '')
                if st_res == "Connecticut":
                    st_res = st_res.replace('Connecticut', 'UConn')
                if st_res == "Loyola Chicago":
                    st_res = st_res.replace('Chicago','(Chi)')
                if st_res == "College of Charleston":
                    st_res = st_res.replace("College of ", '')

                temp_tuple = (year, st_res.strip(),
                          scoring_data[i][1], ranking,scoring_data[i][2],scoring_data[i][3],scoring_data[i][4],scoring_data[i][6]
                       ,scoring_data[i][8],scoring_data[i][10],scoring_data[i][12], scoring_data[i][14], scoring_data[i][16],
                       scoring_data[i][18])

                c.execute('insert into KenpomData values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp_tuple )
                ranking = ranking + 1
            conn.commit()

            year -= 1

        conn.close()




Instance = GetData()
Instance.get_scores()
