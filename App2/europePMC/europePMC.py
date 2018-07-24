import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
import re
import xlsxwriter

def checkCountry(text):
    check = True
    countryArr = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo", "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire", "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands", "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of", "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russian Federation","Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)","Scotland","Czechoslovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain", "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname", "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic","Syria", "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo", "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom","England", "United States","United States of America","U.S.A.","America", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe","USA","UK"]
    for each in countryArr:
        match = re.search(each, text)
        if(match):
            return match.group(0)
    if(check):
        return(" ")


def crawInfo(input,f,count,n):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(input, headers=headers)
    page = soup(response.content, "html5lib")

    #------------initialization----------------------------------------------------------------
    print(input)
    f.write('A' + str(n) , str(count))
    f.write('B' + str(n) , input)

    #------------Title----------------------------------------------------------------
    try:
        title = page.find("span",{"class":"abs_citation_title"})
        print("Title : " + title.text)
        f.write('C' + str(n) , title.text)
    except Exception as e:
        print("Exception title : " + str(e))
        f.write('C' + str(n) , 'Cannot get title')

    #------------Journal and date----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        journalDiv = div.find("div",{"class":"abs_link_metadata"})
        journal = journalDiv.a.text
        date = journalDiv.span.text
        print("Journal : " + journal)
        f.write('D' + str(n) , journal)
        print("Date : " + date)
        f.write('E' + str(n) , date)
    except Exception as e:
        print("Exception journal and date : " + str(e))
        f.write('D' + str(n) , 'Cannot get journal name')
        f.write('E' + str(n) , 'Cannot get date')

    #------------DOI----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abs_link_metadata"})
        temp = div.find("div",{"class":"metaData"})
        doi = temp.find("a")
        print("DOI : " + doi.text)
        f.write('F' + str(n) , doi.text)
    except Exception as e:
        print("Exception DOI : " + str(e))
        f.write('F' + str(n) , 'Cannot get doi number')

    #------------Authors and email----------------------------------------------------------------
    try:
        div = page.find("div",{"class":"abstract--main-authors-list"})
        all = div.findAll("div",{"class":"inline-block author-block"})
        for each in all:
            author = each.find("h3").text
            print("Author : " + author)
            f.write('G' + str(n) , author)
            affi = each.find("span",{"class":"author-refine-subtitle"}).text
            print("Affiliation : " + affi)
            f.write('I' + str(n) , affi)
            country = checkCountry(affi)
            f.write('J' + str(n) , country)
            try:
                match = re.search("(( )[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", affi)
                if (match):
                    print("Email : " + match.group(0))
                    f.write('H' + str(n) , match.group(0))
                else:
                    print("Cannot get email")
                    f.write('H' + str(n) , 'Cannot get email')
            except Exception as e:
                print("Exception email : " + str(e))
                f.write('H' + str(n) , 'Cannot get email')
            n += 1
    except Exception as e:
        print("Exception Authors : " + str(e))
        f.write('G' + str(n) , 'Cannot get author name')
        n += 1
    print("---------------------------------------------------------------------------------------")
    return n


#-------------------------------------------------------------------------------------------------------------------------------
def pmc(input,name):
    now = datetime.datetime.now()
    filename = "europePMC_" + name + ".xlsx"
    filepath = "europePMC/csv/" + filename
    workbook = xlsxwriter.Workbook(filepath)
    f = workbook.add_worksheet()
    f.write('A1', 'Keyword : ')
    f.write('B1', input)
    f.write('A2', 'Database : ')
    f.write('B2', 'https://europepmc.org/')
    f.write('A3', 'Date : ')
    f.write('B3', str(now.isoformat()))
    count = 1
    n = 4
    header = "S.No,Title,Journal name,Date,Doi number,Author name,E-mail,Affiliation\n"
    f.write('A' + str(n) , 'S.No')
    f.write('B' + str(n) , 'Website')
    f.write('C' + str(n) , 'Title')
    f.write('D' + str(n) , 'Journal name')
    f.write('E' + str(n) , 'Date')
    f.write('F' + str(n) , 'Doi number')
    f.write('G' + str(n) , 'Author name')
    f.write('H' + str(n) , 'E-mail')
    f.write('I' + str(n) , 'Affiliation')
    f.write('J' + str(n) , 'Country')
    n += 1
    for i in range(1,999999):
        try:
            link = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            # my_url = 'https://europepmc.org/search?query=climate&page=1'
            my_url = 'https://europepmc.org/search?query=' + input.replace(" ","+") + '&page=' + str(i)
            response = requests.get(my_url, headers=headers)
            page = soup(response.content, "html5lib")
            body = page.findAll("a",{"class":"resultLink linkToAbstract"})
            print("---------------------------------------------------------------")
            print("Input : " + input)
            print("real : https://europepmc.org/search?query=climate&page=1")
            print("URL : " + my_url)
            print(len(body))
            for each in body:
                link.append("https://europepmc.org" + each['href'].replace(".",""))
                print("link : https://europepmc.org" + each['href'].replace(".",""))
                print("--------------------------------------------------------------")
            for each in link:
                n = crawInfo(each,f,count,n)
                count += 1
                n += 1
        except Exception as e:
            print("Exception big : " + str(e))
            break
    workbook.close()
