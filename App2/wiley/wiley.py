import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import xlsxwriter

def checkCountry(text,country):
    check = True
    countryArr = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation","Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)","Scotland","Czechoslovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname", "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic","Syria", "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom","England", "United States" ,"U.S.A.","America","United States of America", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe","USA","UK"]
    for each in countryArr:
        match = re.search(each, text)
        if(match):
            country.append(match.group(0))
            check = False
    if(check):
        country.append(" ")

def contact(input,f,n):
    print("enter contact")
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")
    body = page.findAll("div",{"class":"accordion-tabbed__tab-mobile accordion__closed"})
    print(len(body))
    for i in range(len(body) // 2):
        email = []
        country = []
        affiliation = []
        #--------------Authors----------------------------------------------
        print("Author : " + body[i].a.span.text)
        f.write('H' + str(n) , body[i].a.span.text)
        try:
            add = body[i].find("div",{"class":"author-info accordion-tabbed__content"})
            try:
                allP = add.findAll("p")
                for each in allP:
                    print("Address : " + each.text)
                    affiliation.append(each.text)
                    match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+)", each.text)
                    if(match):
                        email.append(match.group(0))
                        print("Found email in author : " + match.group(0))
            except Exception as e:
                print("Exception address1 : " + str(e))
                f.write('K' + str(n) , "Cannot get affiliation")
        except Exception as e:
            print("Exception address2 : " + str(e))
            f.write('K' + str(n) , 'Cannot get affiliation')

        #--------------email 1----------------------------------------------
        print("Len email : " + str(len(email)))
        try:
            info = body[i].find("div",{"class":"bottom-info"})
            match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", info.text)
            if match:
                print("Email : " + match.group(0))
                email.append(match.group(0))
            else:
                print("Email not match :" + info.text)
                print("Email not match")
                if(len(email) == 0):
                    print("Enter if len(email)")
                    email.append("Cannot get email")
        except Exception as e:
            print("Exception email : " + str(e))
            if(len(email) == 0):
                print("Enter if len(email)")
                email.append("Cannot get email")

        if(len(email) == 0):
            f.write('I' + str(n) , 'Cannot get email')
        else:
            f.write('I' + str(n) , email[0])

        #--------------email 2----------------------------------------------
        try:
            text = page.find("div",{"class":"article-header__correspondence-to"})
            match = re.search(body[i].a.span.text, text.text)
            if(match):
                match = re.search("(( )*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text.text)
                if(match):
                    f.write('J' + str(n) , match.group(0))
                else:
                    f.write('J' + str(n) , 'Cannot get email')
            else:
                f.write('J' + str(n) , 'Cannot get email')
        except Exception as e:
            print("Exception email2 : " + str(e))
            f.write('J' + str(n) , 'Cannot get email')
        print("-----------------------------------------")
        #--------------Country and affiliation----------------------------------------------
        for each in affiliation:
            checkCountry(each,country)
        try:
            for i in range(0,len(affiliation)):
                f.write('K' + str(n) , affiliation[i])
                f.write('L' + str(n) , country[i])
                print("Affiliation : " + affiliation[i])
                print("Country : " + country[i])
                n += 1
        except Exception as e:
            print("Exception country : " + str(e))
    return n

#-------------------------------------------------Wiley------------------------------------------------------------------------------
def wiley(input,name):
    filename = "Wiley_" + name + ".xlsx"
    filepath = "wiley/csv/" + filename
    now = datetime.datetime.now()
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://onlinelibrary.wiley.com/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    count = 1
    n = 4
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Website')
    f.write('C' + str(n) , 'Title')
    f.write('D' + str(n) , 'Journal name')
    f.write('E' + str(n) , 'Volume')
    f.write('F' + str(n) , 'Date')
    f.write('G' + str(n) , 'Doi number')
    f.write('H' + str(n) , 'Author name')
    f.write('I' + str(n) , 'E-mail by method1')
    f.write('J' + str(n) , 'E-mail by method2')
    f.write('K' + str(n) , 'Affiliation')
    f.write('L' + str(n) , 'Country')
    n += 1
    for i in range(0,999999):
        print("Page : " + str(i))
        stop = True
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            a = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","+") + '&startPage=&PubType=journal'
            b = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=' + input.replace(" ","%20") + '&startPage=' + str(i) + '&PubType=journal'
            my_url = ""
            if(i == 0):
                my_url = a
            else:
                my_url = b
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("div",{"class":"item__body"})
            for each in body:
                link = each.h2.span.a['href']
                title = each.h2.text
                info = each.find("div",{"class":"meta__info"})
                date = info.find("span",{"class":"meta__epubDate"}).text
                doi = each.h2.span.a['href']

                #-------------------Initialization--------------------------------------------------------
                print("link : " + link)
                f.write('A' + str(n) , str(count))
                f.write('B' + str(n) , 'https://onlinelibrary.wiley.com' + link)

                #--------------Title----------------------------------------------
                print("Title : " + title)
                f.write('C' + str(n) , title)

                #--------------Journal----------------------------------------------
                journal = info.find("a",{"class":"meta__serial"}).text
                print("Journal : " + journal)
                f.write('D' + str(n) , journal)
                try:
                    vol = info.find("a",{"class":"meta__volume"}).text
                    print("Volume : " + vol)
                    f.write('E' + str(n) , vol)
                except Exception as e:
                    print("Exception volume : " + str(e))
                    f.write('E' + str(n) , 'Cannot get volume')
                #--------------Date----------------------------------------------
                try:
                    print("Date : " + date)
                    f.write('F' + str(n) , date)
                except Exception as e:
                    print("Exception date : " + str(e))
                    f.write('F' + str(n) , 'Cannot get date')

                #--------------Doi----------------------------------------------
                try:
                    print("Doi : https://nph.onlinelibrary.wiley.com" + doi)
                    f.write('G' + str(n) , 'https://nph.onlinelibrary.wiley.com' + doi)
                except Exception as e:
                    print("Exception doi : " + str(e))
                    f.write('G' + str(n) , 'Cannot get doi')

                #--------------Authors and email----------------------------------------------
                parse = "https://nph.onlinelibrary.wiley.com" + doi
                n = contact(parse,f,n)
                print("-------------------------------------------")
                count += 1
                n += 1
                stop = False
            if(stop):
                break
        except Exception as e:
                print("Exception big : " + str(e))
                print("Page : " + str(i))
                break
    print("Jimmy")
    workbook.close()
