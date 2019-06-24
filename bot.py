# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json 
import requests
import urllib.request
import math
from collections import defaultdict
import MySQLdb
import os
from tiket import Tiket, Update


TOKEN = "743391112:AAF60UYlsEhkgb9qU-APK5nqxffhTb9LMbY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
URL_FILE = "https://api.telegram.org/file/bot{}/".format(TOKEN)

try:
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="telegram_bot")        # name of the data base

    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
except:
    print("database not connected")
    
def insert_row(data):
    cur.execute("INSERT INTO tiket (no_tiket,gambar_sebelum,gambar_sesudah,keterangan,latitude,longitude) VALUES ('"+data['no_tiket']+"','"+data['gambar_sebelum']+"','"+data['gambar_sesudah']+"','"+data['keterangan']+"','"+data['latitude'] +"','"+data['longitude']+"')")
    db.commit()
    db.close()

def save_file(fileId, chat_id,noTiket,namaFile):
    url = URL + "getFile?file_id={}".format(fileId)
    js = get_json_from_url(url)
    file_path = js["result"]["file_path"]
    url = URL_FILE + file_path
    testfile = urllib.request.urlretrieve(url,str(noTiket)+"/"+str(noTiket)+"-"+str(namaFile)+".jpg")
    
def save_text(text, chat_id,path, namafile):
    file = open(str(path)+"/"+namafile+".txt","w") 
    file.write(text)
    file.close()
    
def calc_distance(lat1, lon1):
    lat2=-6.229697
    lon2=106.816049
    R = 6371e3  #metres
    o1 = math.radians(lat1)
    o2 = math.radians(lat2)
    delta1 = math.radians(lat2-lat1)
    delta2 = math.radians(lon2-lon1)

    a = math.sin(delta1/2) * math.sin(delta1/2) + math.cos(o1) * math.cos(o2) * math.sin(delta2/2) * math.sin(delta2/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return(d)
def send_message(chatId,text):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chatId)
    get_url(url)
        
def send_file(chatId, file_id,text):
    url = URL + "sendPhoto?photo={}&chat_id={}&caption={}".format(file_id, chatId,text)
    get_url(url)

def send_location(chatId, lat, long):
    url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}".format(chatId, lat, long)
    get_url(url)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset):
    url = URL + "getUpdates?offset={}&limit={}".format(offset+1,1)
    js = get_json_from_url(url)
    return js


def main():
    commands=["/input_tiket","/input_keterangan","/input_selesai","/review_tiket","/input_gambar"]
    update = Update()
    tiket= defaultdict(dict)
    update.setKonten(get_updates(update.offset))
    last_textchat = (update.konten, update.chatId)
    while True:
        update.setKonten(get_updates(update.offset))
        status=False
        if (update.tipeKonten=="location"):
            status=True
        if (update.konten, update.chatId) != last_textchat:
            if(update.tipeKonten=="text"):
                for command in commands:      
                    if command in update.konten[0]:
                        status=True
                        break
            try:
                if status: 
                    print(update.konten[0],update.tipeKonten)
                    if "/input_tiket" in update.konten[0]:
                        if (update.chatId!=0):
                            tiket[update.chatId]=Tiket(noTiket=update.konten[0].lstrip("/input_tiket").strip(),chatId=update.chatId)
                            send_message(update.chatId,"Input tiket dengan No. "+tiket[update.chatId].noTiket+" berhasil didaftarkan")
                    elif "/input_selesai" in update.konten[0]:
                        tiket[update.chatId].saveData()
                        send_message(update.chatId,"Tiket dengan No. "+tiket[update.chatId].noTiket+" selesai diinputkan")
                        tiket.pop(update.chatId)
                    elif "/review_tiket" in update.konten[0]:
                        tiket[update.chatId].reviewTiket()
                else:
                    send_message(update.chatId,"Command Input Harus Sesuai")
            
                if(tiket[update.chatId].noTiket!=""):
                    tiket[update.chatId].setIsiTiket(update)
            except :
                send_message(update.chatId,"Anda belum menginputkan nomor tiket")
            try:
                tiket[update.chatId].print_all()
            except:
                True
            last_textchat = (update.konten, update.chatId)
if __name__ == '__main__':
    main()
