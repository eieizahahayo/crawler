import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

#-------------------------------------------------------------------------------------------------------------------------------
def springer(input):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    my_url = 'https://link.springer.com/search?query=' + input.replace(" ","+")
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    now = datetime.datetime.now()
    # f.write("Keyword:," + input + "\nDatabase:,https://link.springer.com/\nDate:," + str(now.isoformat()) +"\n\n")
    header = "S.No,Journal Name,Subtitle,Volume,Keywords,Doi number,Author name,Affiliation\n"
    # f.write(header)
    body = page.findAll("div",{"class":"text"})
    print("---------------------------------------------------------------")
    for each in body:
        #---------------------Title---------------------------
        url = ""
        try:
            link = each.find("a",{"class":"title"})
            url = link['href']
            print("Title : " + link.text)
        except Exception as e:
            print("Exception title : " + str(e))
            print("Cannot get title")

        #---------------------subtitle---------------------------
        try:
            sub = each.find("p",{"class":"subtitle"})
            if(sub == ""):
                card = "yo"
            else:
                print("Subtitle : " + sub.text )
        except Exception as e:
            print("Exception subtitle : " + str(e))
            print("Cannot get subtitle")

        #---------------------Volume---------------------------
        try:
            vol = each.find("p",{"class":"coverage"}).text
            print("Volume : " + vol)
        except Exception as e:
            print("Exception volume : " + str(e))
            print("Cannot get volume")

        try:
            eachInfo(url)
        except Exception as e:
            print("Exception function : " + str(e))
            print("Cannot get kws, authors, and doi")


        print("---------------------------------------------")

def eachInfo(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get("https://link.springer.com" + url + "#about", headers=headers)
    page = soup(response.content, "html5lib")

    #-----------------------key words----------------------------------
    try:
        div = page.find("div",{"class":"u-content u-mb-24"})
        kws = div.findAll("span")
        # kws = div.findAll("span",{"class":"Keyword"}).text
        # print("Keywords : ")
        # for each in kws:
        #     print(each)
        for each in kws:
            print("Keywords : " + each.text)
    except Exception as e:
        print("Exception keywords : " + str(e))
        print("Cannot get keywords")

    #----------------------DOI--------------------------------------
    try:
        doi = page.find("span",{"class":"bibliographic-information__value u-overflow-wrap"}).text
        print("Doi : " + doi)
    except Exception as e:
        print("Exception doi : " + str(e))
        print("Cannot get doi")

    #--------------------Authors---------------------------------------
    try:
        div1 = page.find("div",{"class":"test-authors-affiliations authors-and-affiliations"}).ul
        div2 = page.find("div",{"class":"test-authors-affiliations authors-and-affiliations"}).ol
        try:
            auts = div1.findAll("li")
            dets = div2.findAll("li")
            for each in auts:
                print("Aut : " + each.text)
            for each in dets:
                print("Details : " + each.text)
        except Exception as e:
            aut = div1.find("li")
            print("Aut : " + aut)
            det = div2.find("li")
            print("Detail : " + det)
    except Exception as e:
        div1 = page.find("div",{"class":"editors-and-affiliations"}).ul
        div2 = page.find("div",{"class":"editors-and-affiliations"}).ol
        try:
            auts = div1.findAll("li")
            dets = div2.findAll("li")
            for each in auts:
                print("Aut : " + each.text)
            for each in dets:
                print("Details : " + each.text)
        except Exception as e:
            aut = div1.find("li")
            print("Aut : " + aut)
            det = div2.find("li")
            print("Detail : " + det)











    body = page.findAll("div",{"class":"text"})
