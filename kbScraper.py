from bs4 import BeautifulSoup as bs
import requests
import pandas as pd



priceList = []
productTitleList = []
productAndPriceZipped = []

def getData(URL, sheetTitle):

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




    sheetTitles = ['Keycaps', 'Switches']

    productColumn = pd.DataFrame(productAndPriceZipped, columns=["Product", "Price"])
    writer = pd.ExcelWriter(r"C:\Users\VD102541\Desktop\KBsheet.xlsx")
    productColumn.to_excel(writer, sheet_name=sheetTitle, index=False)

    writer.sheets[sheetTitle].set_column('A:A', 75)

    writer.save()


#function calls

# I don't know why these 2 function calls don't create new sheets within KBsheet. The result of these 2 function calls is a single sheet, whichever was called second
# (in this case it's keycaps)
getData('https://kbdfans.com/collections/switches', 'Switches')
getData('https://kbdfans.com/collections/keycaps', 'Keycaps')


print('end')
