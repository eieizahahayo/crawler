import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text



#-------------------------------------------------arXiv------------------------------------------------------------------------------
def arXiv(input):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    print("enter arXiv")
    my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=all&source=header'
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("a")
    links = []
    filename = "arxiv" + input + ".csv"
    f = open(filename,"w",encoding="utf-16")
    header = "Title,Subject,date,by\n"
    f.write(header)
    for a in body:
        if("arXiv:" in a.text):
            links.append(a['href'])
    for each in links:
        print("try : " + each)
        crawInfoArxiv(each,f)
    f.close()


def crawInfoArxiv(str,f):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(str, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":" " , ",":" ","Title:":" ","Authors:":" "}

    title = body.find("h1",{"class":"title mathjax"})
    print(replace_all(title.text,re))
    f.write(replace_all(title.text,re) + ",")

    subj = body.find("span",{"class":"primary-subject"})
    print(replace_all(subj.text,re))
    f.write(replace_all(subj.text,re) + ",")

    date = body.find("div",{"class":"dateline"})
    print(replace_all(date.text,re))
    f.write(replace_all(date.text,re) + ",")

    by = body.find("div",{"class":"authors"})
    print(replace_all(by.text,re))
    f.write(replace_all(by.text,re) + "\n")

    print("-------------------------------------------------------------------------------")
