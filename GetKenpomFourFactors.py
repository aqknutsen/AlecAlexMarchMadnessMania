import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

year = 2018

conn = sqlite3.connect('Database.db')
c = conn.cursor()
c.execute('''DROP TABLE  KenpomFourFactors''')
c.execute('''
    create table KenpomFourFactors (
        Year integer,
        Team text,
        Conf text,
        AdjTempo integer,
        AdjTempoRank integer,
        AdjOE integer,
        AdjOERank integer,
        eFGPerOff integer,
        eFGPerRankOff  integer,
        TOPerOff integer,
        TOPerRankOff integer,
        ORPerOff integer,
        ORPerRankOff integer,
        FTRateOff integer,
        FTRateRankOff integer,
        ADjDe integer,
        AdjDeRank integer,
        eFGPerDeff integer,
        eFGPerRankDeff  integer,
        TOPerDeff integer,
        TOPerRankDeff integer,
        ORPerDeff integer,
        ORPerRankDeff integer,
        FTRateDeff integer,
        FTRateRankDeff integer)''')


chromedriver = 'C:\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get('https://kenpom.com/')

list = browser.find_elements_by_xpath("//form[@id='login']/input")

i = 0
for  item in list:
        if i == 0:
            item.send_keys("aqknutsen@gmail.com")
            i += 1
        elif i == 1:
            item.send_keys("Aqk052695$")
            i += 1
        else:
            break



browser.find_element_by_name("submit").click()

element = WebDriverWait(browser, 5).until(
 EC.presence_of_element_located((By.CLASS_NAME, "stats")))

element_to_hover_over = browser.find_element_by_class_name("stats")

hover = ActionChains(browser).move_to_element(element_to_hover_over)
hover.perform()

browser.find_element_by_link_text("Four Factors").click()



while year != 2001:

    scoring_data = [[]]

    try:
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        i = 0
        for link in soup.find_all('a'):
            if 'team.php?team=' in link.get('href'):
                if i == 0 or i == 1:
                    i += 1
                    continue

                row = link.find_parent('tr')
                temp_list = []
                try:
                    count = 0
                    for i in range(0, len(row.contents)):
                        if (row.contents[0] != "\n" and row.contents[0] != " ") and  i % 2 != 0:
                            continue
                        elif (row.contents[0] == "\n" or row.contents[0] == " ") and i % 2 == 0:
                            continue
                        l = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        if count == 0:
                            text = row.contents[i].get_text()
                            st_res = ""
                            for ch in text:
                                if ch not in l:
                                    st_res += ch

                            st_res = st_res.strip()
                            if st_res[len(st_res) - 3] == 'S' and st_res[len(st_res) - 2] == 't' and st_res[
                                        len(st_res) - 1] == '.':
                                st_res = st_res.replace('St.', 'State')
                            if "McNeese" in st_res:
                                st_res = st_res.replace('State', '')
                                st_res = st_res.strip()
                            if "Central Connecticut State" in st_res or "Troy State" == st_res:
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
                                st_res = st_res.replace('Cal St.', 'CSU')
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
                                st_res = st_res.replace('Chicago', '(Chi)')
                            if st_res == "College of Charleston":
                                st_res = st_res.replace("College of ", '')
                            if st_res == "North Carolina A&T" or st_res == "Texas A&M":
                                st_res += ";"
                            if st_res == "Miami ":
                                st_res = st_res.replace(" ", "")
                            temp_list.append(st_res)
                            count += 1
                        else:
                            text = row.contents[i].get_text()
                            try:
                                text = int(text)
                                temp_list.append(text)
                            except Exception:
                                temp_list.append(text)
                    print(temp_list)
                    scoring_data.append(temp_list)
                except Exception:
                    print("Exception")
                    continue

    except Exception:
        print('Error Code')
    print(year)
    for i in range(1, len(scoring_data)):
        temp_tuple = (year, scoring_data[i][0],
                      scoring_data[i][1], scoring_data[i][2], scoring_data[i][3], scoring_data[i][4],
                      scoring_data[i][5]
                      ,scoring_data[i][6], scoring_data[i][7], scoring_data[i][8], scoring_data[i][9],
                      scoring_data[i][10],
                      scoring_data[i][11],scoring_data[i][12],scoring_data[i][13],scoring_data[i][14],
                      scoring_data[i][15],scoring_data[i][16],scoring_data[i][17],scoring_data[i][18]
                     ,scoring_data[i][19],scoring_data[i][20],scoring_data[i][21],scoring_data[i][22]
                     ,scoring_data[i][23])

        c.execute('insert into KenpomFourFactors values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp_tuple)
    conn.commit()

    year -= 1
    y = str(year)
    browser.find_element_by_link_text(y).click()

conn.close()



