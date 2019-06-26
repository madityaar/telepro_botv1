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
#from tiket2 import Tiket, Update


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
###########

data2={"keyboard": [["/input_tiket"]],"one_time_keyboard": True}
data4={"keyboard": [["/input_keterangan"],["/input_gambar_sebelum"],["/input_gambar_progres"],["/input_gambar_sesudah"],["/input_lokasi"],["/review_tiket"]],"one_time_keyboard": True,"resize_keyboard": True}
data5={"keyboard": [[{"text":"kirim lokasi","request_location":True}]],"one_time_keyboard": True,"resize_keyboard": True}
data6={"keyboard": [["Edit Data"],["/input_selesai"]],"one_time_keyboard": True}

data_json=json.dumps(data2)
data_json3=json.dumps(data4)
data_json4=json.dumps(data5)
data_json5=json.dumps(data6)

def reply_keyboard(text,chatId,djson):
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, djson)
    get_url(url)
    
def remove_keyboard(text, chatId):
   
    json_remove=json.dumps({"remove_keyboard":True})
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, json_remove)
    get_url(url)
######

class Update():
    def __init__(self, konten=[None,None],chatId=None,tipeKonten=None,offset=0):
        self.konten=konten
        self.chatId=str(chatId)
        self.tipeKonten=str(tipeKonten)
        self.offset=offset
    
    def setKonten(self,updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        try:
            try:
                self.konten[0] = updates["result"][last_update]["message"]["photo"][2]["file_id"]
            except IndexError:
                try:
                    self.konten[0] = updates["result"][last_update]["message"]["photo"][0]["file_id"]
                except IndexError:
                    True
            self.tipeKonten="gambar"
        except KeyError:
            try:
                self.konten[0]=updates["result"][last_update]["message"]["text"]
                self.tipeKonten="text"
            except KeyError:
                try:
                    self.konten[0] = updates["result"][last_update]["message"]["location"]["latitude"]
                    self.konten[1] = updates["result"][last_update]["message"]["location"]["longitude"]
                    self.tipeKonten="location"
                except KeyError:
                    True
        try:
            self.chatId = updates["result"][last_update]["message"]["chat"]["id"]
            self.offset = updates["result"][last_update]["update_id"]
        except IndexError:
            self.chatId=0
            self.offset=0
            

class Tiket():
    def __init__(self, chatId='',noTiket='',keterangan = '',gambarSebelum = '',gambarProgres = '',gambarSesudah = '',latitude='',longitude='', state="none"):
        self.chatId = str(chatId)
        self.noTiket = noTiket
        self.keterangan = keterangan 
        self.gambarSebelum = gambarSebelum
        self.gambarProgres = gambarProgres
        self.gambarSesudah = gambarSesudah
        self.latitude= latitude
        self.longitude= longitude
        self.state= state
    def setChatId(self,chatId):
        self.chatId = chatId
    
    def setNoTiket(self,noTiket):
        self.noTiket = noTiket
        
    def setState(self,state):
        self.state = state
    
    def setKeterangan(self,keterangan):
        self.keterangan = keterangan
    
    def setGambar(self,fileId,nama):
        if(nama=='sebelum'):
            self.gambarSebelum = str(fileId)
        elif(nama=='progres'):
            self.gambarProgres = str(fileId)
        elif(nama=='sesudah'):
            self.gambarSesudah = str(fileId)
    
    def setIsiTiket(self,update):
        print(update.tipeKonten)
        if(update.tipeKonten=="text"):
            if "/input_keterangan" in update.konten[0]:
                self.setKeterangan(update.konten[0].lstrip("/input_keterangan").strip())
                send_message(self.chatId,"Keterangan berhasil terinput")
        elif(update.tipeKonten=="gambar"):
            if "/input_gambar" in update.konten[1]:
                self.setGambar(update.konten[0],update.konten[1].lstrip("/input_gambar").strip())
        elif(update.tipeKonten=="location"):
            print(update.konten)
            self.setLokasi(update.konten[0],update.konten[1])
            send_message(self.chatId,"Lokasi berhasil terinput")
            
    def setLokasi(self,latitude,longitude):
        self.latitude=latitude
        self.longitude=longitude
    
    def print_all(self):
        print("isi tiket")
        print("chat id: "+self.chatId)
        print("noTiket: "+self.noTiket)
        print("keterangan: "+self.keterangan)
        print("fileId Gambar Sebelum: "+self.gambarSebelum)
        print("fileId Gambar Progres: "+self.gambarProgres)
        print("fileId Gambar Sesudah: "+self.gambarSesudah)
        print("latitude: "+str(self.latitude))
        print("longitude: "+str(self.longitude))
        print("state: "+self.state+"\n")
    
    def saveData(self):
        try:
            os.mkdir(self.noTiket)
        except FileExistsError:
            True
        try:
            save_file(self.gambarSebelum,self.chatId,self.noTiket,'sebelum')
            save_file(self.gambarProgres,self.chatId,self.noTiket,'progres')
            save_file(self.gambarSesudah,self.chatId,self.noTiket,'sesudah')
            save_text(self.keterangan,self.chatId,self.noTiket,'keterangan')
            
            loc_lengkap='Latitude: '+str(self.latitude)+' \nLongitude: '+str(self.longitude)+' \nDistance: '+str(calc_distance(self.latitude,self.longitude))
            save_text(loc_lengkap,self.chatId,self.noTiket,'lokasi')
                                
            send_message(self.chatId,"Tiket dengan No. "+self.noTiket+" selesai diinputkan")
            
            self.noTiket = ''
            self.keterangan = '' 
            self.gambarSebelum = ''
            self.gambarProgres = ''
            self.gambarSesudah = ''
            self.latitude= ''
            self.longitude= ''
            self.state= 'none'
        except KeyError:
            send_message(self.chatId, "Data yang diinputkan belum lengkap")
    
    def reviewTiket(self):
        send_message(self.chatId,"Isi tiket")
        send_message(self.chatId,"noTiket: "+self.noTiket)
        status=True
        if(self.keterangan!=""):
            send_message(self.chatId,"keterangan: "+self.keterangan)
        else:
            status=False
        if(self.gambarSebelum!=""):
            send_file(self.chatId,self.gambarSebelum,"Gambar Sebelum")
        else:
            status=False
        if(self.gambarProgres!=""):
            send_file(self.chatId,self.gambarProgres,"Gambar Progres")
        else:
            status=False
        if(self.gambarSesudah!=""):
            send_file(self.chatId,self.gambarSesudah,"Gambar Sesudah")
        else:
            status=False
        if(self.latitude!=""):
            send_location(self.chatId,self.latitude,self.longitude)
        else:
            status=False
        if(status):   
            reply_keyboard("Edit Kembali atau Submit?",self.chatId,data_json5)
        else:
            reply_keyboard("Data belum lengkap. Sila lengkapi kembali",self.chatId,data_json3)

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
    update = Update()
    tiket= defaultdict(dict)
    update.setKonten(get_updates(update.offset))
    last_textchat = (update.konten, update.chatId)
    while True:
        update.setKonten(get_updates(update.offset))
        if(not bool(tiket[update.chatId])):
            tiket[update.chatId]=Tiket(chatId=update.chatId)
        if (update.konten, update.chatId) != last_textchat:
            if(update.chatId!=0):
                if(tiket[update.chatId].state=="none"):
                    if "/input_tiket" in update.konten[0]:
                        tiket[update.chatId].setState("notiket")
                        remove_keyboard("Silahkan input nomor tiket",update.chatId)
                    if(tiket[update.chatId].noTiket!=''):
                        if "/input_keterangan" in update.konten[0]:
                            tiket[update.chatId].setState("keterangan")
                            remove_keyboard("Silahkan input keterangan",update.chatId)
                        elif "/input_gambar_sebelum" in update.konten[0]:
                            tiket[update.chatId].setState("gambar sebelum")
                            remove_keyboard("Silahkan input gambar",update.chatId)
                        elif "/input_gambar_progres" in update.konten[0]:
                            tiket[update.chatId].setState("gambar progres")
                            remove_keyboard("Silahkan input gambar",update.chatId)
                        elif "/input_gambar_sesudah" in update.konten[0]:
                            tiket[update.chatId].setState("gambar sesudah")
                            remove_keyboard("Silahkan input gambar",update.chatId)
                        elif "/input_lokasi" in update.konten[0]:
                            tiket[update.chatId].setState("lokasi")
                            reply_keyboard("Silahkan input lokasi",update.chatId,data_json4)
                        elif "/input_selesai" in update.konten[0]:
                            tiket[update.chatId].saveData()
                        elif "/review_tiket" in update.konten[0]:
                            tiket[update.chatId].reviewTiket()
                        elif "Edit Data" in update.konten[0]:
                            reply_keyboard("Silahkan pilih data yang akan diedit",update.chatId,data_json3)
                        else:
                            send_message(update.chatId,"Silahkan masukkan command terlebih dahulu")
                    elif (tiket[update.chatId].state!="notiket"):
                        reply_keyboard("Silahkan masukkan nomor tiket terlebih dahulu",update.chatId,data_json)
                else:
                    if(tiket[update.chatId].state=="notiket"):
                        if(update.tipeKonten=="text"):
                            tiket[update.chatId].setNoTiket(update.konten[0])
                            reply_keyboard("Nomor Tiket: "+tiket[update.chatId].noTiket+" berhasil diinput",update.chatId,data_json3)
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Nomor tiket harus berupa teks")
                    elif(tiket[update.chatId].state=="keterangan"):
                        if(update.tipeKonten=="text"):
                            tiket[update.chatId].setKeterangan(update.konten[0])
            
                            reply_keyboard("Keterangan berhasil terinput",update.chatId,data_json3)
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Isi keterangan harus berupa teks")
                    elif(tiket[update.chatId].state=="gambar sebelum"):
                        if(update.tipeKonten=="gambar"):
                            tiket[update.chatId].setGambar(update.konten[0],"sebelum")
                            reply_keyboard("Gambar tampak 'sebelum' berhasil terinput",update.chatId,data_json3)
                            #send_message(update.chatId,"Gambar tampak 'sebelum' berhasil terinput")
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Input gambar harus berupa gambar")
                    elif(tiket[update.chatId].state=="gambar progres"):
                        if(update.tipeKonten=="gambar"):
                            tiket[update.chatId].setGambar(update.konten[0],"progres")
                            reply_keyboard("Gambar tampak 'progres' berhasil terinput",update.chatId,data_json3)
                            #send_message(update.chatId,"Gambar tampak 'progres' berhasil terinput")
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Input gambar harus berupa gambar")
                    elif(tiket[update.chatId].state=="gambar sesudah"):
                        if(update.tipeKonten=="gambar"):
                            tiket[update.chatId].setGambar(update.konten[0],"sesudah")
                            reply_keyboard("Gambar tampak 'sesudah' berhasil terinput",update.chatId,data_json3)
                            #send_message(update.chatId,"Gambar tampak 'sesudah' berhasil terinput")
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Input gambar harus berupa gambar")
                    elif(tiket[update.chatId].state=="lokasi"):
                        if(update.tipeKonten=="location"):
                            tiket[update.chatId].setLokasi(update.konten[0],update.konten[1])
                            reply_keyboard("Lokasi berhasil terinput",update.chatId,data_json3)
                            #send_message(update.chatId,"Lokasi berhasil terinput")
                            tiket[update.chatId].setState("none")
                        else:
                            send_message(update.chatId,"Input lokasi harus berupa lokasi")
                try:
                    tiket[update.chatId].print_all()
                except AttributeError:
                    True
            last_textchat = (update.konten, update.chatId)
            
if __name__ == '__main__':
    main()
