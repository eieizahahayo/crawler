import bs4
import requests
import xlsxwriter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re

def crawInfo(input,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")

    #------------initialization----------------------------------------------------------------
    f.write('A' + str(n) , input)
    n += 1
    print(url)
    header = "S.No,Title,Journal name,Date,Doi number,Author name,E-mail,Affiliation\n"
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Title')
    f.write('C' + str(n) , 'Journal name')
    f.write('D' + str(n) , 'Date')
    f.write('E' + str(n) , 'Doi number')
    f.write('F' + str(n) , 'Author name')
    f.write('G' + str(n) , 'E-mail')
    f.write('H' + str(n) , 'Affiliation')
    n += 1
    f.write('A' + str(n) , str(count))


    #------------Title----------------------------------------------------------------
    try:
        title = page.find("span",{"class":"abs_citation_title"})
        print("Title : " + title.text)
        f.write('B' + str(n) , title.text)
    except Exception as e:
        print("Exception title : " + str(e))
        f.write('B' + str(n) , 'Cannot get title')

    #------------Journal and date----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        journalDiv = div.find("div",{"class":"abs_link_metadata"})
        journal = journalDiv.a.text
        date = journalDiv.span.text
        print("Journal : " + journal)
        f.write('C' + str(n) , journal)
        print("Date : " + date)
        f.write('D' + str(n) , date)
    except Exception as e:
        print("Exception journal and date : " + str(e))
        f.write('C' + str(n) , 'Cannot get journal name')
        f.write('D' + str(n) , 'Cannot get date')

    #------------DOI----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        temp = div.find("div",{"class":"metaData"})
        doi = temp.find("a")
        print("DOI : " + doi.text)
        f.write('E' + str(n) , doi.text)
    except Exception as e:
        print("Exception DOI : " + str(e))
        f.write('E' + str(n) , 'Cannot get doi number')

    #------------Authors and email----------------------------------------------------------------
    temp = n
    try:
        div = page.find("div",{"class":"abstract--main-authors-list"})
        all = div.findAll("div",{"class":"inline-block author-block"})
        for each in all:
            author = each.find("h3").text
            print("Author : " + author)
            f.write('F' + str(temp) , author)
            affi = each.find("span",{"class":"author-refine-subtitle"}).text
            print("Affiliation : " + affi)
            f.write('H' + str(temp) , affi)
            try:
                match = re.search("(( )[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", affi)
                if (match):
                    print("Email : " + match.group(0))
                else:
                    print("Cannot get email")
            except Exception as e:
                print("Exception email : " + str(e))
    except Exception as e:
        print("Exception Authors : " + str(e))
    n += 1
    print("---------------------------------------------------------------------------------------")


#-------------------------------------------------------------------------------------------------------------------------------
def pmc(input):
    for i in range(1,999999):
        if(i == 1):
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://europepmc.org/search?query=' + input.replace(" ","+") + '&page=' + str(i)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            now = datetime.datetime.now()
            filename = "europePMC_" + input.replace(" ","_") + ".xlsx"
            filepath = "europePMC/csv/" + filename
            workbook = xlsxwriter.Workbook(filepath)
            f = workbook.add_worksheet()
            f.write('A1', 'Keyword : ')
            f.write('B1', input)
            f.write('A2', 'Database : ')
            f.write('B2', 'https://europepmc.org/')
            f.write('A3', 'Date : ')
            f.write('B3', str(now.isoformat()))
            body = page.findAll("a",{"class":"resultLink linkToAbstract"})
            # print(page.find("article",{"class":"searchResultItem"}).h2.text)
            print("---------------------------------------------------------------")
            count = 1
            n = 4
            print(len(body))
            for each in body:
                link.append("https://europepmc.org" + each['href'].replace(".",""))
                print("link : https://europepmc.org" + each['href'].replace(".",""))
            for each in link:
                n = crawInfo(each,f,count,n)
                count += 1
        # else:
        #     try:
        #         headers = {
        #             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        #         my_url = 'https://link.springer.com/search/page/' + str(i) + '?facet-content-type=%22Article%22&query=' + input.replace(" ","+")
        #         response = requests.get(my_url, headers=headers)
        #         page = soup(response.content, "html5lib")
        #         now = datetime.datetime.now()
        #         body = page.findAll("li",{"class":"no-access"})
        #         print(len(body))
        #         print("---------------------------------------------------------------")
        #         count = 1
        #         n = 4
        #         for each in body:
        #             link.append(each.h2.a['href'])
        #             print("link : " + each.h2.a['href'])
        #         for each in link:
        #             n = crawInfo(each,f,count,n)
        #             count += 1
        #     except Exception as e:
        #         print("Exception else : " + str(e))
        #         break
    workbook.close()
