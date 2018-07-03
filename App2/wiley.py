import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

def contact(input,f):
    # div author-info accordion-tabbed__content - div big
    # div -> a -> span = name
    # p อันที่ 2 no class author-type - address
    # div bottom-info - contact info
    print("enter contact")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("div",{"class":"accordion-tabbed__tab-mobile accordion__closed"})
    print(len(body))
    re = {"\n":"" , ",":" " , ";":" "}
    for i in range(len(body) // 2):
        if(i == 0):
            print("Author : " + body[i].a.span.text)
            f.write(replace_all(body[i].a.span.text,re) + ",")
            # div = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
            # print("Infomation : " + div.text)
            # try:
            #     # email = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     # print("Email : " + str(email))
            #
            #     match = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     email = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     print("match : " + str(match))
            #     print("match2 : " + str(email))
            #     if match:
            #         print("Email : " + str(match))
            # except Exception as e:
            #     print("Exception email : " + str(e))

            try:
                add = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
                try:
                    allP = add.findAll("p")
                    for each in allP:
                        print("Address : " + each.text)
                        f.write(replace_all(each.text,re))
                except Exception as e:
                    print("Address : " + add.p.text )
                    f.write(replace_all(add.p.text,re))
                f.write(",")
            except Exception as e:
                print("Exception address : " + str(e))
                f.write("Cannot get address,")

            try:
                info = body[i].find("div",{"class":"bottom-info"})
                print("Contact : " + info.text)
                f.write(replace_all(info.text,re) + "\n")
            except Exception as e:
                print("Exception contact : " + str(e))
                f.write("Cannot get email\n")
        else:
            f.write(",,,,,,")
            print("Author : " + body[i].a.span.text)
            f.write(replace_all(body[i].a.span.text,re) + ",")
            # div = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
            # print("Infomation : " + div.text)
            # try:
            #     # email = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     # print("Email : " + str(email))
            #
            #     match = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     email = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",div.text)
            #     print("match : " + str(match))
            #     print("match2 : " + str(email))
            #     if match:
            #         print("Email : " + str(match))
            # except Exception as e:
            #     print("Exception email : " + str(e))

            try:
                add = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
                try:
                    allP = add.findAll("p")
                    for each in allP:
                        print("Address : " + each.text)
                        f.write(replace_all(each.text,re))
                except Exception as e:
                    print("Address : " + add.p.text )
                    f.write(replace_all(add.p.text,re))
                f.write(",")
            except Exception as e:
                print("Exception address : " + str(e))
                f.write("Cannot get address,")

            try:
                info = body[i].find("div",{"class":"bottom-info"})
                print("Contact : " + info.text)
                f.write(replace_all(info.text,re) + "\n")
            except Exception as e:
                print("Exception contact : " + str(e))
                f.write("Cannot get email\n")



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
                f.write(str(counter) + " || https://nph.onlinelibrary.wiley.com" + link + ",")

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
                # print("Authors : " + info.ul.text)
                # if(info.ul.text == ""):
                #     f.write("\n")
                # else:
                #     auts = info.ul.findAll("li")
                #     temp = 0
                #     for each in auts:
                #         if(temp == 0):
                #             f.write(replace_all(each.span.a.span.text,re) + "\n")
                #             temp += 112
                #         else:
                #             f.write(",,,,,," + replace_all(each.span.a.span.text,re) + "\n")

                parse = "https://nph.onlinelibrary.wiley.com" + doi
                contact(parse,f)

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
                    parse = "https://nph.onlinelibrary.wiley.com" + doi
                    contact(parse,f)
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
