#!/usr/bin/python
#config: utf-8

import requests
import subprocess
import os
from bs4 import BeautifulSoup
import sqlite3
import smtplib
from email import message
from dotenv import load_dotenv

# load envfile
load_dotenv()

def main():
    #db
    dbname = 'STOCK.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    mail_on = 0
    item_info = []
    table= "ITEMS"

    # local dev enviroment
    # filename = ''
    # with open(filename+'.html') as myfile:          
    #     soup = BeautifulSoup(myfile, 'html.parser')
    
    res = requests.get(os.environ['URL'])
    soup = BeautifulSoup(res.text, 'html.parser')

    # find items from DOM
    elems = soup.find_all(class_="item part")

    # search soldout and checking data
    for elem in elems:

        #find sold out
        if elem.find(class_="soldout_cover"):

            #get item_id from url
            url = os.path.split(elem.select_one("div.itemImg a").get("href"))
            item_id = url[1]

            #search DB 
            sql = f"select item_id from {table} where item_id = ?"
            data = (item_id,)
            cur.execute(sql, data)
            db_item_list = cur.fetchall()

            if db_item_list==[]:
                print("insert")
                #get item name
                item_name = elem.find('h2').text

                #insert 
                sql = f"insert into {table} (item_name, item_id) values (?, ?)"
                data = (item_name, item_id)
                cur.execute(sql, data)
                conn.commit()

                #stock sold out item name
                item_info.append(item_name)

                #set mail flag
                if mail_on == 0:
                    mail_on = 1

        else:
            #get stock item
            url = os.path.split(elem.select_one("div.itemImg a").get("href"))
            item_id = url[1]

            #delete data. adding item from empty .
            sql = f"delete from {table} where item_id = ?"
            data = (item_id,)
            cur.execute(sql, data)
            conn.commit()

    # send mail flag
    if mail_on :
        send_mail(item_info)
        # flag off
        mail_on = 0

    #db close
    cur.close()
    conn.close()

def send_mail(item_info):
 
    smtp_host = os.environ['SMTP_HOST']
    smtp_port = os.environ['SMTP_PORT']
    smtp_account_id = os.environ['SMTP_ACCOUNT']
    mail_top_message = os.environ['MAIL_TOP_MESSAGE']
    mail_subject = os.environ['MAIL_SUBJECT']

    mail_content = '\n'.join(item_info)
    mail_content = mail_top_message + "\n\n" + mail_content

    from_mail = os.environ['FROM_MAIL']
    to_mail = os.environ['TO_MAIL']

    msg = message.EmailMessage()
    msg.set_content(mail_content)
    msg['Subject'] = mail_subject
    msg['From'] = from_mail
    msg['To'] = to_mail
    
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    server.login(smtp_account_id, smtp_account_pass)
    result = server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    main()