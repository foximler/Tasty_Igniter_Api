import base64
import hashlib
import random
import re
from datetime import datetime
import mysql.connector
import time
import json
from phpserialize import *


def generate_api_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    return base64.b64encode(hashlib.sha256(str(random.getrandbits(256)).encode('ascii')).hexdigest().encode("utf-8"))

class orders: 
    def __init__(self, order_id, order_status, order_printed, order_name,order_email,order_number,
                 order_total_items,order_comments,pickup_time,
                 order_total,order_items, order_type, order_city, order_address, order_state): 
        self.order_id = order_id 
        self.order_status = order_status
        self.order_printed = order_printed
        self.order_email = order_email
        self.order_name = order_name
        self.order_number = order_number
        self.order_total_items = order_total_items
        self.order_comments = order_comments
        self.order_pickup_time = pickup_time
        self.order_total = order_total
        self.order_items = order_items
        self.order_type = order_type
        self.order_address = order_address
        self.order_city = order_city
        self.order_state = order_state

def generate_expoview(order_in):
    items_list = []
    order_type = order_in[12]
    if (order_type == "delivery" ):
        info  = get_order_address(order_in[7])
        order_city = info['city']
        order_address = info['address']
        order_state = info['state']
    else:
        order_city = ""
        order_address = ""
        order_state = ""
    item_object =  loads(order_in[8].encode(), object_hook=phpobject)
    order_name = f"{order_in[2]} {order_in[3]}"
    order_price = round(float(order_in[17]),2)
    d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
    item_list = []
    for items in item_object._asdict()[b'\x00*\x00items'].items():
        item={"Item_name":"","Item_price":"","Item_mods":[],"Item_comments":""}
        item["Item_name"] = items[1]._asdict()[b'name'].decode('utf-8')
        item["Item_price"] = items[1]._asdict()[b'price']
        item_mods = items[1]._asdict()[b'options']._asdict()[b'\x00*\x00items'].items()
        if items[1]._asdict()[b'comment'] is not None:
            item["Item_comments"] = items[1]._asdict()[b'comment'].decode('utf-8')
        mods = []
        if bool(item_mods):
            for mod in item_mods:
                mods_list = mod[1]._asdict()[b'values']._asdict()[b'\x00*\x00items'].items()
                for z in mods_list:
                    i = 1
                    while i <= z[1]._asdict()[b'qty']:
                        mods.append(z[1]._asdict()[b'name'].decode('utf-8'))
                        i += 1
            item["Item_mods"] = mods
        i=1
        while i <= int(items[1]._asdict()[b'qty']): 
            items_list.append(item)
            i += 1
    Holla_back = orders(order_in[0],order_in[18],order_in[30],order_name,order_in[4],order_in[5],order_in[9],order_in[10],d.strftime('%I:%M %p'),order_price,items_list,order_type,order_city,order_address,order_state)
    print(Holla_back)
    return Holla_back

def get_active_orders():
    mydb = mysql.connector.connect(
           host="",
          user="",
          password="",
          database=""
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ti_orders WHERE status_id != 5")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    myresult = mycursor.fetchall()
    lists = []
    for x in myresult:
        lists.append(json.dumps(generate_expoview(x).__dict__))
    return lists

def get_order_address(address):
    mydb = mysql.connector.connect(
           host="",
          user="",
          password="",
          database=""
    )

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM ti_addresses WHERE address_id = {int(address)}")
    myresult = mycursor.fetchall()
    location = {
    'address': f"{myresult[0][2]} - {myresult[0][3]}",
    'city': f"{myresult[0][4]}",
    'state': f"{myresult[0][5]}",
    }
    return location


def update_order_status(order_id,order_status):
    mydb = mysql.connector.connect(
           host="",
          user="",
          password="",
          database=""
    )
    mycursor = mydb.cursor()
    sql= f"UPDATE ti_orders SET status_id = {int(order_status)} WHERE order_id = {int(order_id)}"
    mycursor.execute(sql)
    mydb.commit()
def update_print_status(order_id, print_status):
    mydb = mysql.connector.connect(
           host="",
          user="",
          password="",
          database=""
    )
    mycursor = mydb.cursor()    
    sql= f"UPDATE ti_orders SET order_printed = {int(print_status)} WHERE order_id = {int(order_id)}"
    mycursor.execute(sql)
    mydb.commit()
