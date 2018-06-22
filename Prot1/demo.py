import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.sciencedirect.com/science/article/pii/B9780123948076001957'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
body = page_soup.find('body')
# divBody = body.findAll(text=True)
try:
    detail = body.find("div",{"class":"text-xs"}).text
    print(detail)
    print("done try 1")
except Exception as e:
    print("Exception1 : " + str(e))


try:
    detail = body.find("p",{"class":"volIssue"}).text
    print(detail)
    f.write(replace_all(detail,re) + ",")
    print("done try 2")
except Exception as e:
    print("Exception2 : " + str(e))

try:
    vol = body.find("p",{"class":"specIssueTitle"}).text
    print(vol)
    f.write(replace_all(vol,re) + ",")
    print("done try 3")
except Exception as e:
    print("Exception3 : " + str(e))
