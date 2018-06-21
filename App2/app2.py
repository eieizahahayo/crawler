import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

#-----------------------------------------------ScienceDirect--------------------------------------------------------------------------------
def scienceDirect(input,aut):
    print("enter SD")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    if(not aut):
        print("enter no aut")
        print("------------------------------------------------------------------------")
        my_url = 'https://www.sciencedirect.com/search?qs=' + input.replace(" ","%20") + '&show=25&sortBy=relevance'
        response = requests.get(my_url, headers=headers)
        page = soup(response.content, "html5lib")
        body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
        links = []
        filename = "scienceDirect" + input + ".csv"
        f = open(filename,"w",encoding="utf-16")
        header = "Title,Field of study,keywords,DOI number,Auth detail\n"
        f.write(header)
        for each in body:
            links.append(each['href'])
        for each in links:
            print("try : " + each)
            crawInfoScienceDirect(each,f)
        f.close()
    else:
        print("enter aut")
        print("------------------------------------------------------------------------")
        my_url = "https://www.sciencedirect.com/search?qs=" + input.replace(" ","%20") + "&authors=" + aut.replace(" ","%20") + "&show=25&sortBy=relevance"
        response = requests.get(my_url, headers=headers)
        page = soup(response.content, "html5lib")
        body = page.findAll("a",{"class":"result-list-title-link u-font-serif text-s"})
        links = []
        filename = "scienceDirect" + input + "By"+ aut + ".csv"
        f = open(filename,"w",encoding="utf-16")
        header = "Title,Field of study,keywords,DOI number,Auth detail\n"
        f.write(header)
        for each in body:
            links.append(each['href'])
        for each in links:
            print("try : " + each)
            crawInfoScienceDirect(each,f)
        f.close()



def crawInfoScienceDirect(input,f):
    print("------------------------------------------------------------------------")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    url = "https://www.sciencedirect.com"+input
    response = requests.get(url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":"" , ",":" "}
    print(url)
    f.write(url+"\n")

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
            print("Keywords : ")
            kws = "="
            newline = "& CHAR(10) &"
            for i in range(0,len(temp2)):
                if(i == len(temp2)-1):
                    tmp = '"' + temp2[i].text + '"'
                else:
                    tmp = '"' + temp2[i].text + '"' + newline
                kws = kws + tmp
            print("kws : " + kws)
            f.write(kws+",")
        except Exception as e:
            continue
    if(alreadyDone == False):
        print("no keywords")
        f.write("no keywords")

    #doi number
    try:
        doi = body.find("a",{"class":"doi"})
        print(doi.text)
        f.write(doi.text+",")
    except:
        doi = body.find("a",{"id":"ddDoi"})
        print(doi.text)
        f.write(doi.text+",")

    # #Authors
    # autG = body.findAll("div",{"class":"WorkspaceAuthor"})
    # eachAut = autG.findAll("a",{"class":"author size-m workspace-trigger"})
    # for i in range(0,len(eachAut)):
    #


    print("-----------------------------------------------------------------")
    f.write("\n\n")





#-------------------------------------------------arXiv------------------------------------------------------------------------------
def arXiv(input):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    print("enter arXiv")
    my_url = 'https://arxiv.org/search/?query=' + input.replace(" ","+") + '&searchtype=all&source=header'
    response = requests.get(my_url, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("a")
    links = []
    filename = "arxiv" + input + ".csv"
    f = open(filename,"w",encoding="utf-16")
    header = "Title,Subject,date,by\n"
    f.write(header)
    for a in body:
        if("arXiv:" in a.text):
            links.append(a['href'])
    for each in links:
        print("try : " + each)
        crawInfoArxiv(each,f)
    f.close()


def crawInfoArxiv(str,f):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(str, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.find("body")
    re = {"\n":" " , ",":" ","Title:":" ","Authors:":" "}

    title = body.find("h1",{"class":"title mathjax"})
    print(replace_all(title.text,re))
    f.write(replace_all(title.text,re) + ",")

    subj = body.find("span",{"class":"primary-subject"})
    print(replace_all(subj.text,re))
    f.write(replace_all(subj.text,re) + ",")

    date = body.find("div",{"class":"dateline"})
    print(replace_all(date.text,re))
    f.write(replace_all(date.text,re) + ",")

    by = body.find("div",{"class":"authors"})
    print(replace_all(by.text,re))
    f.write(replace_all(by.text,re) + "\n")

    print("-------------------------------------------------------------------------------")

#------------------------------------------Main-------------------------------------------------------------------------------------
print('[1] : arXiv\n[2] : ScienceDirect')
choice = input("Enter your choice : ")
if(choice == 1):
    key = input('Enter the keyword : ')
    arXiv(key)
else:
    key = input('Enter the keyword : ')
    aut = input('Enter the author : ')
    scienceDirect(key,aut)
