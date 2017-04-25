import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.firefox.webdriver import FirefoxProfile

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


PROXY = "52.183.30.241:8888"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
executable_path = 'D:\Machine Learning\\Anaconda Python Workspace\\Anaconda3\\chromedriver.exe'
browser = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
# browser.get("http://whatismyipaddress.com")

# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
browser.get("https://www.dollardays.com/sitelogin.aspx")

username = 'asad1996172@gmail.com'
password = 'degaymon00'

user = browser.find_element_by_css_selector("#inputLoginUsername")
passs = browser.find_element_by_css_selector("#inputLoginPassword")

user.send_keys(username)
passs.send_keys(password)

browser.find_element_by_css_selector("#ctl00_cphContent_btnLoginSignIn").click()


browser.get('https://www.dollardays.com/wholesale-accessories-pg13.html')

grid = browser.find_element(By.XPATH,'//*[@id="central-content"]/div[9]')
products = grid.find_elements(By.XPATH,'//div[@class="col-xs-12 col-sm-6 col-md-4 col-lg-3 prod-tile"]');
detail_links = []
upcs=[]
productTitles =[]
skus = []
wholesale_prices = []
for product in products:


    baseinfo = product.find_element_by_class_name('baseinfo')
    baseinfo = baseinfo.text
    baseinfo = baseinfo.splitlines()
    productTitle = baseinfo[0]
    sku_number = baseinfo[1].split('|')[0]
    wholesale_price = find_between(product.text,"As low as","/ unit!").lstrip()
    # upc=""

    # details_link = product.find_element(By.XPATH, '//div[@class="col-xs-12 text-center btnCollectionGrp"]');
    try:
        detail_links.append(product.find_element_by_css_selector(".btn.dd-btn-primary.more-details.fsig").get_attribute("href"))
    except NoSuchElementException:
        detail_links.append(product.find_element_by_css_selector(".btn.dd-btn-quaternary.more-details.fsig").get_attribute("href"))


    productTitles.append(productTitle)
    skus.append(sku_number)
    wholesale_prices.append(wholesale_price)


    print(productTitle)
    print(sku_number)
    print(wholesale_price)
    print("\n\n")

print(detail_links)

for link in detail_links:
    if link!="":
        browser.get(link)
        try:
            upc = browser.find_element(By.XPATH, '//div[@id="ctl00_cphContent_divUPC"]').text;
        except NoSuchElementException:

            upc = ""
        upcs.append(upc)
        print(upc)
    else:
        upcs.append("")
        print("")

print(len(productTitles))
print(len(skus))
print(len(upcs))
print(len(wholesale_prices))

all_data=[]
for i in range(len(productTitles)):
    all_data.append({'Product Title': productTitles[i], 'SKU #': skus[i], 'UPC': upcs[i], 'Whole Sale Price Per Unit': wholesale_prices[i]})

all_data = pd.DataFrame(all_data)
if not os.path.isfile('dollarsday.csv'):
    all_data.to_csv('dollarsday.csv', header='column_names',index=False)
else:  # else it exists so append without writing the header
    all_data.to_csv('dollarsday.csv', mode='a', header=False,index=False)