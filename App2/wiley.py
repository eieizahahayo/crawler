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
def wiley(input):
    counter = 1
    filename = "Wiley " + input + ".csv"
    f = open(filename,"w",encoding="utf-16")
    print("enter Wiley\n----------------------------------------------------------")
    for i in range(0,999999):
        if(i == 0):
            print("Page : " + str(i))
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","+")
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"item__body"})
            now = datetime.datetime.now()
            f.write("Keyword:," + input + "\nDatabase:,https://onlinelibrary.wiley.com/\nDate:," + str(now.isoformat()) +"\n\n")
            header = "S.No,Research Title,Journal Name,Volume,Date,Doi number,Authors\n"
            f.write(header)
            for each in body:
                link = each.h2.span.a['href']
                title = each.h2.text
                info = each.find("div",{"class":"meta__info"})
                date = info.find("span",{"class":"meta__epubDate"}).text
                doi = each.h2.span.a['href']
                re = {"\n":"" , ",":" "}

                print("link : " + link)
                f.write(str(counter) + " || " + link + ",")
                print("Title : " + title)
                f.write(replace_all(title,re) + ",")
                arr = [{"class":"meta__serial meta__book"},{"class":"meta__serial"}]
                done = False
                for each in arr:
                    try:
                        if(done):
                            break
                        book = info.find("a",each).text
                        print("Book : " + book)
                        f.write(replace_all(book,re) + ",,")
                        done = True
                    except:
                        continue
                if(done == False):
                    book = info.find("a",{"class":"meta__serial"}).text
                    vol = info.find("a",{"class":"meta__volume"}).text
                    print("Book : " + book)
                    f.write(replace_all(book,re) + ",")
                    print("Volume : " + vol)
                    f.write(replace_all(vol,re) + ",")
                print("Date : " + date)
                f.write(replace_all(date,re) + ",")
                print("Doi : " + doi)
                f.write(replace_all(doi,re) + ",")
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
                my_url = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","%20") + '&startPage=' + str(i)
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

                    print("link : " + link)
                    f.write(str(counter) + " || " + link + ",")
                    print("Title : " + title)
                    f.write(replace_all(title,re) + ",")
                    arr = [{"class":"meta__serial meta__book"},{"class":"meta__serial"}]
                    done = False
                    for each in arr:
                        try:
                            if(done == True):
                                break
                            book = info.find("a",each).text
                            print("Book : " + book)
                            f.write(replace_all(book,re) + ",,")
                            done = True
                        except:
                            continue
                    if(done == False):
                        book = info.find("a",{"class":"meta__serial"}).text
                        vol = info.find("a",{"class":"meta__volume"}).text
                        print("Book : " + book)
                        f.write(replace_all(book,re) + ",")
                        print("Volume : " + vol)
                        f.write(replace_all(vol,re) + ",")
                    print("Date : " + date)
                    f.write(replace_all(date,re) + ",")
                    print("Doi : " + doi)
                    f.write(replace_all(doi,re) + ",")
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
