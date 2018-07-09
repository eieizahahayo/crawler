import bs4
import requests
import xlsxwriter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def crawInfo(input,f,count,n):
    url = "https://link.springer.com" + input
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")

    #----------------------Initialization-----------------------------------------------------------------------------
    f.write('A' + str(n) , url)
    n += 1
    print(url)
    header = "S.No,Title,Journal name,Volume,Date,Keywords,Doi number,Author name,E-mail,Affiliation\n"
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Title')
    f.write('C' + str(n) , 'Journal name')
    f.write('D' + str(n) , 'Volume')
    f.write('E' + str(n) , 'Date')
    f.write('F' + str(n) , 'Keywords')
    f.write('G' + str(n) , 'Doi number')
    f.write('H' + str(n) , 'Author name')
    f.write('I' + str(n) , 'E-mail')
    f.write('J' + str(n) , 'Affiliation')
    n += 1
    f.write('A' + str(n) , str(count))


    #------------------------Title---------------------------------------------------------------------------
    try:
        title = page.find("h1",{"class":"ArticleTitle"})
        print("Title : " + title.text)
        f.write('B' + str(n) , title.text)
    except Exception as e:
        print("Cannot get title : " + str(e))
        f.write('B' + str(n) , 'Cannot get title')

    #------------------------Journal name---------------------------------------------------------------------------
    try:
        jname = page.find("span",{"class":"JournalTitle"})
        print("Journal name : " + jname.text)
        f.write('C' + str(n) , jname.text)
    except Exception as e:
        print("Cannot get journal name : " + str(e))
        f.write('C' + str(n) , jname.text)

    #--------------------------Volume-------------------------------------------------------------------------
    try:
        volume = page.find("p",{"class":"icon--meta-keyline-before"})
        temp = volume.findAll("span")
        vol = ""
        for each in temp:
            vol = vol + each.text + " | "
        print(vol)
        f.write('D' + str(n) , vol)
    except Exception as e:
        print("Cannot get volume : " + str(e))
        f.write('D' + str(n) , 'Cannot get volume')

    #------------------------Date---------------------------------------------------------------------------
    try:
        date = page.find("div",{"class":"main-context__column"})
        print(date.div.text)
        # f.write(date.div.text + ",")
        f.write('E' + str(n) , date.div.text)
    except Exception as e:
        print("Cannot get date : " + str(e))
        f.write('E' + str(n) , 'Cannot get date')

    #------------------------Key words 1---------------------------------------------------------------------------
    try:
        keywords = page.findAll("span",{"class":"Keyword"})
    except Exception as e:
        print("Exception keywords : " + str(e))
        f.write('F' + str(n) , 'Cannot get keywords')


    #----------------------Doi-----------------------------------------------------------------------------
    try:
        doi = page.find("span",{"id" : "doi-url"})
        print(doi.text)
        # f.write(doi.text + ",")
        f.write('G' + str(n) , doi.text)
    except Exception as e:
        print("Exception doi : " + str(e))
        f.write('G' + str(n) , 'Cannot get DOI number')

    #---------------------Authors and email 1------------------------------------------------------------------------------
    authorsArr = []
    mailArr = []
    try:
        count = 1
        ul = page.findAll("ul",{"class":"test-contributor-names"})
        authors = ul[1].findAll("li",{"class":"u-mb-2 u-pt-4 u-pb-4"})
        for each in authors:
            if(len(each.text) > 1):
                name = each.span.text
                num = each.ul.text
                print("Authors : " + name + " | " + num + ".")
                authorsArr.append(name + " | " + num + ".")
                try:
                    mail = each.find("a",{"class":"gtm-email-author"})
                    print("Email : " + mail['title'])
                    mailArr.append(mail['title'])
                except Exception as e:
                    print("Exception Email : " + str(e))
                    mailArr.append("Email is not available")
                count = count + 1
    except Exception as e:
        print("Exception authors : " + str(e))
        authorsArr.append("Cannot get author information")
        mailArr.append("Email is not available")

    #-------------------Affiliation--------------------------------------------------------------------------------
    affiArr = []
    try:
        ol = page.find("ol",{"class":"test-affiliations"})
        affi = ol.findAll("li")
        for each in affi:
            print("Affiliation : " + each.text)
            affiArr.append(each.text)
    except Exception as e:
        print("Exception Affiliation : " + str(e))
        affiArr.append("Cannot get affiliation")

    maximum = max([len(keywords),len(authorsArr),len(mailArr)])
    #------------------------Key words 2---------------------------------------------------------------------------
    kn = n
    for each in keywords:
        f.write('F' + str(kn) , each.text)
        kn += 1

    #------------------------Author and mail 2---------------------------------------------------------------------------
    an = n
    for each in authorsArr:
        f.write('H' + str(an) , each)
        an += 1

    mn = n
    for each in mailArr:
        f.write('I' + str(mn) , each)
        mn += 1

    #------------------------Affiliation 2---------------------------------------------------------------------------
    afn = n
    for each in affiArr:
        f.write('J' + str(afn) , each)
        afn += 1

    n += maximum

    print("-----------------------------------------------------------")
    return n

#-------------------------------------------------------------------------------------------------------------------------------
def springer(input):
    for i in range(1,999999):
        try:
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://link.springer.com/search/page/' + str(i) + '?facet-content-type=%22Article%22&query=' + input.replace(" ","+")
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            now = datetime.datetime.now()
            filename = "Springer_" + input.replace(" ","_") + ".xlsx"
            filepath = "springer/csv/" + filename
            workbook = xlsxwriter.Workbook(filepath)
            f = workbook.add_worksheet()
            f.write('A1', 'Keyword : ')
            f.write('B1', input)
            f.write('A2', 'Database : ')
            f.write('B2', 'https://link.springer.com/')
            f.write('A3', 'Date : ')
            f.write('B3', str(now.isoformat()))
            body = page.findAll("li",{"class":"no-access"})
            print(len(body))
            print("---------------------------------------------------------------")
            count = 1
            n = 4
            for each in body:
                link.append(each.h2.a['href'])
                print("link : " + each.h2.a['href'])
            for each in link:
                n = crawInfo(each,f,count,n)
                count += 1
        except Exception as e:
            print("Exception else : " + str(e))
            break
    workbook.close()
