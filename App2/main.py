import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from arxiv import *
from scienceDirect import *
from wiley import *

print('[1] : arXiv\n[2] : ScienceDirect\n[3] : Wiley')
choice = input("Enter your choice : ")
if(choice == "1"):
    key = input('Enter the keyword : ')
    arXiv(key)
elif(choice == "2"):
    key = input('Enter the keyword : ')
    aut = input('Enter the author : ')
    scienceDirect(key,aut)
elif(choice == "3"):
    key = input("Enter the keyword : ")
    wiley(key)
