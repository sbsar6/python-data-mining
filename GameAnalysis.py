import pandas as pd
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET 
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from lxml import etree
from AmpersandFix import *
from xml.etree import ElementTree
import re
import time

path = "C:\\Users\\Andrew\\Desktop\\python data mining"
dataPath = path +'\\GameData'
game_list = [x[0] for x in os.walk(dataPath)]

for each_file in game_list:
    file_name = os.listdir(each_file)
 
    

#fix method used to remove & sign for some games
fix('150215 LvD.xml')
#indent method to make printing out elements from the tree in a prettier way
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#setting up a dataframe
df = pd.DataFrame(columns = ['Clock',
                             'PhaseID',
                             'PhaseTime',
                             'PhaseName',
                             #'PhaseResult',
                             'RucksNo',
                             'PosGainline',
                             'NegGainline',
                             'Linebreak',
                             'LineBreakPrevPhase',
                             'rdNear',
                             'rdRuck',
                             'rdFar',
                             'rdMiddle',
                             'rsSlow',
                             'rsMedium',
                             'rsFast',
                             'KickTotal',
                             'KickedInfield',
                             'KickedtoTouch',
                             'Try',
                             #'Turnover',
                             ])

                             

tree = etree.parse('150215 LvD.xml')
Troot = tree.getroot()
#print(etree.tostring("ID", pretty_print=True))
#for element in Troot.iter("ID"):
#    print("%s - %s" % (element.tag, element.text))


preIdArr = []     
#print (Troot[0][0].get("ID"))
myArray = []
tryStats=[]
possStats= []
count = 0
gameClock = 0
altClock= 0
cStart = 0
cEnd = 0
preEvent = ["None"]

##for element in Troot.iter("ID"):
##    if element.text =='1':
##        print (etree.tostring(element, pretty_print=True))
                

#Getting information from tree
if len(file_name) >0:
    for file in file_name:
        gameClock = 0
        cEnd=0
        cStart = 0
        for child in Troot[:1]:

            #print (child.tag)
            #print (child.keys())
            
            for item in child:
                    #i =0
                    #print(item.tag)
                    if item.tag == 'instance':
                        count +=1
                    
                    i = 0
                    myArray.append('ID:' + str(count))
                    
                    tryYN= 0
                    posGain = 0
                    negGain = 0
                    linebreak = 0
                    rdNear = 0
                    rdRuck = 0
                    rdFar = 0
                    rdMiddle = 0
                    numRucks = 0
                    rsSlow =0
                    rsMedium= 0
                    rsFast= 0
                    kicksTotal = 0
                    kickInfield = 0
                    kickTouch = 0
                    prePhase = "N/A"
                    LineBreakTest= False
                    for instance in item:
                        
                        for event in instance:
                            #Tally up occurances
                                
                            if event.text == "Gainline +":
                                #print('Gainline positive')
                                posGain +=1
                            if event.text == "Gainline -":
                                negGain +=1
                            if event.text =="Gain LineBreak":
                                #print('Event', event[-1].text)
                                LineBreakTest = True
                                linebreak+=1
                                preEvent.append(PreText)
                            if event.text =="RD - Near":
                                rdNear+=1
                            if event.text =="RD - RUCK":
                                rdRuck+=1
                            if event.text =="RD - Far":
                                rdFar+=1
                            if event.text =="RD - Middle":
                                rdMiddle+=1
                            if event.text =="RS-Average Ball":
                                rsMedium+=1
                            if event.text =="RS- Quick Ball":
                                rsFast+=1
                            if event.text =="RS-Slow Ball":
                                rsSlow+=1
                            if event.text =="Kicks Total":
                                kicksTotal+=1
                            if event.text =="Kicked Infield":
                                kickInfield+=1
                            if event.text =="Kicks to Touch":
                                kickTouch +=1
                            #List the last event that led to linebreak    
                            PreText = event.text
                            if LineBreakTest == True:
                                prePhase = preEvent[-1]
                                #print('PrePhase', prePhase)
                                LineBreakTest = False


                        numRucks = rdNear+rdFar+rdMiddle+rdRuck      
                        nPhase= item[3].text
                        highPhase = 0    
                        #if re.match(r'.:P10+', nPhase):
                         #   print (etree.tostring(item, pretty_print=True))
                                           
                        #phaseNum = list(map(int, phaseNum))
                        starT = (float(item[1].text))/60
                        
                        endT = float(item[2].text)/60
                        possTime =  endT - starT
                        if endT > cEnd:

                            cTemp=0
                            
                            if starT>cEnd:
                                                             
                                cTemp = endT - starT
                                
                            else:
                                cTemp= endT - cEnd
                                #print('start not higher cTemp', cTemp)
                            cEnd= endT
                            
                            cStart =starT
                            
                            gameClock = gameClock + cTemp
                            #print ('Game Clock =',gameClock)
                      
                            
                        '''
                        if currTime > 20:
                            if currTime <21:
                                print('20 Mins Gone')
                        if currTime > 40:
                            if currTime <41:
                                print('40 Mins Gone')
                        if currTime > 60:
                            if currTime <61:
                                print('60 Mins Gone')
                        if currTime > 80:
                            if currTime <81:
                                print('80 Mins Gone')
                    '''
                        if instance.text == "Try":
                            indent(item)
                            ElementTree.dump(item)
                            tryTime =""
                            start = 0
                            end = 0
                            print ('Try Scored')
                            #fullLoc= etree.Element(item)
                            #print (fullLoc)
                            print (etree.tostring(item, pretty_print=True))
                            try:
                                tryID = int(item[0].text)+1
                                tryStats.append(tryID)
                            except: continue    
                            tryYN = 1
                          
                       
                        if instance.text == ":PHASE BALL":
                            pEnd = float(item[2].text)
                            
                            pStart = float(item[1].text)
                            
                            possTime =  pEnd - pStart 
                            print (possTime)
                            possStats.append(possTime)
                            print (item[-1].text)
                                   

                           
                               
                            phase = item[3].text
                            
                            highPhase = 0    
                            
                            phaseNum = re.findall(r'\d+', phase)
                            #if phaseNum:
                            #    print ('phaseNum:' ,phaseNum)
                            phaseNum = list(map(int, phaseNum))
                            
                            try:
                                highNum = phaseNum[-1]
                                print(highNum)
                            except:
                                pass
                            #if phaseNum >highPhase:
                            #    highPhase = phaseNum[0]
                            
                                
                            #print (item[1].text)
                            #possStats.append('Phases :'+ highPhase)
                            
                            #print ('Poss Stats: ', possStats)
                            #print (etree.tostring(item, pretty_print=True))
                        

                            
                    df = df.append({'Clock':gameClock,
                                        'PhaseID':item[0].text,
                                        'PhaseTime':possTime,
                                        'PhaseName':nPhase,
                                        #'PhaseResult',
                                        'RucksNo':numRucks,
                                        'PosGainline':posGain,
                                        'NegGainline':negGain,
                                        'Linebreak':linebreak,
                                        'LineBreakPrevPhase':prePhase,
                                        'rdNear': rdNear,
                                        'rdRuck':rdRuck,
                                        'rdFar':rdFar,
                                        'rdMiddle':rdMiddle,
                                        'rsSlow':rsSlow,
                                        'rsMedium':rsMedium,
                                        'rsFast':rsFast,
                                        'KickTotal':kicksTotal,
                                        'KickedInfield':kickInfield,
                                        'KickedtoTouch':kickTouch,
                                        'Try':tryYN,
                                        #'Turnover',])
                                        }, ignore_index=True)

df.to_csv("Game_Stats.csv")
data = pd.read_csv("Game_Stats.csv")
Data_Play_Ball = data[data["PhaseName"] == "BALL IN PLAY"]
#print(Data_Play_Ball)                     
Data_Play_Ball.to_csv("BiP_Stats.csv")   
Data_Possesion = data[data["PhaseName"] == ":POSSESSION"]
#print(Data_Play_Ball)                     
Data_Possesion.to_csv("Possesion_Stats.csv")  
    
                   

#print ('TryStats: ' ,tryStats)
#print ('Poss Stats' , possStats)
#print ('Game Clock =',gameClock)

