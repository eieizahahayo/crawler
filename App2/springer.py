import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

def crawInfo(input,f,count):
    re = {"\n":"" , ",":" " , ";":" "}
    ret = {"\n":"" , ",":"/" , ";":" "}
    url = "https://link.springer.com" + input
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")

    f.write(url + "\n")
    print(url)
    header = "S.No,Journal Name,Volume,Date,Keywords,Doi number,Author name,E-mail,Affiliation\n"
    f.write(header)
    f.write(str(count) + ",")

    title = page.find("h1",{"class":"ArticleTitle"})
    print("Title : " + title.text)
    f.write(replace_all(title.text,ret) + ",")

    volume = page.find("p",{"class":"icon--meta-keyline-before"})
    temp = volume.findAll("span")
    vol = ""
    for each in temp:
        vol = vol + replace_all(each.text,re) + " | "
    print(vol)
    f.write(vol + ",")

    date = page.find("div",{"class":"main-context__column"})
    print(date.div.text)
    f.write(date.div.text + ",")

    try:
        keywords = page.findAll("span",{"class":"Keyword"})
        f.write(keywords[0].text + ",")
    except Exception as e:
        print("Exception keywords : " + str(e))

    doi = page.find("span",{"id" : "doi-url"})
    print(doi.text)
    f.write(doi.text + ",")


    try:
        count = 1
        ul = page.findAll("ul",{"class":"test-contributor-names"})
        authors = ul[1].findAll("li",{"class":"u-mb-2 u-pt-4 u-pb-4"})
        for each in authors:
            if(len(each.text) > 1):
                name = each.span.text
                num = each.ul.text
                print("Authors : " + str(count) + ". " + name + " | " + num + ".")
                try:
                    mail = each.find("a",{"class":"gtm-email-author"})
                    print("Email : " + mail['title'])
                except Exception as e:
                    print("Exception Email : " + str(e))
                count = count + 1
    except Exception as e:
        print("Exception authors : " + str(e))


    try:
        ol = page.find("ol",{"class":"test-affiliations"})
        affi = ol.findAll("li")
        for each in affi:
            print("Affiliation : " + each.text)
    except Exception as e:
        print("Exception Affiliation : " + str(e))

    for i in range(0,len(keywords)):
        if(i == 0):
            print("yo")
        else:
            print("Keywords : " + keywords[i].text)
            f.write(",,,," + keywords[i].text + "\n")
    print("-----------------------------------------------------------")
    f.write("\n")
    x = count +1
    return x

#-------------------------------------------------------------------------------------------------------------------------------
def springer(input):
    for i in range(0,999999):
        if(i == 0):
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://link.springer.com/search?query=' + input.replace(" ","+") + '&facet-content-type=%22Article%22'
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            now = datetime.datetime.now()
            filename = "Springer_" + input.replace(" ","_") + ".csv"
            f = open(filename,"w",encoding="utf-16")
            f.write("Keyword:," + input + "\nDatabase:,https://link.springer.com/\nDate:," + str(now.isoformat()) +"\n\n")
            body = page.findAll("li",{"class":"no-access"})
            print(len(body))
            print("---------------------------------------------------------------")
            count = 1
            for each in body:
                link.append(each.h2.a['href'])
                print("link : " + each.h2.a['href'])
            for each in link:
                count = crawInfo(each,f,count)

        # else:
        #     headers = {
        #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        #     my_url = 'https://www.springer.com/gp/search?facet-type=type__journal&query=' + input.replace(" ","+") + '&submit=Submit'
        #     response = requests.get(my_url, headers=headers)
        #     page = soup(response.content, "html5lib")
        #     now = datetime.datetime.now()
        #     # f.write("Keyword:," + input + "\nDatabase:,https://link.springer.com/\nDate:," + str(now.isoformat()) +"\n\n")
        #     header = "S.No,Journal Name,Subtitle,Volume,Keywords,Doi number,Author name,Affiliation\n"
        #     # f.write(header)
        #     body = page.findAll("div",{"class":"result-item"})
        #     print(len(body))
        #     print("---------------------------------------------------------------")
        #     for each in body:
        #         # print(each.prettify())
        #         print("Title : " + each.a.text)
        #
        #
        #         print("---------------------------------------------")
