import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def isMatchCondition(phrase, conditions):
    for ele in conditions:
        if(ele in phrase):
            return True
    return False

def contactCrawling(url,country):
    my_url = url
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html5lib")
    body = page_soup.find("body")
    divBody = body.findAll(text=True)
    alla = body.findAll("a")
    languages = {
    #South east asia
    "Thai":["โทร" , "ติดต่อ" , "ที่อยู่" , "สอบถาม","อีเมล","เลขที่"],
    "Malay":["hubungi","e-mel","emel","alamat"],
    "Kmher":["ទូរស័ព្ទ","ទំនាក់ទំនង","អ៊ីមែល","អាសយដ្ឋាន"],
    "Indo":["kontak"],
    "Lao":["ທີ່ຢູ່","ໂທ","ອີເມວ"],
    "Philipin":["alamat"],
    "Vietnam":["địa chỉ nhà","tiếp xúc"]
    }
    for i in range(0,len(divBody)-1):
        if("Dr" in divBody[i] or "@" in divBody[i] or "tel" in divBody[i] or "Tel" in divBody[i] or "TEL" in divBody[i] or "fax" in divBody[i].lower() or "email" in divBody[i].lower() or "e-mail" in divBody[i].lower() or "address" in divBody[i] or "contact" in divBody[i]):
            if(not("function" in divBody[i]) and not("</" in divBody[i])):
                if(not("function" in divBody[i]) and not("</" in divBody[i])):
                    if(not("function" in divBody[i]) and not("</" in divBody[i-2])):
                        print(divBody[i-2])
                        f.write("\"" + divBody[i-2] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i-1])):
                        print(divBody[i-1])
                        f.write("\"" + divBody[i-1] + "\"")
                    print(divBody[i])
                    f.write("\"" + divBody[i] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i+1])):
                        print(divBody[i+1])
                        f.write("\"" + divBody[i+1] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i+2])):
                        print(divBody[i+2])
                        f.write("\"" + divBody[i+2] + "\"")
                    print("---------------------------------------------------------")

        if(isMatchCondition(divBody[i], languages['Thai'])):
            if(not("function" in divBody[i]) and not("</" in divBody[i])):
                if(not("function" in divBody[i]) and not("</" in divBody[i])):
                    if(not("function" in divBody[i]) and not("</" in divBody[i-2])):
                        print(divBody[i-2])
                        f.write("\"" + divBody[i-2] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i-1])):
                        print(divBody[i-1])
                        f.write("\"" + divBody[i-1] + "\"")
                    print(divBody[i])
                    f.write("\"" + divBody[i] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i+1])):
                        print(divBody[i+1])
                        f.write("\"" + divBody[i+1] + "\"")
                    if(not("function" in divBody[i]) and not("</" in divBody[i+2])):
                        print(divBody[i+2])
                        f.write("\"" + divBody[i+2] + "\"")
                    print("---------------------------------------------------------")

    for a in alla:
        if("contact" in a.text.lower()):
            f.write(",")
            print("Link : " + a['href'])
            f.write(a['href'] + "\n")


my_url = 'http://www.jau.in/coa/index.php/department'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html5lib")
body = page_soup.find("body")
divBody = body.findAll(text=True)
alla = body.findAll("a")
filename = "contact.csv"
f = open(filename,"w",encoding="utf-16")
contactCrawling(my_url,"Thai")
f.close()
