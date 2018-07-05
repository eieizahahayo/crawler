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

def contact(input,f,n):
    print("enter contact")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("div",{"class":"accordion-tabbed__tab-mobile accordion__closed"})
    print(len(body))
    for i in range(len(body) // 2):
        email = []
        #--------------Authors----------------------------------------------
        print("Author : " + body[i].a.span.text)
        f.write('G' + str(n) , body[i].a.span.text)
        try:
            add = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
            try:
                allP = add.findAll("p")
                for each in allP:
                    print("Address : " + each.text)
                    f.write('I' + str(n) , each.text)
                    match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", each.text)
                    if(match):
                        email.append(match.group(0))
                        print("Found email in author : " + match.group(0))
            except Exception as e:
                print("Cannot get address")
                f.write('I' + str(n) , "Cannot get affiliation")
        except Exception as e:
            print("Exception address : " + str(e))
            f.write('I' + str(n) , 'Cannot get affiliation')

        #--------------email----------------------------------------------
        try:
            info = body[i].find("div",{"class":"bottom-info"})
            match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", info.text)
            if match:
                print("Email : " + match.group(0))
                email.append(match.group(0))
            else:
                print("Email not match :" + info.text)
                print("Email not match")
                email.append("Cannot get email")
        except Exception as e:
            print("Exception email : " + str(e))
            email.append("Cannot get email")

        ec = n
        if(len(email) == 0):
            f.write('H' + str(n) , 'Cannot get email')
        else:
            tempmail = set(email)
            for each in tempmail:
                f.write('H' + str(ec) , each)
                ec += 1
        n += ec
        print("-----------------------------------------")
        return n

#-------------------------------------------------arXiv------------------------------------------------------------------------------
def wiley(input):
    filename = "Wiley_" + input.replace(" ","_") + ".xlsx"
    filepath = "wiley/csv/" + filename
    now = datetime.datetime.now()
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://onlinelibrary.wiley.com/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    for i in range(0,999999):
        count = 1
        n = 4
        if(i == 0):
            print("Page : " + str(i))
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","+") + '&startPage=&PubType=journal'
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"item__body"})
            for each in body:
                link = each.h2.span.a['href']
                title = each.h2.text
                info = each.find("div",{"class":"meta__info"})
                date = info.find("span",{"class":"meta__epubDate"}).text
                doi = each.h2.span.a['href']

                #-------------------Initialization--------------------------------------------------------
                f.write('A' + str(n) , "https://nph.onlinelibrary.wiley.com" + link)
                print("link : " + link)
                n += 1
                header = "S.No,Title,Journal name,Volume,Date,Keywords,Doi number,Author name,E-mail,Affiliation\n"
                f.write('A' + str(n) , 'S.No')
                f.write('B' + str(n) , 'Title')
                f.write('C' + str(n) , 'Journal name')
                f.write('D' + str(n) , 'Volume')
                f.write('E' + str(n) , 'Date')
                f.write('F' + str(n) , 'Doi number')
                f.write('G' + str(n) , 'Author name')
                f.write('H' + str(n) , 'E-mail')
                f.write('I' + str(n) , 'Affiliation')
                n += 1
                f.write('A' + str(n) , str(count))

                #--------------Title----------------------------------------------
                print("Title : " + title)
                f.write('B' + str(n) , title)

                #--------------Journal----------------------------------------------
                journal = info.find("a",{"class":"meta__serial"}).text
                print("Journal : " + journal)
                f.write('C' + str(n) , journal)
                try:
                    vol = info.find("a",{"class":"meta__volume"}).text
                    print("Volume : " + vol)
                    f.write('D' + str(n) , vol)
                except Exception as e:
                    print("Exception volume : " + str(e))
                    f.write('D' + str(n) , 'Cannot get volume')
                #--------------Date----------------------------------------------
                print("Date : " + date)
                f.write('E' + str(n) , date)

                #--------------Doi----------------------------------------------
                print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                f.write('F' + str(n) , 'https://nph.onlinelibrary.wiley.com' + doi)

                #--------------Authors and email----------------------------------------------
                parse = "https://nph.onlinelibrary.wiley.com" + doi
                n = contact(parse,f,n)
                print("-------------------------------------------")
                count += 1
        else:
            print("Page else : " + str(i))
            try:
                headers = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
                my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","%20") + '&startPage=' + str(i) + '&PubType=journal'
                response = requests.get(my_url, headers=headers)
                page = soup(response.content, "html5lib")
                body = page.findAll("div",{"class":"item__body"})
                for each in body:
                    link = each.h2.span.a['href']
                    title = each.h2.text
                    info = each.find("div",{"class":"meta__info"})
                    date = info.find("span",{"class":"meta__epubDate"}).text
                    doi = each.h2.span.a['href']

                    #-------------------Initialization--------------------------------------------------------
                    f.write('A' + str(n) , "https://nph.onlinelibrary.wiley.com" + link)
                    print("link : " + link)
                    n += 1
                    header = "S.No,Title,Journal name,Volume,Date,Keywords,Doi number,Author name,E-mail,Affiliation\n"
                    f.write('A' + str(n) , 'S.No')
                    f.write('B' + str(n) , 'Title')
                    f.write('C' + str(n) , 'Journal name')
                    f.write('D' + str(n) , 'Volume')
                    f.write('E' + str(n) , 'Date')
                    f.write('F' + str(n) , 'Doi number')
                    f.write('G' + str(n) , 'Author name')
                    f.write('H' + str(n) , 'E-mail')
                    f.write('I' + str(n) , 'Affiliation')
                    n += 1
                    f.write('A' + str(n) , str(count))

                    #--------------Title----------------------------------------------
                    print("Title : " + title)
                    f.write('B' + str(n) , title)

                    #--------------Journal----------------------------------------------
                    journal = info.find("a",{"class":"meta__serial"}).text
                    print("Journal : " + journal)
                    f.write('C' + str(n) , journal)
                    try:
                        vol = info.find("a",{"class":"meta__volume"}).text
                        print("Volume : " + vol)
                        f.write('D' + str(n) , vol)
                    except Exception as e:
                        print("Exception volume : " + str(e))
                        f.write('D' + str(n) , 'Cannot get volume')
                    #--------------Date----------------------------------------------
                    print("Date : " + date)
                    f.write('E' + str(n) , date)

                    #--------------Doi----------------------------------------------
                    print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                    f.write('F' + str(n) , 'https://nph.onlinelibrary.wiley.com' + doi)

                    #--------------Authors and email----------------------------------------------
                    parse = "https://nph.onlinelibrary.wiley.com" + doi
                    n = contact(parse,f,n)
                    print("-------------------------------------------")
                    count += 1
                    n += 1
                    stop = False
                if(stop):
                    break
            except Exception as e:
                print("Exception : " + str(e))
                print("Page : " + str(i))
                break
    print("Jimmy")
    f.close()
