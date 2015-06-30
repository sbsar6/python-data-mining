from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET 
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

from AmpersandFix import *

fix('irelandGame.xml')



#tree = ttk.Treeview(root) 
tree = ET.parse('irelandGame.xml')
Troot = tree.getroot()
myArray=[]
count = 0
i=0
x=0
for x in Troot.findall('code'):
    myArray.append(x.text)

print(myArray)  
print (tree.iter('ID'))
       
   
if Troot.iterfind('LINEOUT'):
    print('found code')
for child in Troot:
    #myArray.append(Troot[0][0][4][0].text)
    #myArray.append(Troot[1][0][0].text)
    

    #print(child.tag, Troot[0][1].text)
    #print(Troot[1][0][1].text)
    for item in child:
        #i =0
        #print(item.tag)
        if item.tag == 'instance':
            count +=1
        
        i = 0
        myArray.append('ID:' + str(count))
        for instance in item:
            
            try:
                #myArray.append(count-1)
                #myArray.append(i)
                #myArray.append(x)
                myArray.append(Troot[0][count-1][i].text)
                
                x =0
                
                for data in instance:
                    try:
                        
                        myArray.append(Troot[0][count-1][i][x].text)
                        
                        x +=1
            
                    except:
                        print(i,x,'nothing here')
                        continue
                i+=1
            except:
                continue
arr=[]
arr = myArray[1:31]
Time1 = float(arr[2]) - float(arr[1])
print('Time of Event: ', Time1)
arr1= dict()
print (arr)
print (myArray[0])
arr1[myArray[0]] = arr       
Lineouts = myArray.count(":LINEOUT")
Scrums = myArray.count(":SCRUM") + myArray.count("Opposition Scrum")
RucksWon = myArray.count("Ruck Won")
RucksLost = myArray.count("Ruck Lost")
conversions =myArray.count(".CONVERSION")
failedCon = myArray.count('.UNSUCCESSFUL CONVERSION')
phaseCount = []
for i in range(0,10):
    tempPhas = '.:P'+ str(i+1)
    phaseCount.append(myArray.count(tempPhas))
print (phaseCount)    
opPhaseCount = []
for i in range(0,10):
    tempPhas = '.OP'+ str(i+1)
    opPhaseCount.append(myArray.count(tempPhas))
print(opPhaseCount)
oppPhases = myArray.count('.OP10')
Phases = myArray.count('.:P10')
print ('Number of Wales Phases of 10 = ', Phases)
print ('Number of Opp phases of 10 = ', oppPhases)
print ('Number of phases = ', (myArray.count(':PHASE BALL')))



print ('Number of conversions = ', conversions)
print ('Number of missed conversions = ', failedCon)
print ('Number of Rucks Won = ',RucksWon)
print ('Number of Rucks Lost = ',RucksLost)
print ('Number of Lineouts = ',Lineouts)
print ('Number of Scrums = ', Scrums)

xAxis = [1,2,3,4,5,6,7,8,9,10]
plt.figure(1)
plt.plot(xAxis, phaseCount, 'r--', xAxis,opPhaseCount, 'g--' )
plt.text(4, 51, 'red- = Wales, green- =Ireland')
plt.ylabel('Occurance of Phases')
plt.xlabel('Number of Phases in Game')
plt.figure(2)
plt.plot(xAxis,[2.38,0,0,6.25,0,10,0,0,0,0], 'r--', xAxis, [0,0,0,0,0,0,16.67, 0,0,50], 'g--')
plt.show()



#Event1 = re.match(r',ID:2',(myArray.toString))
#print (Event1)
gen2 = []
gen = (i for i,x in enumerate(myArray) if x == 'Ref' )
for i in gen: gen2.append(i)
print (gen2)
#[i for i,x in enumerate(myArray) if x == 'Ruck Lost']
print (count)
d=0
#for i in gen2:
#    print (d)
#    print (myArray[(gen2[d])+4])
#    d+=1

print(myArray[gen2[0]])
print(myArray[63])
print (gen2[0] +1)


def posession(whosePosession):
    posessStats = []
    


def fix(filename):
    #Function ensure the parts of the file are escaped
    #In particular the ampersand in <te

    with open(filename, mode='r', encoding='utf-16-le') as f,open(filename+'.tmp', mode='w', encoding='utf-16-le') as of:
        for line in f:
            # Ensure we only replace tags within the text tags
            match = re.match('<text>.+?<\/text>', line)
            if match:
                #Replace with excaped character
                of.write(line.replace('&', '&amp;'))
            else:
                of.write(line)

    # Clean up files
    f.close()
    of.close()
    # Move the tempory file in place
    os.remove(filename)
    os.rename(filename+'.tmp', filename)
