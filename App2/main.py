import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from arxiv.arxiv import *
from acs.acs import *
from scienceDirect.scienceDirect import *
from wiley.wiley import *
from springer.springer import *
from sagepub.sagepub import *
from researchgate.researchgate import *
from europePMC.europePMC import *

print('[1] : Wiley\n[2] : Springer\n[3] : Europe PMC\n[4] : ScienceDirect\n[5] : arXiv\n[6] : ACS')
choice = input("Enter your choice : ")
if(choice == "1"):
    key = input('Enter the keyword : ')
    name = input("Enter file name : ")
    wiley(key,name)
elif(choice == "2"):
    key = input('Enter the keyword : ')
    name = input("Enter file name : ")
    springer(key,name)
elif(choice == "3"):
    key = input("Enter the keyword : ")
    name = input("Enter file name : ")
    pmc(key,name)
elif(choice == "4"):
    key = input("Enter the keyword : ")
    name = input("Enter file name : ")
    scienceDirect(key,name)
# elif(choice == "5"):
#     key = input("Enter the keyword : ")
#     name = input("Enter file name : ")
#     sage(key,name)
# elif(choice == "6"):
#     key = input("Enter the keyword : ")
#     name = input("Enter file name : ")
#     gate(key,name)
elif(choice == "5"):
    key = input("Enter the keyword : ")
    name = input("Enter file name : ")
    arXiv(key,name)
elif(choice == "6"):
    key = input("Enter the keyword : ")
    name = input("Enter file name : ")
    acs(key,name)
