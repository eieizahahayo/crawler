import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def spidey(str,name):
    source = requests.get('https://en.wikipedia.org'+str).text
    sp = soup(source, 'lxml')
    context = sp.find('a', rel='nofollow')
    if context is None:
        a = "Don\'t have a URL"
        f.write(name.replace(","," ") + "," + a +"\n")
    else:
        f.write(name.replace(","," ") + "," + context.text +"\n")


my_url = 'https://en.wikipedia.org/wiki/Category:Life_sciences_industry'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
containers = page_soup.find("div",{"id":"mw-pages"})
each = containers.findAll("div",{"class":"mw-category-group"})
filename = "Life_sciences_industry.csv"
f = open(filename,"w")
headers = "Company,Website\n"
f.write(headers)
for i in range(0, len(each)):
    links = each[i].findAll("a")
    for j in range(0,len(links)):
        if(j!=0):
            temp = links[j]["href"]
            name = links[j].text
            spidey(str(temp),name)
f.close()
