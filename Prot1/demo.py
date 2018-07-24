import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import re



my_url = 'https://europepmc.org/search?query=climate&page=1'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
response = requests.get(my_url, headers=headers)
page = soup(response.content, "html5lib")
body = page.findAll("a",{"class":"resultLink linkToAbstract"})
print(len(body))
