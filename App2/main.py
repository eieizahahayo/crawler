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

print('[1] : arXiv\n[2] : ScienceDirect\n[3] : Wiley\n[4] : Springer\n[5] : Sagepub\n[6] : Research gate\n[7] : Europe PMC\n[8] : ACS')
choice = input("Enter your choice : ")
if(choice == "1"):
    key = input('Enter the keyword : ')
    arXiv(key)
elif(choice == "2"):
    key = input('Enter the keyword : ')
    scienceDirect(key)
elif(choice == "3"):
    key = input("Enter the keyword : ")
    wiley(key)
elif(choice == "4"):
    key = input("Enter the keyword : ")
    springer(key)
elif(choice == "5"):
    key = input("Enter the keyword : ")
    sage(key)
elif(choice == "6"):
    key = input("Enter the keyword : ")
    gate(key)
elif(choice == "7"):
    key = input("Enter the keyword : ")
    pmc(key)
elif(choice == "8"):
    key = input("Enter the keyword : ")
    acs(key)
