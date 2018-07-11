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
def scienceDirect(input):
    filename = "scienceDirect_" + input.replace(" ","_") + ".csv"
    filepath = "scienceDirect/csv/" + filename
    f = open(filepath,"w",encoding="utf-16")
    now = datetime.datetime.now()
    f.write("Keyword:," + input + "\nDatabase:,https://www.sciencedirect.com\nDate:," + str(now.isoformat()) +"\n\n")
    f.write("S.No,Research Title,Journal Name,Volume and Date of publication,Keywords,Doi number,Author name,Affiliation,Email ID\n")
    # stop = ""
    offset = 0
    count = 1
    for i in range(0,99999):
        try:
            print("enter SD")
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            breaker = False
            print("------------------------------------------------------------------------")
            my_url = 'https://www.sciencedirect.com/search?qs=' + input.replace(" ","%20") + '&show=100&sortBy=relevance&offset=' + str(offset)
            offset += 100
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
            stop = body[0].text
            links = []
            checker = []
            # if(i == 0):
            #     stop = body[len(body)-1].text
            for each in body:
                links.append(each['href'])
                # checker.append(each.text)
            # for each in checker:
            #     print("-------------------------------------------")
            #     print(each + " | " + stop)
            #     print("-------------------------------------------")
            #     if(each == stop and i > 0):
            #         return 0
            for each in links:
                print("try : " + each)
                count = crawInfoScienceDirect(each,f,count)
        except Exception as e:
            print("Exception big : " + str(e))
            break
    f.close()
    print("-------------------------------------")
    print(input)



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
        temp = [{"tag": "span", "className": {"class":"title-text"}}, {"tag":"span", "className":{"class":"reference"}}, {"tag":"h1", "className":{"class":"svTitle"}}]
        checkTitle = False
        for each in temp:
            if(checkTitle):
                break
            title = body.find(each['tag'] , each['className'])
            print("Title : " + replace_all(title.text,re))
            f.write(replace_all(title.text,re) + ",")
            checkTitle = True
    except Exception as e:
        print("Exception title : " + str(e))
        f.write("Cannot get title,")

    #Field of study
    try:
        findFieldStudy = [{"tag": "a", "className": {"class":"publication-title-link"}}, {"tag":"div", "className":{"class":"title"}}]
        done = False
        for ele in findFieldStudy:
            try:
                if(done):
                    break
                title = body.find(ele['tag'],ele['className'])
                print("Journal : " + replace_all(title.text,re))
                f.write(replace_all(title.text,re) + ",")
                done = True
            except:
                continue
        if(done == False):
            print("Field of study is a picture.")
            f.write("Field of study is a picture.,")
    except Exception as e:
        print("Exception journal : " + str(e))
        f.write("Cannot get field of study,")

    #detail
    try:
        detail = body.find("div",{"class":"text-xs"}).text
        print(detail)
        f.write(replace_all(detail,re))
        print("done try 1")
    except Exception as e:
        print("Exception1 : " + str(e))
        f.write("Cannot get detail")

    try:
        vol = body.find("p",{"class":"specIssueTitle"}).text
        print(vol)
        f.write(replace_all(vol,re))
        print("done try 3")
    except Exception as e:
        print("Exception3 : " + str(e))
        f.write("Cannot get volume")

    try:
        detail = body.find("p",{"class":"volIssue"}).text
        print(detail)
        f.write(replace_all(detail,re))
        print("done try 2")
    except Exception as e:
        print("Exception2 : " + str(e))
        f.write("Cannot get detail")

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
            except Exception as e:
                print("except : " + str(e))
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
