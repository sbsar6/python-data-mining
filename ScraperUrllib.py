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
        print(List)
        print (List[0][0])
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
            else:
                CL.append(item)
        return CL

        
    def results(self):
        score = self.result.strip().split('-')
        return (score[0],score[1]) 
    
def main(url,path):
    scrap_object = scraperUrllib(Urls[1])
    lists = scrap_object.cleanData()
    result = scrap_object.results()
    print(lists)
    dictionary = {}
    
    for list in lists:
        if list[1] == "":
            dictionary['Teams'] = [list[0],list[2]]
        else:
            dictionary[list[1]] = [list[0],list[2]]
            
    dictionary["Result"] = [result[0],result[1]]
    print(dictionary)
    print (lists[0][0], result[0], ',',lists[0][2], result[1])
    Data = pd.DataFrame(dictionary)
    Data.to_csv(path)
    
    return Data
   
path = r"C:\Users\Andrew\Desktop\python data mining\.csv"
x= main(Urls[1],path)



