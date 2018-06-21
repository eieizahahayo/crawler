import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#--------------------------------------check if function------------------------------------------------------
def isMatchCondition(phrase, conditions):
    for ele in conditions:
        if(ele in phrase):
            return True
    return False

#--------------------------------------contact crawling------------------------------------------------------
def contactCrawling(url,country):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    my_url = url
    response = requests.get(url, headers=headers, timeout=5)
    page_soup = soup(page_html, "html5lib")
    body = page_soup.find("body")
    divBody = body.findAll(text=True)
    alla = body.findAll("a")
    languages = { #dynamic
    #South east asia
    "Thai":["โทร" , "ติดต่อ" , "ที่อยู่" , "สอบถาม","อีเมล","เลขที่"],
    "Malay":["hubungi","e-mel","emel","alamat"],
    "Kmher":["ទូរស័ព្ទ","ទំនាក់ទំនង","អ៊ីមែល","អាសយដ្ឋាន"],
    "Indo":["kontak"],
    "Lao":["ທີ່ຢູ່","ໂທ","ອີເມວ"],
    "Philipin":["alamat"],
    "Vietnam":["địa chỉ nhà","tiếp xúc"],
    "SouthEastAsia" : ["โทร" , "ติดต่อ" , "ที่อยู่" , "สอบถาม","อีเมล","เลขที่","hubungi","e-mel","emel","alamat","ទូរស័ព្ទ","ទំនាក់ទំនង","អ៊ីមែល","អាសយដ្ឋាន","kontak","ທີ່ຢູ່","ໂທ","ອີເມວ","alamat","địa chỉ nhà","tiếp xúc"]
    }
    for i in range(0,len(divBody)-1):
        if("tel" in divBody[i] or "Tel" in divBody[i] or "TEL" in divBody[i] or "fax" in divBody[i].lower() or "email" in divBody[i].lower() or "e-mail" in divBody[i].lower() or "address" in divBody[i] or "contact" in divBody[i]):
            if(not("function" in divBody[i]) and not("</" in divBody[i]) and not("[{" in divBody[i]) and len(divBody[i]) < 150):
                if(not("function" in divBody[i]) and not("</" in divBody[i-2]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i-2] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i-1]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i-1] + "\"")
                f.write("\"" + divBody[i] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i+1]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i+1] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i+2]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i+2] + "\"")

        if(isMatchCondition(divBody[i], languages['SouthEastAsia'])): #Dynamic
            if(not("function" in divBody[i]) and not("</" in divBody[i]) and not("[{" in divBody[i]) and len(divBody[i]) < 150):
                if(not("function" in divBody[i]) and not("</" in divBody[i-2]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i-2] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i-1]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i-1] + "\"")
                f.write("\"" + divBody[i] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i+1]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i+1] + "\"")
                if(not("function" in divBody[i]) and not("</" in divBody[i+2]) and len(divBody[i-2]) < 100):
                    f.write("\"" + divBody[i+2] + "\"")
        f.write("\n")

    for a in alla:
        if("contact" in a.text.lower()):
            f.wrie(",")
            print("Link : " + a['href'])
            f.write(a['href'] + "\n")
#--------------------------------------replace words------------------------------------------------------
def replace_all(text, wordDict):
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text
#--------------------------------------crawling wikipedia------------------------------------------------------
def crawWiki(str):
    my_url = 'https://en.wikipedia.org/wiki/'+str
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    f.write(my_url+",")

#--------------------------------------check next page------------------------------------------------------
def check(url , str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    my_url = url + '?page=' + str
    response = requests.get(my_url, headers=headers, timeout=5)
    page = soup(response.content, "html5lib")
    table = page.find("tbody")
    containers = table.findAll("tr")
    x = containers[0].findAll('td') #Checker [2]
    for i in range(0, len(containers)):
        temp = containers[i].findAll('td')
    return x[2].text

#--------------------------------------navigate next age------------------------------------------------------
def nextPage(url , str):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    my_url = url + '?page=' + str
    response = requests.get(my_url, headers=headers, timeout=5)
    page = soup(response.content, "html5lib")
    table = page.find("tbody")
    containers = table.findAll("tr")
    re = {"\n":" " , ",":" "}
    x = containers[0].findAll('td') #Checker [2]
    for i in range(0, len(containers)):
        temp = containers[i].findAll('td')
        txt = replace_all(temp[2].text,re)
        f.write(txt + "," + temp[2].a['href'] + ",")
        try:
            crawWiki(temp[2].text)
        except:
            f.write("Wiki page not found,")
        try:
            contactCrawling(temp[2].a['href'],"NorthAmerica") #dynamic
        except:
            f.write("Website cannot be reached by code\n")
        print(temp[2].text)
    return x[2].text

#--------------------------------------Main------------------------------------------------------
# user select:
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
regions = ["Asia","Asia_Pacifico/South%20East%20Asia","Asia_Pacifico/South%20Asia","East_Asia","Asia_Pacifico","Asia_Pacifico/Middle_East"]
countries = ["Asia/Afghanistan" , "Asia/East%20Timor" , "Asia/Jordan" , "Asia/Maldives%20","Asia/Republic%20Of%20Korea","Asia/Thailand",
"Asia/Bahrain%20","Asia/Hong%20Kong","Asia/Kazakstan","Asia/Mongolia%20","Asia/Saudi%20Arabia%20","Asia/Turkey",
"Asia/Bangladesh%20","Asia/India","Asia/Kuwait","Asia/Nepal%20","Asia/Singapore%20","Asia/Turkmenistan%20",
]
url = "http://www.webometrics.info/en/" + regions[1] #dynamic
response = requests.get(url, headers=headers, timeout=5)
page = soup(response.content, "html5lib")
table = page.find("tbody")
containers = table.findAll("tr")
filename = "testFinal.csv"     # + "Universities.csv" #dynamic
f = open(filename,"w")
headers = "Name,Official-Website,Wikipedia,Contact\n"
f.write(headers)
re = {"\n":" " , ",":" "}


for i in range(0, len(containers)):
    temp = containers[i].findAll('td')
    txt = replace_all(temp[2].text,re)
    f.write(txt + "," + temp[2].a['href']+",")
    try:
        crawWiki(temp[2].text)
    except:
        f.write("Wiki page not found,")
    try:
        contactCrawling(temp[2].a['href'],"NorthAmerica") #dynamic
    except:
        f.write("Website cannot be reached by code\n")
    print(temp[2].text)

for i in range(1,150):
    try:
        x = nextPage(url,str(i))
        y = check(url,str(i+1))
        if(x == y):
            break
    except:
        f.close()
f.close()
