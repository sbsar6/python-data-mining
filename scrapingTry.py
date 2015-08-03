from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://en.espn.co.uk/premiership-2014-15/rugby/match/231907.html"

def get_category_links(section_url):
    html = urlopen(section_url).read()
    soup = BeautifulSoup(html, "lxml")
    boccat = soup.find("td", "liveTblTextGrn")
    category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("td")]
    return category_links
