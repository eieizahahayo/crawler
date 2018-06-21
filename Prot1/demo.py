import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'http://www.upvetuniv.edu.in/faculties/veterinary-science/'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
body = page_soup.find('body')
divBody = body.findAll(text=True)
# print(body.text)
for i in range(0,len(divBody)):
    if('@' in divBody[i]):
        print(divBody[i])
