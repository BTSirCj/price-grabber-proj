from distutils.util import check_environ
from itertools import product
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import sys
import re
from datetime import datetime

#add diff functions for diff websites (newegg, amazon, bestbuy) X
#add a function to account for tax, ($350 ($370 post tax)) X
#user agent stuff for fake req X

#grab the name of the item X
#make function to ask which retailer to use X
#add error catcher, to grab if link works or not -> finish the Url valid checker X

#add newegg again...
#newegg done


def retail_check():
    answer = input("What retailer will you be using?\nAmazon, Best Buy, or Newegg?: ")
    answer = answer.lower()
    if(answer == "amazon"):
        check_price_amazon()
    elif(answer == "best buy"):
        check_price_bestbuy()
    elif(answer == "newegg"):
        check_price_newegg()
    else:
        print("You need to enter either Amazon, Best Buy, or Newegg")

def check_url(url):
    headers = {
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    tempURL = url
    checker = False

    while(checker == False):
            try:
                r = requests.get(tempURL, headers=headers).status_code
                print("URL is valid, checking if broken...")
                if(r == 404 or r == 400):
                    global tryURL
                    tryURL = input("URL is broken. Check URL and try again: ")
                    check_url(tryURL)
                    return tryURL
                else:
                    checker = True
                    tryURL = url
                    return tryURL
            except requests.ConnectionError as exception:
                print("URL does not exist on Internet")
        

global tax
tax = .1025

def check_price_newegg():
    webType = "newegg"
    global neURL
    url = input("Enter URL (NEWEGG): ")
    neURL = check_url(url)


    priceWant = input("Enter price you want it to be: ")
    priceWant = int(priceWant)

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

    #tax
    finTax = finPrice * tax
    finTax += finPrice

    print("NEWEGG")
    print(productName)
    message = f"Pre Tax Price: ${finPrice}, \nPost Cali 10% Tax Price: ${round(finTax, 2)}"
    print("NEWEGG DONE")

    #send mail
    if(finPrice <= priceWant):
        send_mail(webType, productName, message)



def check_price_bestbuy():
    webType = "best buy"
    url = input("Enter URL (BEST BUY): ")
    global bbURL
    bbURL = check_url(url)
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

    #tax
    finTax = finPrice * tax
    finTax += finPrice

    print("BEST BUY: ")
    print(productName)
    message = f"Pre Tax Price: ${finPrice}, \nPost Cali 10% Tax Price: ${round(finTax, 2)}"
    #print(f"Pre Tax Price: ${finPrice}, \nPost Cali 10% Tax Price: ${round(finTax, 2)}")
    #print(monthly)
    #print(priceWant)

    print("BEST BUY DONE")

    if(finPrice < priceWant):
        send_mail(webType, productName, message)
#try implement a discount checker to see % off in current discount
def check_price_amazon():
    webType = "amazon"
    global amURL
    url = input("Enter URL (AMAZON): ")
    amURL = check_url(url)
    priceWant = input("Enter the price you want it to be: ")
    priceWant = int(priceWant)


    headers = {
    'authority' : 'www.amazon.com',
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

    #checkers which type of $ is used. Small $ or Big $
    temp = docFinal.findAll("span", "a-price a-text-price a-size-medium apexPriceToPay")
    checker = bool(temp)
    if(checker == False): #checks if small $ is used, if it isnt, will switch to finding big $
        temp = docFinal.findAll("span", "a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
    
    prodID = docFinal.find("span", "a-size-large product-title-word-break").string.strip()
    

    price = str(temp)
    price = price.split('$')[1]
    finPrice = price.split('<')[0]
    finPrice = finPrice.replace(',', '')
    finPrice = float(finPrice)

    #apply tax
    finTax = finPrice * tax
    finTax += finPrice

    print("AMAZON")
    print(prodID)
    message = f"Pre Tax Price: ${finPrice}, \nPost Cali 10% Tax Price: ${round(finTax, 2)}"
    #print(priceWant)
    print("AMAZON DONE")

    #send mail
    if(finPrice <= priceWant):
        send_mail(webType, prodID, message)

def send_mail(name, prodName, message):
    if(name == "best buy"):
        url = bbURL
    elif(name == "amazon"):
        url = amURL
    elif(name == "newegg"):
        url = neURL        

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() #encrypts connection
    server.login('sirrrcj@gmail.com', 'btnsfegekmidrumz') #logs into email

    subject = f"Price for: {prodName}"
    body = f"The link: {url}\n{message}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "sirrrcj@gmail.com",
        "cjtanner11@gmail.com",
        msg
    )

    print("EMAIL SENT!")
    server.quit()


#retail_check()
counter = 1
while(counter >= 0):
    retail_check()
    while(True):
        #retail_check()
        print(counter)
        time.sleep(10)
        counter -=1
        if(counter == 0):
            sys.exit(0)