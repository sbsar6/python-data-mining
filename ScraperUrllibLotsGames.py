import urllib
from bs4 import BeautifulSoup
import random
import time
import re
import pandas as pd
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


import re
from bs4 import BeautifulSoup

Urls = ["http://en.espn.co.uk/premiership-2014-15/rugby/match/231903.html",
       "http://en.espn.co.uk/premiership-2014-15/rugby/match/231903.html?view=scorecard"]

home =""
away=""
urlList = []
class scraperUrllib:
    
    def __init__(self,url):
        self.url = url
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}
        self.soup = None
        self.scrap()
        self.result = ""
        self.regex()
        
    def scrap(self):
        req = urllib2.Request(self.url, headers=self.hdr)
        page = urllib2.urlopen(req)
        time.sleep(random.uniform(0.3,0.7))
        self.soup = BeautifulSoup(page)
        
       
    def regex(self):
        regex = '</span> (.+?) <span class="liveSubNavText2">'

        pattern = re.compile(regex)
        self.result = re.findall(pattern,str(self.soup))[0]
    def cleanData(self):
        group = self.soup.find_all("div",{"class":"tabbertab"})
        Group = [i for i in group[3].find_all("tr")]

        List = []
        for value in Group:
            tmp = []
            for i in value.find_all("td"):
                try:
                    try:
                        value = int(i.text.strip().replace('\n\t',''))
                    except Exception as e:
                        value = i.text.strip().replace('\n\t','')
                    if not isinstance(value,int):
                        tmp.append(float(i.text.strip().replace('\n\t','').split('%')[0].split("(")[1])/100.0)
                    else:
                        tmp.append(value)
                except Exception as e:
                    try:
                        tmp.append(float(i.text.strip().replace('\n\t','').split('%')[0])/100.0)
                    except Exception as e:
                        tmp.append(i.text.strip().replace('\n\t',''))
            if len(tmp) == 3:
                List.append(tmp)
        #print(List)
        #print (List[0][0])
        self.home = List[0][0]
        self.away = List[0][1]
        CL = []
        for item in List:
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
        referee = self.soup.find(text ="Referee").findNext('a').text    
        refList = [referee, "Referee", referee]
        CL.append(refList)        
        return CL

        
    def results(self):
        score = self.result.strip().split('-')
        return (score[0],score[1])
    
def main(urlList,path):
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
        scrap_object = scraperUrllib(item)
        
        lists = scrap_object.cleanData()
        result = scrap_object.results()
        
        lists.append(["home","Location", "away"])
        lists.append([result[0],"result",result[1]])
        if (result[0] > result[1]):
            lists.append([1,"win",0])
        elif (result [0] < result[1]):
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
        print (lists[0][0], result[0], ',',lists[0][2], result[1])
        
        #Data.append(dictionary, ignore_index = True)
    Data.head(50)
    Data.to_csv("ScrapedAllGame.csv")
    

    
def https():
        for i in range (1903,2172,2):
            temp = ("http://en.espn.co.uk/premiership-2014-15/rugby/match/23" + str(i)+".html?view=scorecard")
            urlList.append(temp)
        return urlList   
https()
path = r"C:\Users\Andrew\Desktop\python data mining\.csv"
#for item in 
x= main(urlList,path)

