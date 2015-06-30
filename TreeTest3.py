from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET 
#import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

from AmpersandFix import *

fix('irelandGame.xml')

## example data
#mu = 100 # mean of distribution
#sigma = 15 # standard deviation of distribution
#x = mu + sigma * np.random.randn(10000)

#num_bins = 50
## the histogram of the data
#n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
## add a 'best fit' line
#y = mlab.normpdf(bins, mu, sigma)
#plt.plot(bins, y, 'r--')
#plt.xlabel('Smarts')
#plt.ylabel('Probability')
#plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
#
## Tweak spacing to prevent clipping of ylabel
#plt.subplots_adjust(left=0.15)
#plt.show()



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
print ('Number of Lineouts = ',Lineouts)
print ('Number of Scrums = ', Scrums)
#Event1 = re.match(r',ID:2',(myArray.toString))
#print (Event1)
    
print(myArray)  
print (count)

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
