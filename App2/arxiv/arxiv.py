import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import xlsxwriter


def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text


#-------------------------------------------------arXiv------------------------------------------------------------------------------
def arXiv(input):

    filename = "arxiv_" + input.replace(" ","_") + ".xlsx"
    filepath = "arxiv/csv/" + filename
    now = datetime.datetime.now()
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://arxiv.org/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    count = 1
    n = 4

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    print("enter arXiv")
    my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=journal_ref&order=-announced_date_first&size=50'
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("a")
    links = []
    for a in body:
        if("arXiv:" in a.text):
            links.append(a['href'])
    for each in links:
        print("try : " + each)
        n = crawInfoArxiv(each,f,count,n)
        count +=1

    start = 50
    for i in range(2,999999):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            print("enter arXiv")
            my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=journal_ref&order=-announced_date_first&size=50&start=' + str(start)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a")
            links = []
            for a in body:
                if("arXiv:" in a.text):
                    links.append(a['href'])
            for each in links:
                print("try : " + each)
                n = crawInfoArxiv(each,f,count,n)
                count +=1
            start = start + 50
        except Exception as e:
            print("Exception : " + str(e))
            print("Exception page : " + str(i))
            break
    f.close()



def crawInfoArxiv(url,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":" " , ",":" ","Title:":" ","Authors:":" "}

    #-------------------Initialization--------------------------------------------------------
    f.write('A' + str(n) , url)
    print("link : " + url)
    n += 1
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Title')
    f.write('C' + str(n) , 'Subject')
    f.write('D' + str(n) , 'Date')
    f.write('E' + str(n) , 'Ref')
    f.write('F' + str(n) , 'Doi number')
    f.write('G' + str(n) , 'Author name')
    n += 1
    f.write('A' + str(n) , str(count))



    #-------------------------Title---------------------------------
    try:
        title = body.find("h1",{"class":"title mathjax"})
        print("Title : " + replace_all(title.text,re))
        f.write('B' + str(n) , title.text)
    except Exception as e:
        f.write('B' + str(n) , 'Cannot get title')
        print("Exception Title : " + str(e))

    #-------------------------Subject---------------------------------
    try:
        subj = body.find("span",{"class":"primary-subject"})
        print("Subject : " + replace_all(subj.text,re))
        f.write('C' + str(n) , subj.text)
    except Exception as e:
        f.write('C' + str(n) , 'Cannot get subject')
        print("Exception Subject : " + str(e))

    #-------------------------Date---------------------------------
    try:
        date = body.find("div",{"class":"dateline"})
        print("Date : " + replace_all(date.text,re))
        f.write('D' + str(n) , date.text)
    except Exception as e:
        f.write('D' + str(n) , 'Cannot get date')
        print("Exception Date : " + str(e))

    #-------------------------Ref---------------------------------
    try:
        ref = body.find("td",{"class":"tablecell jref"}).text
        print("Ref : " + replace_all(ref,re))
        f.write('E' + str(n) , ref)
    except Exception as e:
        f.write('E' + str(n) , 'Cannot get ref')
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
                f.write('F' + str(n) , doi.text)
                check = True
                print("DOI True 1")
            except:
                continue
    except Exception as e:
        f.write('F' + str(n) , 'Cannot get doi')
        check2 = True
        print("DOI True 2")
        print("Exception doi : " + str(e))
    if(check == False and check2 == False):
        f.write('F' + str(n) , 'Cannot get doi')
        print("Cannot get doi")

    #-------------------------Authors---------------------------------
    try:
        divAut = body.find("div",{"class":"authors"})
        auts = divAut.findAll("a")
        for i in range(0,len(auts)):
            print("Authors : " + replace_all(auts[i].text,re))
            f.write('G' + str(n) , auts[i].text)
            n += 1
    except Exception as e:
        f.write('G' + str(n) , 'Cannot get authors')
        print("Exception Authors : " + str(e))

    print("-------------------------------------------------------------------------------")
    return n
