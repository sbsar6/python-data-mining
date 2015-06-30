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

#tree = ttk.Treeview(root) 
tree = etree.parse('irelandGame.xml')
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
for element in Troot.iter("instance"):
    if element.text =='Try':
        print (etree.tostring(element, pretty_print=True))
                


for child in Troot:
    print (child.attrib)
    #print (child.tag)
    #print (child.keys())
    
    for item in child:
            #i =0
            #print(item.tag)
            if item.tag == 'instance':
                count +=1
            
            i = 0
            myArray.append('ID:' + str(count))
            for instance in item:
                
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
                    except: continue    
                    
                  

                elif instance.text == ":PHASE BALL":
                    pEnd = float(item[2].text)
                    
                    pStart = float(item[1].text)
                    
                    possTime =  pEnd - pStart 
                    print (possTime)
                    possStats.append(possTime)
                    print (item[-1].text)
                           

                   
                       
                    phase = item[3].text
                    print (phase)
                    highPhase = 0    
                    
                    phaseNum = re.findall(r'\d+', phase)
                    print (phaseNum)
                    phaseNum = list(map(int, phaseNum))
                    print (phaseNum)
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

for i in tryStats:
    for event, element in Troot.iter("instance"):
        if element.text == str(i):
            print (etree.tostring(event, pretty_print=True))


    
def PhaseChecker():
    if instance.text == ".:P1":
        phase1time = float(item[2].text) - float(item[1].text)
        phasetimeCount.append()
                    

print ('TrtStats: ' ,tryStats)

