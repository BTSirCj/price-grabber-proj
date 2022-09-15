from itertools import product
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import sys
import re
from datetime import datetime

#add diff functions for diff websites (newegg, amazon, bestbuy)
#add a function to account for tax, ($350 ($370 post tax))
#user agent stuff for fake req

#grab the name of the item
#make function to ask which retailer to use
#add error catcher, to grab if link works or not

#add newegg again...
#newegg done

global tax
tax = .10

def check_price_newegg():
    global neURL
    neURL = input("Enter URL (NEWEGG): ")
    #priceWant = input("Enter price you want it to be: ")
    #priceWant = int(priceWant)

    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    result = requests.get(neURL)
    doc = BeautifulSoup(result.text, "html.parser")
    docFinal = BeautifulSoup(doc.prettify(), "html.parser")

    productName = docFinal.find("h1", "product-title").string.strip()

    temp = docFinal.find("span", "price-current-label")
    pre = temp.parent.find("sup").string
    temp = temp.parent.find("strong").string
    price = int(temp)
    cents = float(pre)
    finPrice = price + cents

    print("NEWEGG")
    print(productName)
    print(finPrice)
    print("NEWEGG DONE")



def check_price_bestbuy():
    webType = "best buy"
    url = input("Enter URL (BEST BUY): ")
    global bbURL
    bbURL = url
    priceWant = input("Enter the price you want it to be: ")

    headers = {
    'authority' : 'www.bestbuy.com',
    'pragma' : 'no.cache',
    'cache-control' : 'no-cache',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept' : '*/*',
    'sec-fetch-site' : 'same-origin',
    'sec-fetch-mode' : 'cors',
    'sec-fetch-dest' : 'empty',
    'referer' : bbURL,
    'accept-language' : 'en-US,en;q=0.9'
}

    result = requests.get(bbURL, headers=headers)
    #result_formatted = json.loads(result.content.decode('utf-8-sig').encode('utf-8'))
    doc = BeautifulSoup(result.text, "html.parser")
    #print(doc.prettify)

    productName = doc.find("h1", "heading-5 v-fw-regular").string.strip()

    #finish working on catching monthly payment
    temp = doc.findAll("div", "priceView-hero-price priceView-customer-price")
    monChecker = doc.find_all("span", "priceView-subscription-units")
    price = str(temp)
    monthly = str(monChecker)
    monthly = monthly.find('/')
    price = price.split('$')[1]
    #monthly = monChecker.split('/')[1]
    finPrice = price.split('<')[0]
    finPrice = finPrice.replace(',', '')
    finPrice = float(finPrice)

    print("BEST BUY: ")
    print(productName)
    print(f"${finPrice}")
    print(monthly)
    print(priceWant)

    print("BEST BUY DONE")

    #if(finPrice < priceWant):
    #    send_mail(webType)

#try implement a discount checker to see % off in current discount
def check_price_amazon():
    webType = "amazon"
    global amURL
    url = input("Enter URL (AMAZON): ")
    amURL = url
    priceWant = input("Enter the price you want it to be: ")
    priceWant = int(priceWant)


    headers = {
    'authority' : 'www.bestbuy.com',
    'pragma' : 'no.cache',
    'cache-control' : 'no-cache',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept' : '*/*',
    'sec-fetch-site' : 'same-origin',
    'sec-fetch-mode' : 'cors',
    'sec-fetch-dest' : 'empty',
    'referer' : amURL,
    'accept-language' : 'en-US,en;q=0.9'
}

    result = requests.get(amURL, headers=headers)
    doc = BeautifulSoup(result.text, "html.parser")
    docFinal = BeautifulSoup(doc.prettify(), "html.parser")

    productName = docFinal.find("h1", "title")

    #checkers which type of $ is used. Small $ or Big $
    temp = docFinal.findAll("span", "a-price a-text-price a-size-medium apexPriceToPay")
    checker = bool(temp)
    if(checker == False): #checks if small $ is used, if it isnt, will switch to finding big $
        temp = docFinal.findAll("span", "a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
    
    prodID = docFinal.find("span", "a-size-large product-title-word-break").string
    

    price = str(temp)
    price = price.split('$')[1]
    finPrice = price.split('<')[0]
    finPrice = finPrice.replace(',', '')
    finPrice = float(finPrice)

    #apply tax
    finTax = finPrice * tax
    finTax += finPrice
    print("AMAZON")
    #print(productName)
    print(f"Pre Tax Price: ${finPrice}, \nPost Cali 10% Tax Price: ${round(finTax, 2)}")
    print(priceWant)
    print(prodID)
    print("AMAZON DONE")

    #send mail
    #if(finPrice <= priceWant):
    #    send_mail(webType)


def send_mail(name):
    if(name == "best buy"):
        url = bbURL
    elif(name == "amazon"):
        url = amURL
    elif(name == "newegg"):
        url = neURL        

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls() #encrypts connection
    server.ehlo()
    server.login('sirrrcj@gmail.com', 'lrzoipmzsakmmsjc') #logs into email

    subject = "Price checker"
    body = f"The link: {url}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "sirrrcj@gmail.com",
        "cjtanner11@gmail.com",
        msg
    )

    print("EMAIL SENT!")
    server.quit()

#check_price_newegg()
#check_price_bestbuy()
check_price_amazon()
global counter
counter = 1
while(counter >= 0):
    while(True):
        #check_price_amazon()
        #print(counter)
        time.sleep(1)
        counter -=1
        if(counter == 0):
            sys.exit(0)