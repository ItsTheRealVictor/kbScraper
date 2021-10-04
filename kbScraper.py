from bs4 import BeautifulSoup as bs
import requests
import xlsxwriter
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
    productAndPriceZipped = []

    def getData():

        pageIndex = 1
        while pageIndex != 19 + 1:
            pageURL = Scraper.URL + f"?page={pageIndex}"
            pageURL_requests = requests.get(pageURL)
            pageSoup = bs(pageURL_requests.content, 'lxml')

            for price in pageSoup.find_all("span", {"class": "theme-money"}):
                Scraper.priceList.append(price.text.strip())

            for product in pageSoup.find_all("div", {"class": "product-block__title"}):
                Scraper.productTitleList.append(product.text.strip())
            pageIndex += 1


    def zipData():

        for product, price in zip(Scraper.productTitleList, Scraper.priceList):
            Scraper.productAndPriceZipped.append((product, price))



Scraper.getData()
Scraper.zipData()

workbook = opx.Workbook()
workbookFileName = "KBsheet.xlsx"


activeWorksheet = workbook.active
activeWorksheet.title = "Keycaps"

productColumn = pd.DataFrame(Scraper.productAndPriceZipped, columns=["Product", "Price"])
writer = pd.ExcelWriter(r"C:\Users\VD102541\Desktop\KBsheet.xlsx")
productColumn.to_excel(writer, sheet_name="Keycaps", index=False)

writer.sheets['Keycaps'].set_column('A:A', 75)

writer.save()



print('end')
