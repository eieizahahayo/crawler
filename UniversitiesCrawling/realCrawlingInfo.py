import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import csv

def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text


def crawInfo(str):
    response = requests.get(str, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
    page_soup = soup(response.content, "html5lib")
    body = page_soup.find("body")
    divBody = body.findAll(text=True)
    f.write(str+"\n")
    dic = {"\n":"" , ",":"", "\t":"","\r":""}
    name = []
    email = []
    tele = []
    title = []
    for i in range(0 , len(divBody)):
        if("dr." in divBody[i].lower() or "prof" in divBody[i].lower() or "mr." in divBody[i] or "mrs." in divBody[i] or "ms." in divBody[i]):
            if(len(divBody[i])<100 and not(divBody[i] in name)):
                txt = replace_all(divBody[i],dic)
                name.append(txt)
                print(txt)
        elif("@" in divBody[i] or "mail" in divBody[i].lower()):
            if(len(divBody[i])<100 and not(divBody[i] in email)):
                txt = replace_all(divBody[i],dic)
                email.append(txt)
                print(txt)
        elif("department" in divBody[i].lower() or "faculty" in divBody[i].lower()):
            if(len(divBody[i])<100 and not(divBody[i] in title)):
                txt = replace_all(divBody[i],dic)
                title.append(txt)
                print(txt)
        match = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', divBody[i])
        if match:
            if(len(divBody[i])<100 and not(divBody[i] in tele)):
                txt = replace_all(divBody[i],dic)
                tele.append(txt)
                print(txt)
    str1 = "="
    str2 = "="
    str3 = "="
    title_temp = "="
    newline = "& CHAR(10) &"

    # for i in range(0,len(title)):
    #     if(i == len(title)-1):
    #         tmp = '"'+title[i]+'"'
    #     else:
    #         tmp = '"'+title[i]+'"'+newline
    #     title_temp = title_temp + tmp
    # print(title_temp)
    # f.write(title_temp + "\n")

    f.write("email,name,phone\n")

    # if(email[i] == "email" or email[i] == "Email" or email[i] == "e-mail" or email[i] == "E-mail"):
    #     print("yo")
    #     f.write(",")
    # else:
    f.write(email[0] + ",")

    for i in range(0,len(name)):
        if(i == len(name)-1):
            tmp = '"'+name[i]+'"'
        else:
            tmp = '"'+name[i]+'"'+newline
        str1 = str1 + tmp
    print(str1)
    f.write(str1 + ",")

    for i in range(0,len(tele)):
         if(i == len(tele)-1):
             tmp = '"'+tele[i]+'"'
         else:
             tmp = '"'+tele[i]+'"'+newline
         str3 = str3 + tmp
    print(str3)
    f.write(str3+"\n")

    for i in range(1,len(email)):
        # if(email[i] == "email" or email[i] == "Email" or email[i] == "e-mail" or email[i] == "E-mail"):
        #     print("yo")
        # else:
        f.write(email[i] + "\n")
    f.write("\n")

with open("list.txt", "r") as ins:
    uni = []
    for line in ins:
        uni.append(line)
filename = "contactIndia.csv"
f = open(filename,"w")
for i in range(0,len(uni)):
    try:
        print(uni[i])
        crawInfo(uni[i].replace("\n",""))
        print("Success")
        print("---------------------------------------------------------------------------------------")
    except:
        print(uni[i])
        f.write("\n\n")
        print("The page cannot be reached")
        print("---------------------------------------------------------------------------------------")
f.close()
