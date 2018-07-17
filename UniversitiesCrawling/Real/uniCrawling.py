import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import xlsxwriter
from time import sleep
def initialization(n,f):
    print("Enter initialization")
    f.write('A' + str(n) , 'S.no')
    f.write('B' + str(n) , 'Website')
    f.write('C' + str(n) , 'University/faculty')
    f.write('D' + str(n) , 'Email')
    f.write('E' + str(n) , 'Name')
    f.write('F' + str(n) , 'Telephone number')

def definitionWrite(input,n,f):
    #------------------------University----------------------------------------------------------------
    print("enter definitionWrite")
    f.write('C' + str(n) , input)

def crawInfo(url,f,n,count):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}, timeout = 60)
    page_soup = soup(response.content, "html5lib")
    body = page_soup.find("body")
    divBody = body.findAll(text=True)
    name = []
    email = []
    tele = []
    #------------------------Initialization----------------------------------------------------------------
    f.write('A' + str(n) , str(count))
    f.write('B' + str(n) , url)

    for i in range(0 , len(divBody)):
        match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", divBody[i])
        if("dr." in divBody[i].lower() or "prof" in divBody[i].lower() or "mr." in divBody[i] or "mrs." in divBody[i] or "ms." in divBody[i]):
            if(len(divBody[i])<100 and not(divBody[i] in name)):
                name.append(divBody[i])
        elif(match):
            email.append(match.group(0).replace(" ",""))
        match = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', divBody[i])
        if match:
            if(len(divBody[i])<100 and not(divBody[i] in tele)):
                tele.append(divBody[i])
    #------------------------Information----------------------------------------------------------------
    et = n
    nt = n
    tt = n
    maximum = 0
    try:
        if(len(email) == 0):
            f.write('D' + str(et), 'Email is protected')
        else:
            for each in set(email):
                f.write('D' + str(et) , each)
                et += 1
        print("Email : " + each )
    except Exception as e:
        print("Email exception : " + str(e))

    print("--------------------------------------------------------------")
    try:
        for each in set(name):
            f.write('E' + str(nt) , each)
            nt += 1
            print("Name : " + each)
    except Exception as e:
        print("Name exception : " + str(e))

    print("--------------------------------------------------------------")
    try:
        for each in set(tele):
            f.write('F' + str(tt) , each)
            tt += 1
            print("tele : " + each )
    except Exception as e:
        print("Tele exception : " + str(e))
    print("--------------------------------------------------------------")
    list = [et,nt,tt]
    n += (max(list) - n)
    return n

#--------------------------main-----------------------------------------------------------------------
def crawling(file,name):
    sleep(5)
    with open( file , "r") as ins:
        uni = []
        for line in ins:
            uni.append(line)
    filename = "contact_" + name + ".xlsx"
    filepath = "xlsx/" + filename
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    n = 1
    count = 1
    f.write('A' + str(n) , uni[0])
    n += 1
    initialization(n,f)
    n += 1
    for i in range(1,len(uni)):
        try:
            if(i%2 == 1):
                print("Enter if : " + uni[i])
                definitionWrite(uni[i],n,f)
            elif(i%2 == 0):
                print("Enter else : " + uni[i])
                n = crawInfo(uni[i].replace("\n",""),f,n,count)
                count += 1
                print("Success")
                n += 1
                print("---------------------------------------------------------------------------------------")
        except Exception as e:
            print(uni[i])
            print("Exception big : " + str(e))
            f.write('A' + str(n) , str(count))
            f.write('B' + str(n) , uni[i].replace("\n",""))
            f.write('C' + str(n) , 'The page cannot be reach')
            f.write('D' + str(n) , 'The page cannot be reach')
            f.write('E' + str(n) , 'The page cannot be reach')
            f.write('F' + str(n) , 'The page cannot be reach')
            count += 1
            n += 1
            print("The page cannot be reached")
            print("---------------------------------------------------------------------------------------")
    workbook.close()
