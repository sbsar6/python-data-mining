from lxml import html

import requests
import urllib
atree = html.parse('http://en.espn.co.uk/premiership-2014-15/rugby/match/231907.html')

page = requests.get('http://en.espn.co.uk/premiership-2014-15/rugby/match/231907.html')
tree= html.fromstring(page.text)
#htmlfile = urllib.urlopen('http://en.espn.co.uk/premiership-2014-15/rugby/match/231907.html')
print(len(tree[1]))
print (tree.iter('SCRUMContent'))
#htmltext = htmlfile.read()
#print (htmltext)
#root = tree.getroot()
#print(tree.root)
aRoot = atree.getroot()
print(html.tostring(aRoot))
matchStats = tree.xpath('//*[@id="rightDiv"]/div[1]/table/tbody/tr[2]/td[1]')
print (matchStats)
#for element in root.iter(h2):
#    print("%s - %s" % (element.tag, element.text))
