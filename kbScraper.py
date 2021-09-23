from bs4 import BeautifulSoup as bs
import requests, lxml

URL = "https://realpython.com/beautiful-soup-web-scraper-python/"
page = requests.get(URL)
soup = bs(page.content, "lxml")
