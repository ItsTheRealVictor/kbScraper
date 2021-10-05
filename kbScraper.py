from bs4 import BeautifulSoup as bs
from numpy import product
import requests
import pandas as pd
import openpyxl as opx





def getData(URL):

    priceList = []
    productTitleList = []
    productAndPriceZipped = []

    page = requests.get(URL)
    pageSoup = bs(page.content, "lxml")

    pageIndex = 1
    while pageIndex != 19 + 1:
        pageURL = URL + f"?page={pageIndex}"
        pageURL_requests = requests.get(pageURL)
        pageSoup = bs(pageURL_requests.content, 'lxml')

        for price in pageSoup.find_all("span", {"class": "theme-money"}):
            priceList.append(price.text.strip())

        for product in pageSoup.find_all("div", {"class": "product-block__title"}):
            productTitleList.append(product.text.strip())
        pageIndex += 1

    #Zip the data from the productTitleList and priceList into a list of tuples
    for product, price in zip(productTitleList, priceList):
        productAndPriceZipped.append((product, price))

    return productAndPriceZipped


sheetNames = ['Keycaps', 'Switches', 'Accessories', 'Kits']
listOfURLs = ["https://kbdfans.com/collections/keycaps",
              "https://kbdfans.com/collections/switches",
              "https://kbdfans.com/collections/keyboard-part",
              "https://kbdfans.com/collections/diy-kit"]
    

df = pd.DataFrame(columns=['Product Name', 'Price'])
writer = pd.ExcelWriter(r"C:\Users\VD102541\Desktop\KBsheet.xlsx")

for name in sheetNames:
    df.to_excel(writer, sheet_name=name, index=False)
    writer.sheets[str(name)].set_column('A:A', 75)

for index, url in enumerate(listOfURLs):
    getData(url)
    urlDF = pd.DataFrame(getData(url), columns=['Product Name', 'Price'])
    urlDF.to_excel(writer, sheet_name=sheetNames[index], index=False)
writer.save()




print('end')
