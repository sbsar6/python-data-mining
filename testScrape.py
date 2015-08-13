
import random
import time
import re
import pandas as pd


import requests
import re
from bs4 import BeautifulSoup


home =""
away=""
urlList = []


soup = None

def https():
        for i in range (8681,8949,2):
            temp = ("http://en.espn.co.uk/premiership-2013-14/rugby/match/18" + str(i)+".html?view=scorecard")
            urlList.append(temp)
        return urlList
https()
Data = pd.DataFrame(columns = ['Team Name',
                                   'Tries Scored',
                                   'Conversions',
                                   'Penalty Goals',
                                   'Kick at Goal Success',
                                   'Drop Goals',
                                   'Kicks from Hand',
                                   'Passes',
                                   'Runs',
                                   'Metres Run',	
                                   'Possession(%)',
                                   'Clean Breaks',
                                   'Defenders Beaten',
                                   'Offloads',
                                   'Rucks Won',
                                   'Mauls Won',
                                   'Turnovers Conceded',
                                   'Tackles Made',
                                   'Tackles Missed',
                                   'Tackling Success Rate',
                                   'Scrums on own feed',
                                   'Lineouts on own feed',
                                   'Penalties Conceeded',
                                   'Yellow Cards',
                                   'Red Cards',
                                   'Referee',
                                   'Playing Location',
                                   'Result',
                                   'Outcome'
                                   ])
                                   
                                   
for item in urlList: 
    #req = urllib2.Request(item, headers=hdr)
    #page = urllib2.urlopen(req)

    r = requests.get(item)
    page = r.text
    soup = BeautifulSoup(page)
    


    referee = soup.find(text ="Referee").findNext('a').text

    matchDet = soup.find(text ="Match stats").findNext().text


    regex = '</span> (.+?) <span class="liveSubNavText2">'
    pattern = re.compile(regex)
    result = re.findall(pattern,str(soup))[0]
    score = result.strip().split('-')
    print (score)

    #PreMatchBits = matchDet.find(text = "Pos").findAllPrevious('tr')
    FList = []
    List = []
    print(matchDet)
    List = matchDet.replace('\t','').split('\n')
    print(List)
    #replace('\n\t','')
   
      
    while '' in List:
            List.remove('')
    tmp = []
    print(List)
    for i in List:

        if i == '':
            pass
        if i == 'Kick/pass/run':
            pass
        elif i =='Attacking':
            pass
        elif i == 'Defensive':
            pass
        elif i =='Set pieces':
            pass
        elif i == 'Discipline':
            pass
        elif i == 'Mauls won':
                print (tmp[1])
                tmp[1]= 'Mauls won'
                print (tmp)
        elif i == 'Turnovers conceded':
                print(tmp)
                tmp[0] = str(tmp[1])
                tmp[1] = 'Turnovers conceded'
        else:
            try:
                tmp.append(int(i))
            except:
                tmp.append(i)
         
        if len(tmp) == 3:
            FList.append(tmp)
            tmp = []
    print (FList)
    time.sleep(1000)
    CL = []
    for item in FList:
        if item[1] == 'Tackles made/missed':
            CL.append([item[0].split('/')[0],'Tackles made',item[2].split('/')[0]])
            CL.append([item[0].split('/')[1],'Tackles missed',item[2].split('/')[1]])
        elif item[1] == 'Yellow/red cards':
            CL.append([item[0].split('/')[0],'Yellow cards',item[2].split('/')[0]])
            CL.append([item[0].split('/')[1],'Red cards',item[2].split('/')[1]])
        elif item[1] == 'Territory (1H/2H)':
            pass
        else:
            CL.append(item)
    referee = soup.find(text ="Referee").findNext('a').text    
    refList = [referee, "Referee", referee]
    CL.append(refList)    

    
    CL.append(["home","Location", "away"])
    lists = CL
    lists.append([score[0],"result",score[1]])
    if (score[0] > score[1]):
        lists.append([1,"win",0])
    elif (score [0] < score[1]):
        lists.append([0,"win",1])
        
    #print(lists)
    #time.sleep(20)
    try:
        for i in range (0,3,2):
            Data= Data.append({'Team Name':lists[0][i],
                                   'Tries Scored':lists[1][i],
                                   'Conversions':lists[2][i],
                                   'Penalty Goals':lists[3][i],
                                   'Kick at Goal Success':lists[4][i],
                                   'Drop Goals':lists[5][i],
                                   'Kicks from Hand':lists[6][i],
                                   'Passes':lists[7][i],
                                   'Runs':lists[8][i],
                                   'Metres Run':lists[9][i],	
                                   'Possession(%)':lists[10][i],
                                   'Clean Breaks':lists[11][i],
                                   'Defenders Beaten':lists[12][i],
                                   'Offloads':lists[13][i],
                                   'Rucks Won':lists[14][i],
                                   'Mauls Won':lists[15][i],
                                   'Turnovers Conceded':lists[16][i],
                                   'Tackles Made':lists[17][i],
                                   'Tackles Missed':lists[18][i],
                                   'Tackling Success Rate':lists[19][i],
                                   'Scrums on own feed':lists[20][i],
                                   'Lineouts on own feed':lists[21][i],
                                   'Penalties Conceeded':lists[22][i],
                                   'Yellow Cards':lists[23][i],
                                   'Red Cards':lists[24][i],
                                   'Referee':lists[25][i],
                                   'Playing Location':lists[26][i],
                                   'Result':lists[27][i],
                                   'Outcome':lists[28][i]
                               }, ignore_index = True)
            
    except:
        print(lists)
        pass
    #print(dictionary)
    print (lists[0][0], score[0], ',',lists[0][2], score[1])
    
    #Data.append(dictionary, ignore_index = True)

Data.to_csv("EnglishPrem2013.csv")



