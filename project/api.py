import base64
import hashlib
import random
import re
from datetime import datetime
import mysql.connector
import time
import json
def generate_api_key():
    """
    @return: A hashkey for use to authenticate agains the API.
    """
    return base64.b64encode(hashlib.sha256(str(random.getrandbits(256)).encode('ascii')).hexdigest().encode("utf-8"))

class orders: 
    def __init__(self, order_id, order_status, order_printed, order_name,order_email,order_number,
                 order_total_items,order_comments,pickup_time,
                 order_total,order_items): 
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


def generate_expoview(order_in):
    order_name = f"{order_in[2]} {order_in[3]}"
    d = datetime.strptime(str(order_in[15]), "%H:%M:%S")
    order_split = order_in[8].replace(':',"").split('O27')[1:]
    order_price = round(float(order_in[17]),2)
    items = []
    for x in order_split:
        item={"Item_name":"","Item_price":"","Item_mods":[],"Item_comments":""}
        Item_message = x.split('"name"')[1].split(";")[1]
        item["Item_quantity"] = int(x.split('"qty";')[1].split(";")[0].split('"')[1::2][0])
        item_message_final = Item_message.split('"')[1::2][0]
        item["Item_name"]=item_message_final
        Price_message = x.split('"price";d')[1].split(";")[0]
        item["Item_price"]=Price_message
        Comment_message = x.split(';s7"comment"')[1].split(";")[1]
        if re.findall('CartItemOptionValue',x) != []:
            j = 1
            while j <= len(re.findall('CartItemOptionValues',x)):
                mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                message_finals = mods_message.split('"')[1::2][0]
                mods_quantity = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"qty"')[1]
                message_quantity = int(mods_quantity.split(";")[1][1::2][0])
                mod_print = 0
                while mod_print < message_quantity :
                    item["Item_mods"].append(message_finals)
                    mod_print += 1
                j = j+1
        if Comment_message != 'N' and Comment_message != 's0""':
            comment_message_final = Comment_message.split('"')[1::2][0]
            item["Item_comments"]=comment_message_final
        items.append(item)
    Holla_back = orders(order_in[0],order_in[18],order_in[30],order_name,order_in[4],order_in[5],order_in[9],
        order_in[10],d.strftime('%I:%M %p'),order_price,items)

    return Holla_back

def get_active_orders():
    mydb = mysql.connector.connect(
          host="",
          user="",
          password="",
          database=""
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ti_orders WHERE status_id != 6")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    myresult = mycursor.fetchall()
    lists = []
    for x in myresult:
        lists.append(json.dumps(generate_expoview(x).__dict__))
    return lists

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
