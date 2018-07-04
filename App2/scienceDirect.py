import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text


#-----------------------------------------------ScienceDirect--------------------------------------------------------------------------------
def scienceDirect(input,aut):
    for i in range(0,99999):
        try:
            print("enter SD")
            count = 1
            stop = ""
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            if(not aut):
                print("enter no aut")
                print("------------------------------------------------------------------------")
                my_url = 'https://www.sciencedirect.com/search?qs=' + input.replace(" ","%20") + '&show=100&sortBy=relevance&offset=' + str(i)
                response = requests.get(my_url, headers=headers)
                page = soup(response.content, "html5lib")
                body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
                if(i == 0):
                    stop = body[0].text
                links = []
                checker = []
                filename = "scienceDirect_" + input.replace(" ","_") + ".csv"
                f = open(filename,"w",encoding="utf-16")
                now = datetime.datetime.now()
                f.write("Keyword:," + input + "\nDatabase:,https://www.sciencedirect.com\nDate:," + str(now.isoformat()) +"\n\n")
                f.write("S.No,Research Title,Journal Name,Volume and Date of publication,Keywords,Doi number,Author name,Affiliation,Email ID\n")
                for each in body:
                    links.append(each['href'])
                    checker.append(each.text)
                for each in checker:
                    if(each == stop):
                        break
                for each in links:
                    print("try : " + each)
                    count = crawInfoScienceDirect(each,f,count)
            else:
                print("enter aut")
                print("------------------------------------------------------------------------")
                my_url = 'https://www.sciencedirect.com/search?qs=' + input.replace(" ","%20") + '&authors=' + aut.replace(" ","%20") +  '&show=100&sortBy=relevance&offset=' + str(i)
                response = requests.get(my_url, headers=headers)
                page = soup(response.content, "html5lib")
                body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
                if(i == 0):
                    stop = body[0].text
                links = []
                checker = []
                filename = "scienceDirect_" + input.replace(" ","_") + ".csv"
                f = open(filename,"w",encoding="utf-16")
                now = datetime.datetime.now()
                f.write("Keyword:," + input + "\nDatabase:,https://www.sciencedirect.com\nDate:," + str(now.isoformat()) +"\n\n")
                f.write("S.No,Research Title,Journal Name,Volume and Date of publication,Keywords,Doi number,Author name,Affiliation,Email ID\n")
                for each in body:
                    links.append(each['href'])
                    checker.append(each.text)
                for each in checker:
                    if(each == stop):
                        break
                for each in links:
                    print("try : " + each)
                    count = crawInfoScienceDirect(each,f,count)
        except Exception as e:
            print("Exception big : " + str(e))
            break
        f.close()



def crawInfoScienceDirect(input,f,count):
    print("------------------------------------------------------------------------")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    url = "https://www.sciencedirect.com"+input
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":"" , ",":" "}
    print(url)
    f.write(str(count) + " || " + url + ",")

    #Title
    try:
        title = body.find("span",{"class":"title-text"})
        print("Title : " + replace_all(title.text,re))
        f.write(replace_all(title.text,re) + ",")
    except:
        title = body.find("h1",{"class":"svTitle"})
        print("Title : " + replace_all(title.text,re))
        f.write(replace_all(title.text,re) + ",")

    #Field of study
    findFieldStudy = [{"tag": "a", "className": {"class":"publication-title-link"}}, {"tag":"div", "className":{"class":"title"}}]
    done = False
    for ele in findFieldStudy:
        try:
            if(done):
                break
            title = body.find(ele['tag'],ele['className'])
            print("Title : " + replace_all(title.text,re))
            f.write(replace_all(title.text,re) + ",")
            done = True
        except:
            continue
    if(done == False):
        print("Field of study is a picture.")
        f.write("Field of study is a picture.,")

    #detail
    try:
        detail = body.find("div",{"class":"text-xs"}).text
        print(detail)
        f.write(replace_all(detail,re))
        print("done try 1")
    except Exception as e:
        print("Exception1 : " + str(e))

    try:
        vol = body.find("p",{"class":"specIssueTitle"}).text
        print(vol)
        f.write(replace_all(vol,re))
        print("done try 3")
    except Exception as e:
        print("Exception3 : " + str(e))

    try:
        detail = body.find("p",{"class":"volIssue"}).text
        print(detail)
        f.write(replace_all(detail,re))
        print("done try 2")
    except Exception as e:
        print("Exception2 : " + str(e))

    f.write(",")

    #key words
    findArr = [{"tag":"div","className":{"class":"keywords-section"}},{"tag":"ul","className":{"class":"keyword"}},{"tag":"div","className":{"class":"svKeywords"}}]
    alreadyDone = False
    for ele in findArr:
        try:
            if(alreadyDone):
                break
            kw = body.find(ele['tag'], ele['className'])
            temp2 = kw.findAll("span")
            alreadyDone = True
            for i in range(len(temp2)):
                if(i == 0):
                    f.write(temp2[i].text + ",")
                    #doi number --------------------------------------------------
                    doiArr = [{"class":"doi"},{"class":"S_C_ddDoi"}]
                    done = False
                    for ele in doiArr:
                        try:
                            if(done):
                                break
                            doi = body.find("a",ele)
                            print(doi.text)
                            f.write(doi.text+"\n")
                            done = True
                        except:
                            continue
                    if(done == False):
                        print("Cannot get DOI")
                        f.write("Cannot get DOI\n")
                    #-------------------------------------------------------------
                else:
                    f.write(",,,," + temp2[i].text + "\n")
        except Exception as e:
            continue
    if(alreadyDone == False):
        print("no keywords")
        f.write("no keywords,")
        #doi number --------------------------------------------------
        doiArr = [{"class":"doi"},{"class":"S_C_ddDoi"}]
        done = False
        for ele in doiArr:
            try:
                if(done):
                    break
                doi = body.find("a",ele)
                print(doi.text)
                f.write(doi.text+"\n")
                done = True
            except:
                print("except : " + str(i))
                continue
        if(done == False):
            print("Cannot get DOI")
            f.write("Cannot get DOI\n")
        #-------------------------------------------------------------
    print("-----------------------------------------------------------------")
    f.write("\n\n")
    count += 1
    x = count
    return x
