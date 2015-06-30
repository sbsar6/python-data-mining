from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET 
import re
root = Tk()

tree = ttk.Treeview(root) 
tree = ET.parse('irelandSetPiece.xml')
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
myArray.count(        
re.split(r',ID:', myArray)       

    
print(myArray)  
for item in Troot.findall('text'):
    print(item.attrib)

for actor in Troot.findall('ID'):
    name = actor.find('real_person:name', ns)
    print(name.text)
    for char in actor.findall('role:character', ns):
        print(' |-->', char.text) 
print (count)
root.mainloop()
