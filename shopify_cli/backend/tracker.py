import string
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import smtplib



def checkPrice(data_dict,shop,token):
    response_to_shopify = []
    headers = {}
    headers["User-Agent"] = data_dict["user_agent"]

    if data_dict["website"] == "amazon":

        page = requests.get(data_dict["url"], headers=headers)

        json_data = {
        "price_id": [
            "priceblock_ourprice",
            "priceblock_dealprice"
        ],
        "savings_id": [
            "regularprice_savings",
            "dealprice_savings"
        ],
        "user_agent": "google chrome",
    } 
        soup = BeautifulSoup(page.content, "html.parser")
        data_dict["title"] = soup.find(id="productTitle").get_text().strip()
        for id in json_data["price_id"]:
            try:
                data_dict["price"] = soup.find(id="priceblock_ourprice").get_text()
                break
            except:
                pass
        
        #cleaning
        try:
            data_dict["price"] = re.sub("^₹\\xa0|,", '', data_dict["price"])
            data_dict["price"]= float(data_dict["price"])
        except:
            pass

    elif data_dict["website"] == "snapdeal":
        response = requests.get(data_dict["url"], headers=headers)
        soup = BeautifulSoup(response.content,"html.parser")

        # Selecting only required part of the page i.e Price and title
        cards = soup.find_all("div",attrs = {"class":"pdp-comp comp-product-description clearfix"})

        for card in cards:

            data_dict['title'] = card.find("h1", attrs = {"itemprop":"name"}).text
            data_dict['price']= card.find("span", attrs = {"itemprop":"price"}).text
            
        # Cleaning
        try:
            data_dict["title"] =re.sub('\s+', '', data_dict['title'])
            data_dict['price'] = float(re.sub('[^0-9]+', "",data_dict['price']))

        except:
            pass
    
    elif data_dict["website"] == "flipkart":
        response = requests.get(data_dict["url"], headers=headers)

   
        soup = BeautifulSoup(response.content,"html.parser")
        
        cards = soup.find_all("div",attrs = {"id":"container"})
        
        for card in cards:

            data_dict["title"] = card.find("span", attrs = {"class": "B_NuCI"}).text
            data_dict["price"] = card.find("div", attrs = {"class": "_30jeq3"}).text

         #cleaning
        try:
            data_dict["price"] = re.sub("^₹\\xa0|,", '', data_dict["price"])
            print(data_dict)
            data_dict["price"]= float(data_dict["price"])
        except:
            pass

    #set shopify price

    try:
        if data_dict["intent"] == "less":
            data_dict["shopify"] = data_dict["price"] - float(data_dict["amount"])
        elif data_dict["intent"] == "more":
            data_dict["shopify"] = data_dict["price"] + float(data_dict["amount"])

        else:
            data_dict["shopify"] = data_dict["price"]
    except:
        pass
    
    print("NAME:", data_dict["title"])
    print("Other Ecom PRICE:  ₹", data_dict["price"], "\n")
    print("Your store price must be:  ₹", float(data_dict["shopify"]), "\n")
    prod_id = data_dict["prodid"]
    
    #get_current_price
    dict_prod = getPrice(shop,token,prod_id)

    #get email
    data_dict["email"] = str(getemail(shop,token))

    current_price = dict_prod["price"]
    variant_id = dict_prod["variant_id"]
    data_dict["cp"] = current_price
    data_dict["pn"] = dict_prod["title"]
    shopify_price = str(data_dict["shopify"])
    print("current price:  ₹", float(dict_prod["price"]))
    timestmp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_dict["ts"] = timestmp
    response_to_shopify.append(timestmp)
    response_to_shopify.append(data_dict["website"])
    response_to_shopify.append("0")

    #max-min
    try:

        if data_dict["shopify"]<= float(data_dict["max"]) and data_dict["shopify"]>= float(data_dict["min"]):
            updatePrice(shop,token,prod_id,shopify_price)
            if float(data_dict["shopify"]) != float(current_price):
                response_to_shopify[2] = "1"
                dict_prod = getPrice(shop,token,prod_id)
                updated_price = dict_prod["price"]
                data_dict["up"] = str(updated_price)
                send_email(data_dict)

    except:
        pass
    
    #updated_price
    dict_prod = getPrice(shop,token,prod_id)
    updated_price = dict_prod["price"]
    data_dict["up"] = str(updated_price)
    
    response_to_shopify.append(data_dict["title"])
    response_to_shopify.append(data_dict["url"])
    response_to_shopify.append(dict_prod["title"])
    response_to_shopify.append(str(variant_id))
    response_to_shopify.append(data_dict["email"]) 
    response_to_shopify.append(data_dict["price"])
    response_to_shopify.append(data_dict["intent"]) 
    response_to_shopify.append(data_dict["amount"]) 
    response_to_shopify.append(current_price)
    response_to_shopify.append(updated_price)

    return response_to_shopify


def getPrice(shop,token,prod_id):
    dict_prod = {}
    headers = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': f'{token}',
    }

    x = requests.get(f'https://{shop}.myshopify.com/admin/api/2020-10/products/{prod_id}.json', headers=headers)
    data= x.json()
    # print(data)
    for product in data["product"]["variants"]:
        # print(product)
        dict_prod["price"] = product["price"] 
        dict_prod["variant_id"] = product["id"]
    dict_prod["title"] = data["product"]["title"]


    return dict_prod

  

def updatePrice(shop,token,prod_id,shopify_price):
    data_query = '''
              mutation {
                  productUpdate(input: {id: "gid://shopify/Product/%s", variants: {price:"%s"} } ) {
                    product {
                      id
                    }
                  }
                }
              '''%(prod_id,shopify_price)

    headers = {
      'Content-Type': 'application/graphql',
      'X-Shopify-Access-Token': f'{token}',
    }

    response = requests.post(f'https://{shop}.myshopify.com/admin/api/2020-10/graphql.json', data=data_query, headers=headers)
    print(json.dumps(response.json(), indent=2))
    return response.json()

def getemail(shop,token):
    email = ""
    headers = {
      'Content-Type': 'application/graphql',
      'X-Shopify-Access-Token': f'{token}',
    }
    response = requests.get(f'https://{shop}.myshopify.com/admin/api/2020-10/shop.json', headers=headers)
    data= response.json()
    email= data["shop"]["email"]

    return email


def send_email(data_dict):
    
      
    """
    Sends email from user's email ID to themself.

    Parameter:
        data_dict (dict): Dictionary containing user data
    """
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    print(5335)

    s.starttls()

    # login to email
    s.login("gmail", "password")
    print(5335)

    # write the email subject and body
    subject = "Shopify Price Change Alert"

    body = """The following changes has been made on the product you have selected for price automation. Please have a look.
    Time: {0}
    Product Name: {1}
    Competitor price: {2}
    Intent: {3}
    Price difference: {4}
    Previous price: {5} 
    Updated price: {6}
Thankyou,
Shopify Price Automation Team
    """.format(data_dict["ts"],data_dict["pn"],data_dict["price"],data_dict["intent"],data_dict["amount"],data_dict["cp"],data_dict["up"])
    # form the email message
    msg = "Subject: {0}\n\n{1}".format(subject, body)

    # send the message using the SMTP object, server
    s.sendmail("mayankchauhan2496@gmail.com",data_dict["email"], msg)
    
    # exit from loop in __main__ if email is sent
    print("...Email sent successfully!")
    s.quit()
    return msg