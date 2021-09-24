from bs4 import BeautifulSoup as bs
import requests, lxml

URL = "https://kbdfans.com/collections/keycaps"
page = requests.get(URL)
soup = bs(page.content, "lxml")

priceList = []
productTitleList = []

pageIndex = 1
while pageIndex != 19 + 1:
    pageURL = URL + f"?page={pageIndex}"
    pageURL_requests = requests.get(pageURL)
    pageSoup = bs(pageURL_requests.content, 'lxml')
    for price in pageSoup.find_all("span", {"class": "theme-money"}):
        priceList.append(price.text)
    pageIndex += 1

print((priceList[5:10])) # a test to see if the while loop works

print('end')
