from bs4 import BeautifulSoup as bs
from numpy import product
import requests
import pandas as pd
import openpyxl as opx


def getData(URL):
    '''Gets product title and pricing data from a shopify site. The title and price are zipped into a list of tuples, later converted to Pandas 
    dataframes and copied to an excel spreadsheet'''
    
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

'''URLs can be added or removed from these lists based on the product categories for which the user wants pricing data. 
# A corresponding sheet name must be added to sheetNames for each URL'''
listOfURLs = ["https://kbdfans.com/collections/keycaps",
              "https://kbdfans.com/collections/switches",
              "https://kbdfans.com/collections/keyboard-part",
              "https://kbdfans.com/collections/diy-kit"]
sheetNames = ['Keycaps', 'Switches', 'Accessories', 'Kits']
    

#(There might be a more elegant way to do this) This is a boilerplate Dataframe, copied to each sheet from the sheetNames list.
df = pd.DataFrame(columns=['Product Name', 'Price'])
writer = pd.ExcelWriter(r"C:\Users\VD102541\Desktop\KBsheet.xlsx")

# creates the sheets from sheetNames
for name in sheetNames:
    df.to_excel(writer, sheet_name=name, index=False)
    writer.sheets[str(name)].set_column('A:A', 75)
    
# iteratively passes urls from listOfURLs to the getData() function. A dataframe is created for each URL and copied to the spreadsheet. 
for index, url in enumerate(listOfURLs):
    getData(url)
    urlDF = pd.DataFrame(getData(url), columns=['Product Name', 'Price'])
    urlDF.to_excel(writer, sheet_name=sheetNames[index], index=False)
writer.save()




print('end')
