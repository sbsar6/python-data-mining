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

fix('irelandGame.xml')

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

df = pd.DataFrame(columns = ['Clock',
                             'PhaseID',
                             'PhaseTime',
                             #'PhaseResult',
                             #'RucksNo',
                             'PosGainline',
                             'NegGainline',
                             'Linebreak',
                             'rdNear',
                             'rdRuck',
                             'rdFar',
                             'rdMiddle',
                             'rsSlow',
                             'rsMedium',
                             'rsFast',
                             'Try',
                             #'Turnover',
                             ])
                             
#tree = ttk.Treeview(root) 
tree = etree.parse('150215 Leinster - Dragons XML Edit list.xml')
Troot = tree.getroot()
print(Troot[1][1].tag)
#print(etree.tostring("ID", pretty_print=True))
#for element in Troot.iter("ID"):
#    print("%s - %s" % (element.tag, element.text))


print (tree.iter('ID'))
preIdArr = []     
print (len(Troot))
print (len(Troot[0]))
print (len(Troot[1]))
if Troot.iterfind('TRY'):
    print('found code')
print (Troot[0][0].get("ID"))
myArray = []
tryStats=[]
possStats= []
count = 0
gameClock = 0
altClock= 0
cStart = 0
cEnd = 0
for element in Troot.iter("ID"):
    if element.text =='1':
        print (etree.tostring(element, pretty_print=True))
                


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
            rsSlow =0
            rsMedium= 0
            rsFast= 0
            for instance in item:
                
                for event in instance:
                    
                    if event.text == "Gainline +":
                        print('Gainline positive')
                        posGain +=1
                    if event.text == "Gainline -":
                        negGain +=1
                    if event.text =="Gain LineBreak":
                        linebreak+=1
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
                        
                nPhase = item[3].text
                highPhase = 0    
                #if re.match(r'.:P10+', nPhase):
                 #   print (etree.tostring(item, pretty_print=True))
                                   
                #phaseNum = list(map(int, phaseNum))
                starT = (float(item[1].text))/60
                
                
                endT = float(item[2].text)/60
                
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
                    if phaseNum:
                        print ('phaseNum:' ,phaseNum)
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
                
                try:
                    #myArray.append(count-1)
                    #myArray.append(i)
                    #myArray.append(x)
                    myArray.append(Troot[0][count-1][i].text)
                    
                    x =0
                    
                    for data in instance:
                        if data.text == "Try":
                            print ('Try Scored')
                        #else: print (data.attrib)
                        try:
                            
                            myArray.append(Troot[0][count-1][i][x].text)
                            
                            x +=1
                
                        except:
                            print(i,x,'nothing here')
                            continue
                    i+=1
                except:
                    continue
            df = df.append({'Clock':gameClock,
                                'PhaseID':item[0].text,
                                'PhaseTime':cTemp,
                                #'PhaseResult',
                                #'RucksNo',
                                'PosGainline':posGain,
                                'NegGainline':negGain,
                                'Linebreak':linebreak,
                                'rdNear': rdNear,
                                'rdRuck':rdRuck,
                                'rdFar':rdFar,
                                'rdMiddle':rdMiddle,
                                'rsSlow':rsSlow,
                                'rsMedium':rsMedium,
                                'rsFast':rsFast,
                                'Try':tryYN,
                                #'Turnover',])
                                }, ignore_index=True)
df.to_csv("Game_Stats.csv")
for item in tryStats:
    i=0
    
    for child in Troot:
        for item in child:
            for instance in item:
                
                try:
                    if instance.text == str(tryStats[i]):
                        #indent(item)
                        #ElementTree.dump(item)
                        #tryTime =""
                        #start = 0
                        #end = 0
                        print(i)
                        print (str(tryStats[i]))
                        print(item[2].text)
                        print (item[1].text)
                        tryTime = float(item[2].text) -float(item[1].text)
                        print (tryTime)
                        #fullLoc= etree.Element(item)
                        #print (fullLoc)
                        print (etree.tostring(item, pretty_print=True))
                        i+=1
                except: continue
                     
    

    
def PhaseChecker():
    if instance.text == ".:P1":
        phase1time = float(item[2].text) - float(item[1].text)
        phasetimeCount.append()
                    

print ('TrtStats: ' ,tryStats)
print ('Poss Stats' , possStats)
print ('Game Clock =',gameClock)
print ('Alt Clock =',altClock)
