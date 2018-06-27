import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

def contact(input):
    # div author-info accordion-tabbed__content - div big
    # p author-type - address
    # div bottom-info - contact info
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("div",{"class":"item__body"})


#-------------------------------------------------arXiv------------------------------------------------------------------------------
def wiley(input):
    counter = 1
    filename = "Wiley_" + input.replace(" ","_") + ".csv"
    f = open(filename,"w",encoding="utf-16")
    print("enter Wiley\n----------------------------------------------------------")
    for i in range(0,999999):
        if(i == 0):
            print("Page : " + str(i))
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","+") + '&startPage=&PubType=journal'
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"item__body"})
            now = datetime.datetime.now()
            f.write("Keyword:," + input + "\nDatabase:,https://onlinelibrary.wiley.com/\nDate:," + str(now.isoformat()) +"\n\n")
            header = "S.No,Research Title,Journal Name,Volume,Date,Doi number,Author name,Address,Email\n"
            f.write(header)
            for each in body:
                link = each.h2.span.a['href']
                title = each.h2.text
                info = each.find("div",{"class":"meta__info"})
                date = info.find("span",{"class":"meta__epubDate"}).text
                doi = each.h2.span.a['href']
                re = {"\n":"" , ",":" "}

                #--------------S.No----------------------------------------------
                print("link : " + link)
                f.write(str(counter) + " || " + link + ",")

                #--------------Title----------------------------------------------
                print("Title : " + title)
                f.write(replace_all(title,re) + ",")

                #--------------Book----------------------------------------------
                book = info.find("a",{"class":"meta__serial"}).text
                print("Book : " + book)
                f.write(replace_all(book,re) + ",")
                try:
                    vol = info.find("a",{"class":"meta__volume"}).text
                    print("Volume : " + vol)
                    f.write(replace_all(vol,re) + ",")
                except Exception as e:
                    print("Exception volume : " + str(e))
                    f.write("Cannot get volume,")
                #--------------Date----------------------------------------------
                print("Date : " + date)
                f.write(replace_all(date,re) + ",")

                #--------------Doi----------------------------------------------
                print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                f.write("https://nph.onlinelibrary.wiley.com" + replace_all(doi,re) + ",")

                #--------------Authors----------------------------------------------
                print("Authors : " + info.ul.text)
                if(info.ul.text == ""):
                    f.write("\n")
                else:
                    auts = info.ul.findAll("li")
                    temp = 0
                    for each in auts:
                        if(temp == 0):
                            f.write(replace_all(each.span.a.span.text,re) + "\n")
                            temp += 112
                        else:
                            f.write(",,,,,," + replace_all(each.span.a.span.text,re) + "\n")
                print("-------------------------------------------")
                counter += 1
        else:
            print("Page else : " + str(i))
            try:
                headers = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
                my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","%20") + '&startPage=' + str(i) + '&PubType=journal'
                response = requests.get(my_url, headers=headers)
                page = soup(response.content, "html5lib")
                body = page.findAll("div",{"class":"item__body"})
                print("Body : " + str(body))
                now = datetime.datetime.now()
                stop = True
                for each in body:
                    link = each.h2.span.a['href']
                    title = each.h2.text
                    info = each.find("div",{"class":"meta__info"})
                    date = info.find("span",{"class":"meta__epubDate"}).text
                    doi = each.h2.span.a['href']
                    re = {"\n":"" , ",":" "}

                    #--------------S.No----------------------------------------------
                    print("link : " + link)
                    f.write(str(counter) + " || " + link + ",")

                    #--------------Title----------------------------------------------
                    print("Title : " + title)
                    f.write(replace_all(title,re) + ",")

                    #--------------Book----------------------------------------------
                    book = info.find("a",{"class":"meta__serial"}).text
                    print("Book : " + book)
                    f.write(replace_all(book,re) + ",")
                    try:
                        vol = info.find("a",{"class":"meta__volume"}).text
                        print("Volume : " + vol)
                        f.write(replace_all(vol,re) + ",")
                    except Exception as e:
                        print("Exception volume : " + str(e))
                        f.write("Cannot get volume,")

                    #--------------Date----------------------------------------------
                    print("Date : " + date)
                    f.write(replace_all(date,re) + ",")

                    #--------------Doi----------------------------------------------
                    print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                    f.write("https://nph.onlinelibrary.wiley.com" + replace_all(doi,re) + ",")

                    #--------------Authors----------------------------------------------
                    print("Authors : " + info.ul.text)
                    if(info.ul.text == ""):
                        f.write("\n")
                    else:
                        auts = info.ul.findAll("li")
                        temp = 0
                        for each in auts:
                            if(temp == 0):
                                f.write(replace_all(each.span.a.span.text,re) + "\n")
                                temp += 112
                            else:
                                f.write(",,,,,," + replace_all(each.span.a.span.text,re) + "\n")
                    print("-------------------------------------------")
                    counter += 1
                    stop = False
                if(stop):
                    break
            except Exception as e:
                print("Exception : " + str(e))
                print("Page : " + str(i))
                break
    print("Jimmy")
    f.close()
