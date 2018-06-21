import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def spidey(num):
    my_url = 'http://www.webometrics.info/en/Asia_Pacifico/South%20East%20Asia?page='+num
    response = requests.get(my_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
    page = soup(response.content, "html5lib")
    table = page.find("tbody")
    containers = table.findAll("tr")
    for i in range(0, len(containers)):
        temp = containers[i].findAll('td')
        print(temp[2].text)
        try:
            text_file.write(temp[2].text + "\n")
            text_file2.write(temp[2].a["href"] + "\n")
        except:
            print("hi")




text_file = open("listUni.txt", "w")
text_file2 = open("listUniWeb.txt", "w")
my_url = 'http://www.webometrics.info/en/Asia_Pacifico/South%20East%20Asia'
response = requests.get(my_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
page = soup(response.content, "html5lib")
table = page.find("tbody")
containers = table.findAll("tr")
for i in range(0, len(containers)):
    temp = containers[i].findAll('td')
    text_file.write(temp[2].text + "\n")
    text_file2.write(temp[2].a['href'] + "\n")


for i in range(1,150):
    spidey(str(i))


text_file.close()
text_file2.close()
