from bs4 import BeautifulSoup as bs
import requests
import lxml
import openpyxl as opx
import pandas as pd

class Scraper:

    def __init__(self, URL, page, soup):
        self.URL = URL
        self.page = page
        self.soup = soup


    URL = "https://kbdfans.com/collections/keycaps"
    page = requests.get(URL)
    soup = bs(page.content, "lxml")

    priceList = []
    productTitleList = []


    def getData():

        pageIndex = 1
        while pageIndex != 19 + 1:
            pageURL = Scraper.URL + f"?page={pageIndex}"
            pageURL_requests = requests.get(pageURL)
            pageSoup = bs(pageURL_requests.content, 'lxml')

            for price in pageSoup.find_all("span", {"class": "theme-money"}):
                Scraper.priceList.append(price.text)

            for product in pageSoup.find_all("div", {"class": "product-block__title"}):
                Scraper.productTitleList.append(product.text)
            pageIndex += 1


    def printData():

        for product, price in zip(Scraper.productTitleList, Scraper.priceList):
            print(product.strip() + "..." + price.strip())



Scraper.getData()
# Scraper.printData()

workbook = opx.Workbook()
workbookFileName = "KBsheet.xlsx"

activeWorksheet = workbook.active
activeWorksheet.title = "Keycaps"

testDF = pd.DataFrame(Scraper.productTitleList)
writer = pd.ExcelWriter(r"C:\Users\valex\Desktop\KBsheet.xlsx")
testDF.to_excel(writer, sheet_name="Keycaps", index=False)
writer.save()





print('end')
