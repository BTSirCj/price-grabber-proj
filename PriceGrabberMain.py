from bs4 import BeautifulSoup
import requests
import json
import smtplib
import time
import sys
import re
from datetime import datetime

#add diff functions for diff websites (newegg, amazon, bestbuy)
#add a function to account for tax, ($350 ($370 post tax))
#user agent stuff for fake req

global finURL

def check_price_bestbuy():
    url = input("Enter URL: ")
    finURL = url

    headers = {
    'authority' : 'www.bestbuy.com',
    'pragma' : 'no.cache',
    'cache-control' : 'no-cache',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept' : '*/*',
    'sec-fetch-site' : 'same-origin',
    'sec-fetch-mode' : 'cors',
    'sec-fetch-dest' : 'empty',
    'referer' : url,
    'accept-language' : 'en-US,en;q=0.9'
}

    result = requests.get(url, headers=headers)
    #result_formatted = json.loads(result.content.decode('utf-8-sig').encode('utf-8'))
    doc = BeautifulSoup(result.text, "html.parser")
    #print(doc.prettify)

    temp = doc.findAll("div", "priceView-hero-price priceView-customer-price")
    #print("\$.*" in temp)
    price = str(temp)
    price = price.split('$')[1]
    finPrice = price.split('<')[0]
    finPrice = finPrice.replace(',', '')
    finPrice = float(finPrice)

    print(finPrice)
    #print(price)

    #if(convPrice < 500.00):
        #send_mail()

def check_price_amazon():
    url = input("Enter URL: ")
    finURL = url

    headers = {
    'authority' : 'www.bestbuy.com',
    'pragma' : 'no.cache',
    'cache-control' : 'no-cache',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept' : '*/*',
    'sec-fetch-site' : 'same-origin',
    'sec-fetch-mode' : 'cors',
    'sec-fetch-dest' : 'empty',
    'referer' : url,
    'accept-language' : 'en-US,en;q=0.9'
}

    result = requests.get(url, headers=headers)
    #result_formatted = json.loads(result.content.decode('utf-8-sig').encode('utf-8'))
    doc = BeautifulSoup(result.text, "html.parser")
    docFinal = BeautifulSoup(doc.prettify(), "html.parser")

    #print(doc.prettify)


    #fix so that small $ and big $ are recognized. Maybe an if elif? check which it is.
    temp = docFinal.findAll("span", "a-price a-text-price a-size-medium apexPriceToPay")
    #temp = docFinal.findAll("span", "a-price aok-align-center reinventPricePriceToPayMargin priceToPay")

    print(temp)
    #print("\$.*" in temp)
    #price = str(temp)
    #price = price.split('$')[1]
    #finPrice = price.split('<')[0]
    #finPrice = finPrice.replace(',', '')
    #finPrice = float(finPrice)

    #temp = docFinal.findAll("span", "a-price a-text-price a-size-medium apexPriceToPay")
    #print(finPrice)


def send_mail():
    url = finURL
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

check_price_amazon()
global counter
counter = 1
while(counter >= 0):
    while(True):
        #check_price()
        #print(counter)
        time.sleep(5)
        counter -=1
        if(counter == 0):
            sys.exit(0)