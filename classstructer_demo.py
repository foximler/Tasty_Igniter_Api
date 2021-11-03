


import re
from datetime import datetime
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="",
  user="username",
  password="password",
  database="tasty"  
)



class orders: 
    def __init__(self, order_id, order_name,order_number,
                 order_total_items,order_comments,pickup_time,
                 order_total,order_items): 
        self.order_id = order_id 
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
    items = []
    for x in order_split:
        item={"Item_name":"","Item_price":"","Item_mods":[],"Item_comments":""}
        Item_message = x.split('"name"')[1].split(";")[1]
        item_message_final = Item_message.split('"')[1::2][0]
        item["Item_name"]=item_message_final
        Price_message = x.split('"price";d')[1].split(";")[0]
        item["Item_price"]=Price_message
        Comment_message = x.split(';s7"comment"')[1].split(";")[1]
        if re.findall('CartItemOptionValue',x) != []:
            j = 1
            while j <= len(re.findall('CartItemOptionValues',x)):
                mods_message = x.split('"Igniter\Flame\Cart\CartItemOptionValues')[j].split('"name"')[1]
                j = j+1
                message_finals = mods_message.split('"')[1::2][0]
                item["Item_mods"].append(message_finals)
        if Comment_message != 'N' and Comment_message != 's0""':
            comment_message_final = Comment_message.split('"')[1::2][0]
            item["Item_comment"]=comment_message_final
        items.append(item)
    Holla_back = orders(order_in[0],order_name,order_in[5],order_in[9],
        order_in[10],d.strftime('%I:%M %p'),order_in[17],items)

    return Holla_back

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM ti_orders WHERE status_id = 3")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
myresult = mycursor.fetchall()
lists = []
for x in myresult:
   lists.append(generate_expoview(x))
   print('\n\n')
for obj in lists:
    print( obj.order_id, obj.order_name, obj.order_number,
          obj.order_total_items,obj.order_comments,
          obj.order_pickup_time, obj.order_total,obj.order_items,sep ='-' )
    print("\n\n")




