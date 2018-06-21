import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

def spidey(str,web):
    my_url = 'https://en.wikipedia.org/wiki/'+str
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    re = {"\n":" " , ",":" "}
    txt = replace_all(str,re)
    webtxt = replace_all(web,re)
    f.write(txt + "," + my_url + "," + webtxt + "\n")
    print(str)



with open("listUni.txt", "r") as ins:
    uni = []
    for line in ins:
        uni.append(line)

with open("listUniWeb.txt", "r") as ins:
    web = []
    for line in ins:
        web.append(line)

filename = "AsiaUni.csv"
f = open(filename,"w")
headers = "Name,wiki-site,website\n"
f.write(headers)

for i in range(0,len(uni)):
    try:
        spidey(uni[i],web[i])
    except:
        temp = "Page not found,"
        re = {"\n":" " , ",":" "}
        txt = replace_all(uni[i],re)
        webtxt = replace_all(web[i],re)
        f.write(txt + "," + temp + "," + webtxt + "\n" )
        print("Page not found")
f.close()
