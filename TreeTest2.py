from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET 
root = Tk()
tree = ttk.Treeview(root) 
tree = ET.parse('irelandSetPiece.xml')
Troot = tree.getroot()
myArray=[]
count = 0
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
        i =0
        #print(item.tag)
        if item.tag == 'instance':
            count +=1  
        myArray.append('ID:' + str(count))
        for instance in item:
            try:
                myArray.append(Troot[0][count-1][i].text)
                i +=1
                if Troot[0][count-1][i].text == '\n':
                    x=0
                    for data in instance:
                        try:
                            myArray.append(Troot[0][count-1][i][x].text)
                            print(hap)
                            if Troot[0][count-1][i][x].text in ('\n'):
                                print ('found an n')
                            if Troot[0][count-1][i][x].text =='\n':
                                print ('found an n')
                                y=0
                                for info in data:
                                    try:
                                        myArray.append(Troot[0][count-1][i][x][y].text)
                                        print('one from bottom level reached')
                                        y +=1
                                        if Troot[0][count-1][i][x][y].text == '\n':
                                            b=0
                                            for stuff in info:
                                                try:
                                                    myArray.append(Troot[0][count-1][i][x][y][b].text)
                                                    print('bottom level reached')
                                                    b +=1
                                                except:
                                                    continue
                                    except:
                                        continue
                            x +=1            
                        except:
                            continue
            except:
                continue

        

        '''use try and catch for lowest level.for instance in item:
                print(instance.tag, Troot[0][2].text)
                for data in instance:
                    print(data.tag, data.attrib)
                    for info in data:
                        print(info.tag, info.attrib)'''
    
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
