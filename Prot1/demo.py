import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests

my_url = 'https://onlinelibrary.wiley.com/doi/10.1111/j.1365-2052.2007.01561.x'


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
response = requests.get(my_url, headers=headers)
page = soup(response.content, "html5lib")
text = page.find("div",{"class":"article-header__correspondence-to"})
print(type(text))
print(text.prettify)
print(text.text)
