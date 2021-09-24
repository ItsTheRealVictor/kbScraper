from bs4 import BeautifulSoup as bs
import requests, lxml

URL = "https://kbdfans.com/collections/keycaps?page=1"
page = requests.get(URL)
soup = bs(page.content, "lxml")


#lists containing product data
productPrices = soup.find_all("span", {"class":"theme-money"})
productTitles = soup.find_all("div", {"class":"product-block__title"})



#Test loop to see if find_all() function retrieved desired data
for productTitle, price in zip(productTitles, productPrices):
    price = str(price.text)
    productTitle = str(productTitle.text)
    print(productTitle + price)
