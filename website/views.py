from flask import Blueprint, render_template, request, flash, jsonify,redirect
from flask_login import login_required, current_user




import json
#from flask_mail import Mail, Message
views = Blueprint('views', __name__)
import sys
import logging
import requests
from os import path
from flask import Flask, request, Response
#from flask_ngrok import run_with_ngrok
from alice_blue import *
import json
import math
from flask_sqlalchemy import SQLAlchemy
import datetime
import pypyodbc
import ast
#access_token = AliceBlue.login_and_get_access_token(username='AB169563', password='sharu12311', twoFA='a',  api_secret='K0VSBC2Y6NNZ6QFI9BVQK4VIYR4UW07DX60BV2RFESA6ECRX1C581UWQFM4UIHBG')
#alice = AliceBlue(username='AB169563', password='sharu12311', access_token=access_token)
headers = {
'authorization': "qt9fD7m5T2O68KChvUiGPr4s0HElZoeWanSVN1kzRbc3wgFpXyMyZn4g1Px8m9AoUaHdb62YwvBphf5N",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
import os
from flask import Flask, render_template, request, flash, redirect, url_for

connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:mydbpop.database.windows.net,1433;Database=mydbpop;uid=pop;pwd=yahoo@786;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
#connection = pypyodbc.connect('Driver={SQL Server};Server=.;Database=master;uid=sa;pwd=test')


cursor = connection.cursor()    
url = "https://www.fast2sms.com/dev/bulk"
logging.basicConfig(level=logging.DEBUG)

@views.route("/book", methods=['GET','POST'])
def logic():
    
    #json_data = alice.get_balance() # get balance / margin limits
    #margin_avaiable = json_data['data']['cash_positions'][1]['available']['cashmarginavailable']
    margin_avaiable = 100000
    output = str(request.get_data(as_text=True));
    data = ast.literal_eval(output)
    print(data)
    #order = request.get_data();
    #x = order.split()
    #GSM 888 123 long exit
    if data['status'] == 'entry':
        sql ="select COUNT(*) from stocksks where stock_name = ? and status= ? and valid=1"
        adr = (data['stock_name'], 'entry')
        op = cursor.execute(sql,adr)
        #op = cursor.execute(sql)
        row1= cursor.fetchone()[0]
        print('row1')
        print(row1)
        if row1 == 0:
            print('inserting data')
            qty = int(float(margin_avaiable * 0.02)) / int(float(data['price']))
            print('qty',math.floor(qty))
            valid = '1'
            oms_order_id='123'
            currentdate = datetime.datetime.now()
            print(currentdate)
            cursor.execute("INSERT INTO stocksks(stock_name, price, st, mode, status,valid,orderid,dat) VALUES(?,?,?,?,?,?,?,?) ", (data['stock_name'],data['price'],data['st'],data['mode'],data['status'],valid,oms_order_id,currentdate))   
            connection.commit()
        
        
        '''if qty >0 and data['mode']=='long':
            response = alice.place_order(transaction_type = TransactionType.Buy,
                         instrument = alice.get_instrument_by_symbol('NSE', 'INFY'),
                         quantity = qty,
                         order_type = OrderType.StopLossMarket,
                         product_type = ProductType.Intraday,
                         #price = 0.0,
                         #trigger_price = 8.0,
                         stop_loss = data['st'],
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)
           
        if qty >0 and data['mode']=='short':
            response = alice.place_order(transaction_type = TransactionType.Sell,
                         instrument = alice.get_instrument_by_symbol('NSE', 'INFY'),
                         quantity = qty,
                         order_type = OrderType.StopLossMarket,
                         product_type = ProductType.Intraday,
                         #price = 0.0,
                         #trigger_price = 8.0,
                         stop_loss = data['st'],
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)     
            
        if((response["status"]=="success") and (response["message"]=="Order placed successfully")):
            oms_order_id = response["data"]["oms_order_id"]
            cursor.execute("INSERT INTO stocksks(stock_name, price, st, mode, status,valid,orderid,dat) VALUES(?,?,?,?,?,?,?,?) ", (data['stock_name'],data['price'],data['st'],data['mode'],data['status'],valid,oms_order_id,currentdate))
            connection.commit()
            msg=data['stock_name']+' '+data['mode'] + ' at price '+ data['price']
            payload = "sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers=8308831893"
            response1 = requests.request("POST", url, data=payload, headers=headers)
            '''

    if data['status'] == 'exit':
        print('stock name')
        print(data['stock_name'])
        #order = request.get_data();
        #x = order.split()
        #change the GSM valoe to x[0] stock name
        #sql ="""select orderid from stocksks where stock_name = %s and status= %s""" %(data['stock_name'],"'entry'")
        
        
        sql ="select COUNT(*) from stocksks where stock_name = ? and status= ? and valid=1"
        adr = (data['stock_name'], 'entry')
        op = cursor.execute(sql,adr)
        #op = cursor.execute(sql)
        row2= cursor.fetchone()[0]
        print('row2')
        print(row2)
        
        if row2 > 0:
            print("closing trade")
            sql ="select orderid from stocksks where stock_name = ? and status= ? and valid=1"
            adr = (data['stock_name'], 'entry')
            op = cursor.execute(sql,adr)
            row3 = cursor.fetchone()[0]
            print(row3)
            currentdate1 = datetime.datetime.now()
            
            #response = alice.cancel_order(oid) #Cancel an open order     
           # if((response["status"]=="success")):
            if(("success"=="success")):
                cursor.execute("INSERT INTO stocksks (stock_name, price, st, mode, status,orderid,valid,dat) VALUES (?,?,?,?,?,?,?,?)",(data['stock_name'],data['price'],data['st'],data['mode'],data['status'],row3,0,currentdate1))
                connection.commit()
                updatesql = """update stocksks set valid= %s where orderid= %s""" %(0,row3)
                cursor.execute(updatesql)
                connection.commit()
                #msg=data['stock_name']+' '+data['mode'] + ' at price '+ data['price']
                #payload = "sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers=8308831893"
                #response1 = requests.request("POST", url, data=payload, headers=headers)

    return "hello chetan"