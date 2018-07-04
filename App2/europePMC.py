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

    #------------Title----------------------------------------------------------------
    try:
        title = page.find("span",{"class":"abs_citation_title"})
        print("Title : " + title.text)
    except Exception as e:
        print("Exception title : " + str(e))

    #------------Journal and date----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        journalDiv = div.find("div",{"class":"abs_link_metadata"})
        journal = journalDiv.a.text
        date = journalDiv.span.text
        print("Journal : " + journal)
        print("Date : " + date)
    except Exception as e:
        print("Exception journal and date : " + str(e))

    #------------DOI----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        temp = div.find("div",{"class":"metaData"})
        doi = temp.find("a")
        print("DOI : " + doi.text)
    except Exception as e:
        print("Exception DOI : " + str(e))

    #------------Authors and email----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abstract--main-authors-list"})
        all = div.findAll("div",{"class":"inline-block author-block"})
        for each in all:
            print("Author : " + each.find("h3").text)
            affi = each.find("span",{"class":"author-refine-subtitle"}).text
            print("Affiliation : " + affi)
            try:
                match = re.search("(( )[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", affi)
                if match:
                    print("Email : " + match.group(0))
            except Exception as e:
                print("Exception email : " + str(e))
    except Exception as e:
        print("Exception Authors : " + str(e))

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
            workbook = xlsxwriter.Workbook(filename)
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
