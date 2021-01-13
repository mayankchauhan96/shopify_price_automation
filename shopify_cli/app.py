from flask import Flask, request, jsonify, send_from_directory, render_template, url_for
from flask_cors import CORS
import time
from datetime import datetime
from backend import tracker, helper
from apscheduler.scheduler import Scheduler
import atexit
import requests
from flaskext.mysql import MySQL
import re
import json

app = Flask(__name__)
CORS(app)

#mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'mayank'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'shopify'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
        
conn = mysql.connect()
cursor =conn.cursor()
res_data={}
response_data=[]


@app.route('/access', methods = ['POST'])
def accessToken():
    data1 = request.get_json()
    token = data1["token"]
    shop = data1["shop"]
    shop = shop.split(".myshopify.com")
    shop = shop[0]

    if cursor.execute("(SELECT id FROM Mycredential WHERE shop=%s)",shop) != 0:
        cursor.execute("UPDATE Mycredential SET token=%s WHERE shop=%s;",(token,shop))
        conn.commit()
    else:
        cursor.execute("INSERT INTO Mycredential( token, shop) VALUES (%s, %s)", (token, shop))
        conn.commit()

    return 'success'


@app.route('/result', methods = ['POST'])
def result():
    global res_data
    data_dict = request.get_json()
    print(data_dict)
    data_dict["intent"] = data_dict["intent"][0]
    data_dict["user_agent"] = "google chrome"
    time_diff = int(data_dict["time"])
    shop= data_dict["shop"]
    shop = re.findall("shop=\w+", shop)
    shop = shop[0].split("shop=")
    shop = shop[1]
    cursor.execute("(SELECT token FROM Mycredential WHERE shop=%s);",shop)
    token = cursor.fetchall()
    token = token[0][0]
    is_active = "1"

    #db_prod
    prod_id = data_dict["prodid"]
    prod_id = prod_id[0]
    prod_id = prod_id.split("gid://shopify/Product/")
    prod_id = int(prod_id[1])
    print(prod_id)
    data_dict["prodid"] = prod_id
    
    if cursor.execute("(SELECT shp_prod_id FROM ActiveProducts WHERE shp_prod_id=%s)",prod_id) == 0:
        cursor.execute("INSERT INTO ActiveProducts( shp_prod_id, shop) VALUES (%s, %s)", (prod_id, shop))
        conn.commit()
    #active_status
    cursor.execute("UPDATE ActiveProducts SET active_status=%s WHERE shp_prod_id=%s;",(is_active,prod_id))
    conn.commit()
    iters = 0  
    while True:
        iters += 1
        print("\nCheck #", iters, "on:", datetime.today())
        # check if the price has changed
        try:
            response = tracker.checkPrice(data_dict,shop,token)
        except Exception as e:
            if e != "SystemExit":
                print("\nSorry! Price tracking attempt failed.")

        #active_status_check
        print("active? ",cursor.execute("(SELECT active_status FROM ActiveProducts WHERE shp_prod_id=%s)",prod_id))
        if cursor.execute("(SELECT active_status FROM ActiveProducts WHERE shp_prod_id=%s)",prod_id) == 0:
            print("Exiting...")
            break

        # print the frequency of price checks
        print("Price will be checked every " + helper.getTime(time_diff))
        print("Interrupt keyboard to stop. (Ctrl+Z / Ctrl+C)")
        try:
            email = response[7]
            response.insert(0,iters)
            response_data.append(response)
            logs = json.dumps(response_data)
            cursor.execute("UPDATE ActiveProducts SET logs=%s WHERE shp_prod_id=%s;",(logs,prod_id))
            print("logs updated")
            cursor.execute("UPDATE Mycredential SET email=%s WHERE shop=%s;",(email,shop))
            conn.commit()
        except:
            pass
        
        time.sleep(time_diff)



@app.route('/data', methods = ['POST'])
def getData():
    data = request.get_json()
    shop= data["shop"]
    shop = re.findall("shop=\w+", shop)
    shop = shop[0].split("shop=")
    shop = shop[1]
    # prodid= data["prodid"]

    cursor.execute("SELECT logs FROM ActiveProducts WHERE shop=%s;",shop)
    tuples  = cursor.fetchall()
    li= []
    # print(li)
    # li = li[0][0]
    # li = json.loads(li)
    for tup in tuples:
        tmp = json.loads(tup[0])
        for i in tmp:
            li.append(i)
    # print(li)

    res_data["data"] = li
    return res_data

@app.route('/terminate', methods = ['POST'])
def terminate():
    data = request.get_json()
    prod_id= data["prodid"]
    prod_id = prod_id[0]
    prod_id = prod_id.split("gid://shopify/Product/")
    prod_id = int(prod_id[1])
    print(prod_id)
    data_dict = request.get_json()
    is_active= "0"
    cursor.execute("UPDATE ActiveProducts SET active_status=%s WHERE shp_prod_id=%s;",(is_active,prod_id))
    conn.commit()
    print("success")
    return "success"

@app.route('/isactive', methods = ['POST'])
def active():
    final_lst=[]
    response_data={}
    data = request.get_json()
    shop= data["shop"]
    shop = re.findall("shop=\w+", shop)
    shop = shop[0].split("shop=")
    shop = shop[1]
    is_active= "1"
    cursor.execute("SELECT shp_prod_id,logs FROM ActiveProducts WHERE shop=%s AND active_status=%s;",(shop,is_active))
    li = cursor.fetchall()
    for prod in li:
        prod_lst=[]
        prod_lst.append(prod[0])
        lst = json.loads(prod[1])
        prod_lst.append(lst[0][4])
        prod_lst.append(lst[0][2])
        prod_lst.append(lst[0][5])
        final_lst.append(prod_lst)
    response_data["data"] = final_lst
    print(response_data)

    return response_data

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')