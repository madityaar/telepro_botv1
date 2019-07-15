# -*- coding: utf-8 -*-
import json 
import requests
import urllib.request
import math
from collections import defaultdict
import MySQLdb
import os
import datetime
import glob
import time
#from tiket2 import Tiket, Update


TOKEN = "743391112:AAF60UYlsEhkgb9qU-APK5nqxffhTb9LMbY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
URL_FILE = "https://api.telegram.org/file/bot{}/".format(TOKEN)
max_dist=50
max_keterangan=200
max_tiket=10

###########
try:
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="dtest")        # name of the data base
    
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
    print("database connected")
except:
    print("database not connected")
    
def insert_row(data):
    cur.execute("INSERT INTO tiket (no_tiket,gambar_sebelum,gambar_sesudah,keterangan,latitude,longitude) VALUES ('{}','{}','{}','{}','{}','{}')".format(data['no_tiket'],data['gambar_sebelum'],data['gambar_sesudah'],data['keterangan'],data['latitude'],data['longitude']))
    db.commit()

def isApproved(idchat):
    sql="select isApproved from UserApproval where idUserApproval='"+str(idchat)+"'"
    cur.execute(sql)
    records = cur.fetchall()
    return records

def insert_row_user(data):
    sql=""
    cur.execute(sql)
    db.commit()
    db.close()

def update_row_odp(tiket,dist):
    sql="update mytable set photo_before='{}-a', photo_process='{}-b', photo_after='{}-c', longitude_u={}, latitude_u={}, distance={}, updated_by={}, updated_date=SYSDATE(),keterangan='{}' where ticket_id='{}'".format(tiket.noTiket,tiket.noTiket,tiket.noTiket,str(tiket.longitude),str(tiket.latitude),str(dist),tiket.chatId,tiket.keterangan,tiket.noTiket)
    cur.execute(sql)
    db.commit()

def daftar(chatid,array):
    sql="INSERT INTO userapproval VALUES ('{}','{}','{}','{}',1)".format(str(chatid),array[0],array[1].upper(),array[2].upper())
    cur.execute(sql)
    db.commit()

def select_ticket(ticket):
    sql="select ticket_id,ODP, longitude, latitude from mytable where ticket_id='{}'".format(str(ticket))
    cur.execute(sql)
    empty=()
    records = cur.fetchall()
    if(records==empty):
        return None
    else:
        return records[0]
###########




def reply_keyboard(text,chatId,djson):
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, djson)
    get_url(url)
    
def remove_keyboard(text, chatId):
    json_remove=json.dumps({"remove_keyboard":True})
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, json_remove)
    get_url(url)
######
data1={"keyboard": [["/input_tiket"]],"one_time_keyboard": True}
data3={"keyboard": [[{"text":"kirim lokasi","request_location":True}],["/cancel"]],"one_time_keyboard": True,"resize_keyboard": True}
data4={"keyboard": [["Edit Data"],["/input_selesai"]],"one_time_keyboard": True}
data5={"keyboard": [["/cancel"]],"one_time_keyboard": True}
json_input_tiket=json.dumps(data1)
json_req_location=json.dumps(data3)
json_aft_review=json.dumps(data4)
json_cancel=json.dumps(data5)
    
    
class Keyboard():
    def __init__(self):
        data2={"keyboard": [["/input_keterangan"],["/input_gambar_ODC-RK-MSAN"],["/input_gambar_ODP-RP"],["/input_gambar_saluran_penanggal"],["/input_gambar_tiang"],["/input_lokasi"],["/review_tiket"],["/kirim_contoh"]],"one_time_keyboard": True,"resize_keyboard": True}
        #data2={"keyboard": [["/input_keterangan"],["/input_gambar_ODP-RP"],["/input_gambar_saluran_penanggal"],["/input_gambar_tiang"],["/input_lokasi"],["/review_tiket"],["/kirim_contoh"]],"one_time_keyboard": True,"resize_keyboard": True}
        json_all_comm=json.dumps(data2)
        data6={"keyboard": [["ODC A"],["ODC B"],["/cancel"]],"one_time_keyboard": True}
        data7={"keyboard": [["ODP A"],["ODP B"],["ODP C"],["/cancel"]],"one_time_keyboard": True}
        data8={"keyboard": [["sebelum"],["progres"],["sesudah"],["/cancel"]],"one_time_keyboard": True}
        json_odc_lv2=json.dumps(data6)
        json_odp_lv2=json.dumps(data7)
        json_bfraft=json.dumps(data8)
        self.json_lvl_1=json_all_comm
        self.json_ODC_lvl_2=json_odc_lv2
        self.json_ODP_lvl_2=json_odp_lv2
        self.json_ODCA_lvl_3=json_bfraft
        self.json_ODCB_lvl_3=json_bfraft
        self.json_ODPA_lvl_3=json_bfraft
        self.json_ODPB_lvl_3=json_bfraft
        self.json_ODPC_lvl_3=json_bfraft
        self.json_tiang_lvl_2=json_bfraft
        self.json_saluran_lvl_2=json_bfraft
    
    def cekKeyboardGambar(self):
        a= json.dumps({"keyboard": [["/cancel"]], "one_time_keyboard": True})
        if(self.json_ODCA_lvl_3==a):
            self.json_ODC_lvl_2=self.json_ODC_lvl_2.replace('["ODC A"], ','')
        if(self.json_ODCB_lvl_3==a):
            self.json_ODC_lvl_2=self.json_ODC_lvl_2.replace('["ODC B"], ','')
        if(self.json_ODPA_lvl_3==a):
            self.json_ODP_lvl_2=self.json_ODP_lvl_2.replace('["ODP A"], ','')
        if(self.json_ODPB_lvl_3==a):
            self.json_ODP_lvl_2=self.json_ODP_lvl_2.replace('["ODP B"], ','')
        if(self.json_ODPC_lvl_3==a):
            self.json_ODP_lvl_2=self.json_ODP_lvl_2.replace('["ODP C"], ','')
        if(self.json_saluran_lvl_2==a):
            self.json_lvl_1=self.json_lvl_1.replace('["/input_gambar_saluran_penanggal"], ','')
        if(self.json_tiang_lvl_2==a):
            self.json_lvl_1=self.json_lvl_1.replace('["/input_gambar_tiang"], ','')
        if(self.json_ODC_lvl_2==a):
            self.json_lvl_1=self.json_lvl_1.replace('["/input_gambar_ODC-RK-MSAN"], ','')
        if(self.json_ODP_lvl_2==a):
            self.json_lvl_1=self.json_lvl_1.replace('["/input_gambar_ODP-RP"], ','')
    
    def resetKeyboard(self):
        data2={"keyboard": [["/input_keterangan"],["/input_gambar_ODP-RP"],["/input_gambar_saluran_penanggal"],["/input_gambar_tiang"],["/input_lokasi"],["/review_tiket"],["/kirim_contoh"]],"one_time_keyboard": True,"resize_keyboard": True}
        json_all_comm=json.dumps(data2)
        data6={"keyboard": [["ODC A"],["ODC B"],["/cancel"]],"one_time_keyboard": True}
        data7={"keyboard": [["ODP A"],["ODP B"],["ODP C"],["/cancel"]],"one_time_keyboard": True}
        data8={"keyboard": [["sebelum"],["progres"],["sesudah"],["/cancel"]],"one_time_keyboard": True}
        json_odc_lv2=json.dumps(data6)
        json_odp_lv2=json.dumps(data7)
        json_bfraft=json.dumps(data8)
        self.json_lvl_1=json_all_comm
        self.json_ODC_lvl_2=json_odc_lv2
        self.json_ODP_lvl_2=json_odp_lv2
        self.json_ODCA_lvl_3=json_bfraft
        self.json_ODCB_lvl_3=json_bfraft
        self.json_ODPA_lvl_3=json_bfraft
        self.json_ODPB_lvl_3=json_bfraft
        self.json_ODPC_lvl_3=json_bfraft
        self.json_tiang_lvl_2=json_bfraft
        self.json_saluran_lvl_2=json_bfraft
    

class Update():
    def __init__(self, konten=[None,None],chatId=None,tipeKonten=None,offset=0):
        self.konten=konten
        self.chatId=str(chatId)
        self.tipeKonten=str(tipeKonten)
        self.offset=offset
    
    def setKonten(self,updates):
        self.konten[0]=None
        self.konten[1]=None
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        ###tahap identifikasi isi pesan
        try:
            ###identifikasi jika isi berupa gambar###
            try:
                self.konten[0] = updates["result"][last_update]["message"]["photo"][2]["file_id"]
                self.tipeKonten="gambar"
            except IndexError:
                try:
                    self.konten[0] = updates["result"][last_update]["message"]["photo"][0]["file_id"]
                    self.tipeKonten="gambar"
                except IndexError:
                    True
            ###identifikasi jika isi berupa gambar###
        except KeyError:
            ###identifikasi jika isi berupa teks###
            try:
                self.konten[0]=updates["result"][last_update]["message"]["text"]
                self.tipeKonten="text"
                self.konten[0] = self.konten[0].replace('"', '|')
                self.konten[0] = self.konten[0].replace("'", "|")
            ###identifikasi jika isi berupa teks###
            except KeyError:
                ###identifikasi jika isi berupa lokasi###
                try:
                    self.konten[0] = updates["result"][last_update]["message"]["location"]["latitude"]
                    self.konten[1] = updates["result"][last_update]["message"]["location"]["longitude"]
                    self.tipeKonten="location"
                except KeyError:
                    True
                ###identifikasi jika isi berupa lokasi###
            ###mengupdate chatid pada update
        try:
            self.chatId = updates["result"][last_update]["message"]["chat"]["id"]
            self.offset = updates["result"][last_update]["update_id"] 
        except (IndexError):
            self.chatId=0
            self.offset=0
        except KeyError:
            ###menghandle edited message agar bot tidak crash
            self.offset = updates["result"][last_update]["update_id"]
            
    def cek_command(self,tiket):
        if "/input_tiket" in self.konten[0]:
            tiket[self.chatId].setState("notiket")
            reply_keyboard("Silakan input nomor tiket",self.chatId,json_cancel)
        if(tiket[self.chatId].noTiket!=''):
            if "/input_keterangan" in self.konten[0]:
                tiket[self.chatId].setState("keterangan")
                reply_keyboard("Silakan input keterangan",self.chatId,json_cancel)
            elif "/input_gambar_ODC-RK-MSAN" in self.konten[0]:
                tiket[self.chatId].setState("gambar ODC")
                reply_keyboard("Pilih ODC",self.chatId,tiket[self.chatId].keyboard.json_ODC_lvl_2)
            elif "/input_gambar_ODP-RP" in self.konten[0]:
                tiket[self.chatId].setState("gambar ODP")
                reply_keyboard("Pilih ODP",self.chatId,tiket[self.chatId].keyboard.json_ODP_lvl_2)
            elif "/input_gambar_saluran_penanggal" in self.konten[0]:
                tiket[self.chatId].setState("gambar saluran")
                reply_keyboard("Silakan pilih kondisi ",self.chatId,tiket[self.chatId].keyboard.json_saluran_lvl_2)
            elif "/input_gambar_tiang" in self.konten[0]:
                tiket[self.chatId].setState("gambar tiang")
                reply_keyboard("Silakan pilih kondisi ",self.chatId,tiket[self.chatId].keyboard.json_tiang_lvl_2)
            elif "/input_lokasi" in self.konten[0]:
                tiket[self.chatId].setState("lokasi")
                reply_keyboard("Silakan input lokasi",self.chatId,json_req_location)
            elif "/input_selesai" in self.konten[0]:
                tiket[self.chatId].saveData()
            elif "/review_tiket" in self.konten[0]:
                tiket[self.chatId].reviewTiket()
            elif "/cancel" in self.konten[0]:
                tiket[self.chatId].setState('none')
            elif "/kirim_contoh" in self.konten[0]:
                try:
                    tiket[self.chatId].kirimContoh()
                except:
                    print('error sending image')
            elif "Edit Data" in self.konten[0]:
                tiket[self.chatId].keyboard.resetKeyboard()
                reply_keyboard("Silakan pilih data yang akan diedit",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                
            else:
                tiket[self.chatId].send_message("Silakan masukkan perintah yang sesuai")
        elif (tiket[self.chatId].state!="notiket"):
            reply_keyboard("Silakan masukkan nomor tiket terlebih dahulu",self.chatId,json_input_tiket)
        return tiket
            
    def cek_konten_sesuai_state(self,tiket):
        if(self.konten[0]=="/cancel"):
            string_rep="Input {} dibatalkan".format(tiket[self.chatId].state)
            tiket[self.chatId].setState("none")
            if(tiket[self.chatId].state=="notiket"):
                reply_keyboard(string_rep,self.chatId,json_input_tiket)
            else:
                reply_keyboard(string_rep,self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
        elif(tiket[self.chatId].state=="notiket"):
            if(self.tipeKonten=="text"):
                if(len(self.konten[0])==max_tiket):
                    records=None
                    records=select_ticket(self.konten[0])
                    if(bool(records)):
                        tiket[self.chatId].setNoTiket(self.konten[0])
                        tiket[self.chatId].setODP(records)
                        reply_keyboard("Nomor Tiket: {} berhasil diinput".format(tiket[self.chatId].noTiket),self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                        tiket[self.chatId].setState("none")
                    else:
                        tiket[self.chatId].send_message("Tiket yang diinputkan tidak terdaftar. Mohon masukkan kembali")
                else:
                    tiket[self.chatId].send_message("Tiket harus terdiri 10 karakter")
            else:
                tiket[self.chatId].send_message("Nomor tiket harus berupa teks")
        elif(tiket[self.chatId].state=="keterangan"):
            if(self.tipeKonten=="text"):
                if(len(self.konten[0])<=max_keterangan):
                    tiket[self.chatId].setKeterangan(self.konten[0])
                    reply_keyboard("Keterangan berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                    tiket[self.chatId].setState("none")
                else:
                    tiket[self.chatId].send_message("Keterangan tidak boleh lebih dari 30 karakter")
            else:
                tiket[self.chatId].send_message("Isi keterangan harus berupa teks")
#### MENU TINGKAT 2 ODC
        elif(tiket[self.chatId].state=="gambar ODC"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="ODC A"):
                    tiket[self.chatId].setState("gambar ODC A")   
                    reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODCA_lvl_3)
                elif(self.konten[0]=="ODC B"):
                    tiket[self.chatId].setState("gambar ODC B")
                    reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODCB_lvl_3)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 ODC
        elif(tiket[self.chatId].state=="gambar ODC A"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODC A sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODC A progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODC A sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
           
#### MENU TINGKAT 4 ODC       
        elif(tiket[self.chatId].state=="gambar ODC A sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC A sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODC A progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC A progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODC A sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC A sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        
#### Menu TINGKAT 3 ODC B
        elif(tiket[self.chatId].state=="gambar ODC B"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODC B sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODC B progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODC B sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 4 ODC B
        elif(tiket[self.chatId].state=="gambar ODC B sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC B sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODC B progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC B progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODC B sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODC B sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        
#### MENU TINGKAT 2 ODP
        elif(tiket[self.chatId].state=="gambar ODP"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="ODP A"):
                    tiket[self.chatId].setState("gambar ODP A")   
                    reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPA_lvl_3)
                elif(self.konten[0]=="ODP B"):
                    tiket[self.chatId].setState("gambar ODP B")
                    reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPB_lvl_3)
                elif(self.konten[0]=="ODP C"):
                    tiket[self.chatId].setState("gambar ODP C")
                    reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPC_lvl_3)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 ODP
        elif(tiket[self.chatId].state=="gambar ODP A"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP A sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP A progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP A sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
                
        elif(tiket[self.chatId].state=="gambar ODP B"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP B sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP B progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP B sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
                
        elif(tiket[self.chatId].state=="gambar ODP C"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP C sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP C progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP C sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 4
        elif(tiket[self.chatId].state=="gambar ODP A sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP A sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP A progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP A progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP A sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP A sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### Menu Tingkat 4 ODP B
        elif(tiket[self.chatId].state=="gambar ODP B sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP B sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP B progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP B progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP B sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP B sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### Menu Tingkat 4 ODP C
        elif(tiket[self.chatId].state=="gambar ODP C sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP C sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP C progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP C progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP C sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar ODP C sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### MENU TINGKAT 2 SALURAN        
        elif(tiket[self.chatId].state=="gambar saluran"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar saluran sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar saluran progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar saluran sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 SALURAN
        elif(tiket[self.chatId].state=="gambar saluran sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar saluran sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar saluran progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar saluran progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar saluran sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar saluran sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### MENU TINGKAT 2 TIANG
        elif(tiket[self.chatId].state=="gambar tiang"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar tiang sebelum")    
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar tiang progres")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar tiang sesudah")
                    reply_keyboard("Silakan input gambar",self.chatId,json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 TIANG
        elif(tiket[self.chatId].state=="gambar tiang sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar tiang sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar tiang progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar tiang progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar tiang sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                reply_keyboard("Gambar tiang sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        
        
        elif(tiket[self.chatId].state=="lokasi"):
            if(self.tipeKonten=="location"):
                tiket[self.chatId].setLokasi(self.konten[0],self.konten[1])
                reply_keyboard("Lokasi berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input lokasi harus berupa lokasi")
        return tiket

            

class Tiket():
    def __init__(self, chatId='',noTiket='',keterangan = '',gambar= defaultdict(dict),latitude='',longitude='', state="none", isApproved=0, ODP={"nama":"","lat":None,"long":None},keyboard=Keyboard()):
        self.chatId = str(chatId)
        self.noTiket = noTiket
        self.keterangan = keterangan 
        self.gambar=gambar
        self.gambar["ODCA"]["sebelum"]=""
        self.gambar["ODCA"]["progres"]=""
        self.gambar["ODCA"]["sesudah"]=""
        
        self.gambar["ODCB"]["sebelum"]=""
        self.gambar["ODCB"]["progres"]=""
        self.gambar["ODCB"]["sesudah"]=""
        
        self.gambar["ODPA"]["sebelum"]=""
        self.gambar["ODPA"]["progres"]=""
        self.gambar["ODPA"]["sesudah"]=""
        
        self.gambar["ODPB"]["sebelum"]=""
        self.gambar["ODPB"]["progres"]=""
        self.gambar["ODPB"]["sesudah"]=""
        
        self.gambar["ODPC"]["sebelum"]=""
        self.gambar["ODPC"]["progres"]=""
        self.gambar["ODPC"]["sesudah"]=""
        
        self.gambar["saluran"]["sebelum"]=""
        self.gambar["saluran"]["progres"]=""
        self.gambar["saluran"]["sesudah"]=""
        
        self.gambar["tiang"]["sebelum"]=""
        self.gambar["tiang"]["progres"]=""
        self.gambar["tiang"]["sesudah"]=""
        
        self.keyboard= keyboard
        
        self.latitude= latitude
        self.longitude= longitude
        self.state= state
        self.isApproved=isApproved
        self.ODP=ODP
        
    def setChatId(self,chatId):
        self.chatId = chatId
    
    def setNoTiket(self,noTiket):
        self.noTiket = noTiket
        
    def setState(self,state):
        self.state = state
    
    def setODP(self,records):
        self.ODP["nama"]=records[1]
        self.ODP["long"]=float(records[2])
        self.ODP["lat"]=float(records[3])
        
    
    def setKeterangan(self,keterangan):
        self.keterangan = keterangan
        self.keyboard.json_lvl_1=self.keyboard.json_lvl_1.replace('["/input_keterangan"], ','')
    def setIsApproved(self, isApproved):
        self.isApproved = isApproved
    
    def setGambar(self,fileId,nama):
        if(nama=='gambar ODC A sebelum'):
            self.gambar["ODCA"]["sebelum"] = str(fileId)
            self.keyboard.json_ODCA_lvl_3=self.keyboard.json_ODCA_lvl_3.replace('["sebelum"], ','')
        elif(nama=='gambar ODC A progres'):
            self.gambar["ODCA"]["progres"] = str(fileId)
            self.keyboard.json_ODCA_lvl_3=self.keyboard.json_ODCA_lvl_3.replace('["progres"], ','')
        elif(nama=='gambar ODC A sesudah'):
            self.gambar["ODCA"]["sesudah"] = str(fileId)
            self.keyboard.json_ODCA_lvl_3=self.keyboard.json_ODCA_lvl_3.replace('["sesudah"], ','')
            
        elif(nama=='gambar ODC B sebelum'):
            self.gambar["ODCB"]["sebelum"] = str(fileId)
            self.keyboard.json_ODCB_lvl_3=self.keyboard.json_ODCB_lvl_3.replace('["sebelum"], ','')
        elif(nama=='gambar ODC B progres'):
            self.gambar["ODCB"]["progres"] = str(fileId)
            self.keyboard.json_ODCB_lvl_3=self.keyboard.json_ODCB_lvl_3.replace('["progres"], ','')
        elif(nama=='gambar ODC B sesudah'):
            self.gambar["ODCB"]["sesudah"] = str(fileId)
            self.keyboard.json_ODCB_lvl_3=self.keyboard.json_ODCB_lvl_3.replace('["sesudah"], ','')
            
        elif(nama=='gambar ODP A sebelum'):
            self.gambar["ODPA"]["sebelum"] = str(fileId)
            self.keyboard.json_ODPA_lvl_3=self.keyboard.json_ODPA_lvl_3.replace('["sebelum"], ','')
        elif(nama=='gambar ODP A progres'):
            self.gambar["ODPA"]["progres"] = str(fileId)
            self.keyboard.json_ODPA_lvl_3=self.keyboard.json_ODPA_lvl_3.replace('["progres"], ','')
        elif(nama=='gambar ODP A sesudah'):
            self.gambar["ODPA"]["sesudah"] = str(fileId)
            self.keyboard.json_ODPA_lvl_3=self.keyboard.json_ODPA_lvl_3.replace('["sesudah"], ','')
            
        elif(nama=='gambar ODP B sebelum'):
            self.gambar["ODPB"]["sebelum"] = str(fileId)
            self.keyboard.json_ODPB_lvl_3=self.keyboard.json_ODPB_lvl_3.replace('["sebelum"], ','')
        elif(nama=='gambar ODP B progres'):
            self.gambar["ODPB"]["progres"] = str(fileId)
            self.keyboard.json_ODPB_lvl_3=self.keyboard.json_ODPB_lvl_3.replace('["progres"], ','')
        elif(nama=='gambar ODP B sesudah'):
            self.gambar["ODPC"]["sesudah"] = str(fileId)
            self.keyboard.json_ODPB_lvl_3=self.keyboard.json_ODPB_lvl_3.replace('["sesudah"], ','')
            
        elif(nama=='gambar ODP C sebelum'):
            self.gambar["ODPC"]["sebelum"] = str(fileId)
            self.keyboard.json_ODPC_lvl_3=self.keyboard.json_ODPC_lvl_3.replace('["sebelum"], ','')
        elif(nama=='gambar ODP C progres'):
            self.gambar["ODPC"]["progres"] = str(fileId)
            self.keyboard.json_ODPC_lvl_3=self.keyboard.json_ODPC_lvl_3.replace('["progres"], ','')
        elif(nama=='gambar ODP C sesudah'):
            self.gambar["ODPC"]["sesudah"] = str(fileId)
            self.keyboard.json_ODPC_lvl_3=self.keyboard.json_ODPC_lvl_3.replace('["sesudah"], ','')
            
        elif(nama=='gambar saluran sebelum'):
            self.gambar["saluran"]["sebelum"] = str(fileId)
            self.keyboard.json_saluran_lvl_2=self.keyboard.json_saluran_lvl_2.replace('["sebelum"], ','')
        elif(nama=='gambar saluran progres'):
            self.gambar["saluran"]["progres"] = str(fileId)
            self.keyboard.json_saluran_lvl_2=self.keyboard.json_saluran_lvl_2.replace('["progres"], ','')
        elif(nama=='gambar saluran sesudah'):
            self.gambar["saluran"]["sesudah"] = str(fileId)
            self.keyboard.json_saluran_lvl_2=self.keyboard.json_saluran_lvl_2.replace('["sesudah"], ','')
            
        elif(nama=='gambar tiang sebelum'):
            self.gambar["tiang"]["sebelum"] = str(fileId)
            self.keyboard.json_tiang_lvl_2=self.keyboard.json_tiang_lvl_2.replace('["sebelum"], ','')
        elif(nama=='gambar tiang progres'):
            self.gambar["tiang"]["progres"] = str(fileId)
            self.keyboard.json_tiang_lvl_2=self.keyboard.json_tiang_lvl_2.replace('["progres"], ','')
        elif(nama=='gambar tiang sesudah'):
            self.gambar["tiang"]["sesudah"] = str(fileId)
            self.keyboard.json_tiang_lvl_2=self.keyboard.json_tiang_lvl_2.replace('["sesudah"], ','')
        
        self.keyboard.cekKeyboardGambar()
            
            
    def setLokasi(self,latitude,longitude):
        self.latitude=latitude
        self.longitude=longitude
        self.keyboard.json_lvl_1=self.keyboard.json_lvl_1.replace('["/input_lokasi"], ','')
    
    def print_all(self):
        print("isi tiket")
        print("chat id: {}".format(self.chatId))
        print("noTiket: {}".format(self.noTiket))
        print("keterangan: {}".format(self.keterangan))
        print("fileId Gambar ODC A sebelum: {}".format(self.gambar["ODCA"]["sebelum"]))
        print("fileId Gambar ODC A progres: {}".format(self.gambar["ODCA"]["progres"]))
        print("fileId Gambar ODC A sesudah: {}".format(self.gambar["ODCA"]["sesudah"]))
        print("fileId Gambar ODC B sebelum: {}".format(self.gambar["ODCB"]["sebelum"]))
        print("fileId Gambar ODC B progres: {}".format(self.gambar["ODCB"]["progres"]))
        print("fileId Gambar ODC B sesudah: {}".format(self.gambar["ODCB"]["sesudah"]))
        print("fileId Gambar ODP A sebelum: {}".format(self.gambar["ODPA"]["sebelum"]))
        print("fileId Gambar ODP A progres: {}".format(self.gambar["ODPA"]["progres"]))
        print("fileId Gambar ODP A sesudah: {}".format(self.gambar["ODPA"]["sesudah"]))
        print("fileId Gambar ODP B sebelum: {}".format(self.gambar["ODPB"]["sebelum"]))
        print("fileId Gambar ODP B progres: {}".format(self.gambar["ODPB"]["progres"]))
        print("fileId Gambar ODP B sesudah: {}".format(self.gambar["ODPB"]["sesudah"]))
        print("fileId Gambar ODP C sebelum: {}".format(self.gambar["ODPC"]["sebelum"]))
        print("fileId Gambar ODP C progres: {}".format(self.gambar["ODPC"]["progres"]))
        print("fileId Gambar ODP C sesudah: {}".format(self.gambar["ODPC"]["sesudah"]))
        print("fileId Gambar saluran sebelum: {}".format(self.gambar["saluran"]["sebelum"]))
        print("fileId Gambar saluran progres: {}".format(self.gambar["saluran"]["progres"]))
        print("fileId Gambar saluran sesudah: {}".format(self.gambar["saluran"]["sesudah"]))
        print("fileId Gambar tiang sebelum: {}".format(self.gambar["tiang"]["sebelum"]))
        print("fileId Gambar tiang progres: {}".format(self.gambar["tiang"]["progres"]))
        print("fileId Gambar tiang sesudah: {}".format(self.gambar["tiang"]["sesudah"]))
        print("latitude: {}".format(str(self.latitude)))
        print("longitude: {}".format(str(self.longitude)))
        print("state: {}\n".format(self.state))
    
    def saveData(self):
        now = datetime.datetime.now()
        
        file_path=str(now.year)+"/"+str(now.month)
        try:
            os.mkdir(str(now.year))
            
        except FileExistsError as e:
            print(e)
        try:
            os.mkdir(file_path)
        except FileExistsError as e:
            print(e)
        try:
            dist=round(self.calc_distance())
            
            try:
                for name in glob.glob(file_path+'/'+self.noTiket+'?.txt'):
                    os.remove(name)
                self.save_file(self.gambarSebelum,file_path+"/"+self.noTiket+'-a.jpg')
                self.save_file(self.gambarProgres,file_path+"/"+self.noTiket+'-b.jpg')
                self.save_file(self.gambarSesudah,file_path+"/"+self.noTiket+'-c.jpg')
            except:
                True
            try:
                update_row_odp(self,dist)
                self.send_message("Tiket dengan No. {} selesai diinputkan".format(self.noTiket))
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)
                self.send_message(e)
            
            self.noTiket = ''
            self.keterangan = '' 
            self.gambarSebelum = ''
            self.gambarProgres = ''
            self.gambarSesudah = ''
            self.latitude= ''
            self.longitude= ''
            self.state= 'none'
        except KeyError:
            self.send_message("Data yang diinputkan belum lengkap")
    
    def reviewTiket(self):
        self.send_message("Isi tiket")
        self.send_message("noTiket: {}".format(self.noTiket))
        dist=0
        status=True
        if(self.keterangan!=""):
            self.send_message("keterangan: {}".format(self.keterangan))
        else:
            self.send_message("Keterangan belum diinputkan")
            status=False
            
        if(self.gambar["ODCA"]["sebelum"]!=""):
            self.send_file(self.gambar["ODCA"]["sebelum"],"Gambar ODC A Sebelum")
        else:
            self.send_message("Gambar ODC A 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["ODCA"]["progres"]!=""):
            self.send_file(self.gambar["ODCA"]["progres"],"Gambar ODC A Progres")
        else:
            self.send_message("Gambar ODC A 'progres' belum diinputkan")
            status=False
        if(self.gambar["ODCA"]["sesudah"]!=""):
            self.send_file(self.gambar["ODCA"]["sesudah"],"Gambar ODC A Sesudah")
        else:
            self.send_message("Gambar ODC A 'sesudah' belum diinputkan")
            status=False
            
        if(self.gambar["ODCB"]["sebelum"]!=""):
            self.send_file(self.gambar["ODCB"]["sebelum"],"Gambar ODC B Sebelum")
        else:
            self.send_message("Gambar ODC B 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["ODCB"]["progres"]!=""):
            self.send_file(self.gambar["ODCB"]["progres"],"Gambar ODC B Progres")
        else:
            self.send_message("Gambar ODC B 'progres' belum diinputkan")
            status=False
        if(self.gambar["ODCB"]["sesudah"]!=""):
            self.send_file(self.gambar["ODCB"]["sesudah"],"Gambar ODC B Sesudah")
        else:
            self.send_message("Gambar ODC B 'sesudah' belum diinputkan")
            status=False
        if(self.gambar["ODPA"]["sebelum"]!=""):
            self.send_file(self.gambar["ODPA"]["sebelum"],"Gambar ODP A Sebelum")
        else:
            self.send_message("Gambar ODP A 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["ODPA"]["progres"]!=""):
            self.send_file(self.gambar["ODPA"]["progres"],"Gambar ODP A Progres")
        else:
            self.send_message("Gambar ODP A 'progres' belum diinputkan")
            status=False
        if(self.gambar["ODPA"]["sesudah"]!=""):
            self.send_file(self.gambar["ODPA"]["sesudah"],"Gambar ODP A Sesudah")
        else:
            self.send_message("Gambar ODP A 'sesudah' belum diinputkan")
            status=False
        
        if(self.gambar["ODPB"]["sebelum"]!=""):
            self.send_file(self.gambar["ODPB"]["sebelum"],"Gambar ODP B Sebelum")
        else:
            self.send_message("Gambar ODP B 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["ODPB"]["progres"]!=""):
            self.send_file(self.gambar["ODPB"]["progres"],"Gambar ODP B Progres")
        else:
            self.send_message("Gambar ODP B 'progres' belum diinputkan")
            status=False
        if(self.gambar["ODPB"]["sesudah"]!=""):
            self.send_file(self.gambar["ODPB"]["sesudah"],"Gambar ODP B Sesudah")
        else:
            self.send_message("Gambar ODP B 'sesudah' belum diinputkan")
            status=False
        
        if(self.gambar["ODPC"]["sebelum"]!=""):
            self.send_file(self.gambar["ODPC"]["sebelum"],"Gambar ODP C Sebelum")
        else:
            self.send_message("Gambar ODPC 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["ODPC"]["progres"]!=""):
            self.send_file(self.gambar["ODPC"]["progres"],"Gambar ODP C Progres")
        else:
            self.send_message("Gambar ODPC 'progres' belum diinputkan")
            status=False
        if(self.gambar["ODPC"]["sesudah"]!=""):
            self.send_file(self.gambar["ODPC"]["sesudah"],"Gambar ODP C Sesudah")
        else:
            self.send_message("Gambar ODP C 'sesudah' belum diinputkan")
            status=False
        
        if(self.gambar["tiang"]["sebelum"]!=""):
            self.send_file(self.gambar["tiang"]["sebelum"],"Gambar tiang Sebelum")
        else:
            self.send_message("Gambar tiang 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["tiang"]["progres"]!=""):
            self.send_file(self.gambar["tiang"]["progres"],"Gambar tiang Progres")
        else:
            self.send_message("Gambar tiang 'progres' belum diinputkan")
            status=False
        if(self.gambar["tiang"]["sesudah"]!=""):
            self.send_file(self.gambar["tiang"]["sesudah"],"Gambar tiang Sesudah")
        else:
            self.send_message("Gambar tiang 'sesudah' belum diinputkan")
            status=False
        
        if(self.gambar["saluran"]["sebelum"]!=""):
            self.send_file(self.gambar["saluran"]["sebelum"],"Gambar saluran Sebelum")
        else:
            self.send_message("Gambar saluran 'sebelum' belum diinputkan")
            status=False
        if(self.gambar["saluran"]["progres"]!=""):
            self.send_file(self.gambar["saluran"]["progres"],"Gambar saluran Progres")
        else:
            self.send_message("Gambar saluran 'progres' belum diinputkan")
            status=False
        if(self.gambar["saluran"]["sesudah"]!=""):
            self.send_file(self.gambar["saluran"]["sesudah"],"Gambar saluran Sesudah")
        else:
            self.send_message("Gambar saluran 'sesudah' belum diinputkan")
            status=False
        
        if(self.latitude!=""):
            self.send_location()
            dist=round(self.calc_distance())
            self.send_message("Jarak anda dengan ODP adalah {} m".format(str(dist)))
        else:
            self.send_message("Lokasi belum diinputkan")
            status=False
        if(dist>max_dist):
            self.send_message("Jarak yang dikirimkan melebihi {} m.".format(max_dist))
        if(status):   
            reply_keyboard("Edit Kembali atau Submit?",self.chatId,json_aft_review)
        else:
            reply_keyboard("Data belum lengkap atau gambar ada yang sama. Silakan lengkapi atau ganti",self.chatId,self.keyboard.json_lvl_1)
        
    def save_file(self, fileId,path):
        url = URL + "getFile?file_id={}".format(fileId)
        js = get_json_from_url(url)
        file_path = js["result"]["file_path"]
        url = URL_FILE + file_path
        urllib.request.urlretrieve(url,path)

    def save_text(self,isitext, namafile):
        file = open(str(self.noTiket)+"/"+namafile+".txt","w") 
        file.write(isitext)
        file.close()
        
    def calc_distance(self):
        lat2=self.ODP['lat']
        lon2=self.ODP['long']
        R = 6371e3  #metres
        o1 = math.radians(self.latitude)
        o2 = math.radians(lat2)
        delta1 = math.radians(lat2-self.latitude)
        delta2 = math.radians(lon2-self.longitude)
        print((lon2,lat2))
        print((self.longitude,self.latitude))
        a = math.sin(delta1/2) * math.sin(delta1/2) + math.cos(o1) * math.cos(o2) * math.sin(delta2/2) * math.sin(delta2/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        print(c)
        print(d)
        return(d)
        
    def sendImage(self,path,caption):
        try:
            url_send = URL+"sendPhoto";
            print(url_send)
            files = {'photo': open(path, 'rb')}
            print(files)
            data = {'chat_id' : self.chatId,'caption':caption}
            requests.post(url_send, files=files, data=data)
        except:
            print("send image gagal")
        
    def send_message(self, text):
        url = URL + "sendMessage?text={}&chat_id={}".format(text, self.chatId)
        get_url(url)
            
    def send_file(self, file_id,text):
        url = URL + "sendPhoto?photo={}&chat_id={}&caption={}".format(file_id, self.chatId,text)
        get_url(url)
    
    def send_location(self):
        url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}".format(self.chatId, self.latitude, self.longitude)
        get_url(url)
        
    def kirimContoh(self):
        self.sendImage("contoh/1.jpg","Contoh gambar 'sebelum' yang ideal")
        self.sendImage("contoh/2.jpg","Contoh gambar 'progres' yang ideal")
        self.sendImage("contoh/3.jpg","Contoh gambar 'sesudah' yang ideal")
                

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
            if(bool(isApproved(update.chatId))):
                tiket[update.chatId]=Tiket(chatId=update.chatId,isApproved=1)
            else:
                tiket[update.chatId]=Tiket(chatId=update.chatId,isApproved=0)
        if (update.konten, update.chatId) != last_textchat:
            if(update.chatId!=0):
                if(tiket[update.chatId].isApproved==1):
                    if(tiket[update.chatId].state=="none"):
                        tiket=update.cek_command(tiket) 
                    else:
                        tiket=update.cek_konten_sesuai_state(tiket) 
                    try:
                        tiket[update.chatId].print_all()
                    except AttributeError as e:
                        print(e)
                else:
                    if(tiket[update.chatId].state=="daftar"):
                        if(update.tipeKonten=="text"):
                            array = update.konten[0].split("_")
                            try:
                                daftar(update.chatId,array)
                                tiket[update.chatId].send_message("Selesai terdaftar")
                                tiket[update.chatId].setIsApproved(1)
                                tiket[update.chatId].setState("none")
                            except:
                                tiket[update.chatId].send_message("Format yang dikirimkan salah")
                    elif(tiket[update.chatId].state=="none"):
                        if "/daftar" in update.konten[0]:
                            tiket[update.chatId].setState("daftar")
                            tiket[update.chatId].send_message("kirim dengan format: NIK_NAMA_LOKER")
                        else:    
                            tiket[update.chatId].send_message("ID Anda belum terdaftar atau belum mendapat izin. Silahkan mendaftar /daftar")   
            last_textchat = (update.konten, update.chatId)
            time.sleep(0.1)
            
if __name__ == '__main__':
    main()
