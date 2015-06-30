from tkinter import *
from tkinter import ttk
from tkinter.ttk import*

import xml.etree.ElementTree as ET
tree = ttk.Treeview(ET.parse('irelandSetPiece.xml'))
Troot = tree.getroot()
for child in Troot:
        print(child.tag, child.attrib)

for neighbor in Troot.iter('ALL_INSTANCES'):
        print(neighbor.attrib)
        
class ImportXML (Frame):

        def __init__(self, master):

                # The group editor must be initialised with the desired group size as decided by the lecturer
                super(ImportXML, self).__init__(master)
                self.master = master
                self.grid()
                self.CreateTree
               
        def CreateTree(self):

                tree = ttk.Treeview(ET.parse('irelandSetPiece.xml'))
                Troot = tree.getroot()
                tree.grid (row =0, column = 0)
                Troot.findall(".")

                for child in Troot:
                  print(child.tag, child.attrib)

                for neighbor in Troot.iter('ALL_INSTANCES'):
                 print(neighbor.attrib)


if __name__ == '__main__':

    root = Tk()
   
    app = ImportXML(root)
    root.mainloop()
