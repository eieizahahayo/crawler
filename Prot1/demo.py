import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
import json
import re

my_url = 'https://www.sciencedirect.com/science/article/pii/S1871678416325687'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
response = requests.get(my_url, headers=headers)
page = soup(response.content, "html5lib")
counter = page.findAll("a",{"class":"author size-m workspace-trigger"})
emails = page.find("script" ,{"type":"application/json"})
data = json.loads(emails.text) #a dictionary!
ans = json.dumps(data,indent=3)


content = data.get('authors').get('content')
for i in range(0, len(content)):
    card = content[i].get('$$')
    # fucker = json.dumps(card,indent=3)
    # print(fucker)
    for j in range(0, len(counter)):
        outer = card[j].get('$$')
        outer2 = json.dumps(outer,indent=3)
        print(outer2)
        
        name = outer[0].get("_")
        surname = outer[1].get("_")
        realname = name + " " + surname
        print("Name : " + realname)
        if(len(outer) > 2):
            try:
                email = outer[len(outer)-1].get("_")
                print("Email : " + email)
            except Exception as e:
                print("Cannot get email")
        try:
            temp = outer[2].get("$$")
            id = temp[0].get("_")
            print("id : " + id)
        except Exception as e:
            id = "not-match"
            print("Exception : " + str(e))
        print("---------------------------------------------------------------")

    print("*****************************************************************************************")

    for j in range(len(counter),len(card)-1):
        try:
            outer = card[j].get('$$')
            outer2 = json.dumps(outer,indent=3)
            print(outer2)
            if(len(outer) == 2):
                affi = outer[0].get("_")
                temp = outer[1].get("$$")
                country = temp[len(temp)-1].get("_")
                print("Affiliation : " + affi)
                print("Country : " + country)
            elif(len(outer) > 2):
                try:
                    print("First way")
                    id = outer[0].get("_")
                    affi = outer[1].get("_")
                    temp = outer[2].get("$$")
                    country = temp[len(temp)-1].get("_")
                except:
                    print("Second way")
                    id = outer[0].get("_")
                    temp = outer[1].get("$$")
                    affi = temp[0].get("_")
                    temp2 = outer[2].get("$$")
                    country = temp[len(temp)-1].get("_")
                print("Id : " + id)
                print("Affiliation : " + str(affi))
                print("Country : " + country)
                print("---------------------------------------------------------------")
        except Exception as e:
            print("Exception : " + str(e))
            
    print("================================================================")






















# authors = page.findAll("span",{"class":"content"})
# for ele in authors:
#     temp = ele.findAll("span")
#     name = temp[0].text
#     surname = temp[1].text
#     print(name + " " + surname)
