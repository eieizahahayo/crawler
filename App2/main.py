import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from arxiv import *
from scienceDirect import *

print('[1] : arXiv\n[2] : ScienceDirect')
choice = input("Enter your choice : ")
if(choice == 1):
    key = input('Enter the keyword : ')
    arXiv(key)
else:
    key = input('Enter the keyword : ')
    aut = input('Enter the author : ')
    scienceDirect(key,aut)
