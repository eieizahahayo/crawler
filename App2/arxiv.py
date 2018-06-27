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
    my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=all&order=-announced_date_first&size=50'
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("a")
    links = []
    filename = "arxiv_" + input.replace(" ","_") + ".csv"
    f = open(filename,"w",encoding="utf-16")
    header = "S.No,Title,Subject,date,Journal reference,DOI,Authors\n"
    f.write(header)
    for a in body:
        if("arXiv:" in a.text):
            links.append(a['href'])
    count = 1
    for each in links:
        print("try : " + each)
        f.write(str(count))
        count = crawInfoArxiv(each,f,count)

    start = 50
    for i in range(2,999999):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            print("enter arXiv")
            my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=all&order=-announced_date_first&size=50&start=' + str(start)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a")
            links = []
            for a in body:
                if("arXiv:" in a.text):
                    links.append(a['href'])
            for each in links:
                print("try : " + each)
                f.write(str(count))
                count = crawInfoArxiv(each,f,count)
            start = start + 50
        except Exception as e:
            print("Exception : " + str(e))
            print("Exception page : " + str(i))
            break
    f.close()



def crawInfoArxiv(url,f,count):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":" " , ",":" ","Title:":" ","Authors:":" "}

    #-------------------------S.No---------------------------------
    f.write(" || " + url + ",")


    #-------------------------Title---------------------------------
    try:
        title = body.find("h1",{"class":"title mathjax"})
        print("Title : " + replace_all(title.text,re))
        f.write(replace_all(title.text,re) + ",")
    except Exception as e:
        f.write("Cannot get title,")
        print("Exception Title : " + str(e))

    #-------------------------Subject---------------------------------
    try:
        subj = body.find("span",{"class":"primary-subject"})
        print("Subject : " + replace_all(subj.text,re))
        f.write(replace_all(subj.text,re) + ",")
    except Exception as e:
        f.write("Cannot get subject,")
        print("Exception Subject : " + str(e))

    #-------------------------Date---------------------------------
    try:
        date = body.find("div",{"class":"dateline"})
        print("Date : " + replace_all(date.text,re))
        f.write(replace_all(date.text,re) + ",")
    except Exception as e:
        f.write("Cannot get date,")
        print("Exception Date : " + str(e))

    #-------------------------Ref---------------------------------
    try:
        ref = body.find("td",{"class":"tablecell jref"}).text
        print("Ref : " + replace_all(ref,re))
        f.write(replace_all(ref,re) + ",")
    except Exception as e:
        f.write("Cannot get reference,")
        print("Exception ref : " + str(e))

    #-------------------------DOI---------------------------------
    arr = [{"class":"tablecell doi"},{"class":"tablecell report-number"}]
    check = False
    check2 = False
    try:
        for each in arr:
            try:
                if(check):
                    break
                divDoi = body.find("div","metatable")
                doi = divDoi.find("td",each)
                print("Doi : " + doi.text)
                f.write(doi.text + ",")
                check = True
            except:
                continue
    except Exception as e:
        f.write("Cannot get doi,")
        check2 = True
        print("Exception doi : " + str(e))
    if(check == False and check2 == False):
        f.write("Cannot get doi,")
        print("Cannot get doi")

    #-------------------------Authors---------------------------------
    try:
        divAut = body.find("div",{"class":"authors"})
        auts = divAut.findAll("a")
        for i in range(0,len(auts)):
            if(i == 0):
                print("Authors : " + replace_all(auts[i].text,re))
                f.write(replace_all(auts[i].text,re) + "\n")
            else:
                print(auts[i].text)
                f.write(",,,,,," + replace_all(auts[i].text,re) + "\n")
    except Exception as e:
        f.write("Cannot get authors\n")
        print("Exception Authors : " + str(e))

    print("-------------------------------------------------------------------------------")
    x = count + 1
    return x
