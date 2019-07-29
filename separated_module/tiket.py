# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:32:43 2019

@author: Ditzy
"""
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
from keyboard import *
from general import *

class Tiket():
    def __init__(self, chatId='',noTiket='',keterangan = '',gambar= defaultdict(dict),latitude='',longitude='', state="none", isApproved=0, ODP={"nama":"","lat":None,"long":None},keyboard=Keyboard()):
        self.chatId = str(chatId)
        self.noTiket = noTiket
        self.keterangan = keterangan 
        self.gambar=gambar
        
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
            self.gambar["ODPB"]["sesudah"] = str(fileId)
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
                self.save_file(self.gambar['ODPA']['sebelum'],'{}/{}-{}-a.jpg'.format(file_path,self.noTiket,'ODPA'))
                self.save_file(self.gambar['ODPA']['progres'],'{}/{}-{}-b.jpg'.format(file_path,self.noTiket,'ODPA'))
                self.save_file(self.gambar['ODPA']['sesudah'],'{}/{}-{}-c.jpg'.format(file_path,self.noTiket,'ODPA'))
                
                self.save_file(self.gambar['ODPB']['sebelum'],'{}/{}-{}-a.jpg'.format(file_path,self.noTiket,'ODPB'))
                self.save_file(self.gambar['ODPB']['progres'],'{}/{}-{}-b.jpg'.format(file_path,self.noTiket,'ODPB'))
                self.save_file(self.gambar['ODPB']['sesudah'],'{}/{}-{}-c.jpg'.format(file_path,self.noTiket,'ODPB'))
                
                self.save_file(self.gambar['ODPC']['sebelum'],'{}/{}-{}-a.jpg'.format(file_path,self.noTiket,'ODPC'))
                self.save_file(self.gambar['ODPC']['progres'],'{}/{}-{}-b.jpg'.format(file_path,self.noTiket,'ODPC'))
                self.save_file(self.gambar['ODPC']['sesudah'],'{}/{}-{}-c.jpg'.format(file_path,self.noTiket,'ODPC'))
                
                self.save_file(self.gambar['saluran']['sebelum'],'{}/{}-{}-a.jpg'.format(file_path,self.noTiket,'saluran'))
                self.save_file(self.gambar['saluran']['progres'],'{}/{}-{}-b.jpg'.format(file_path,self.noTiket,'saluran'))
                self.save_file(self.gambar['saluran']['sesudah'],'{}/{}-{}-c.jpg'.format(file_path,self.noTiket,'saluran'))
                
                self.save_file(self.gambar['tiang']['sebelum'],'{}/{}-{}-a.jpg'.format(file_path,self.noTiket,'tiang'))
                self.save_file(self.gambar['tiang']['progres'],'{}/{}-{}-b.jpg'.format(file_path,self.noTiket,'tiang'))
                self.save_file(self.gambar['tiang']['sesudah'],'{}/{}-{}-c.jpg'.format(file_path,self.noTiket,'tiang'))
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
       
    def reviewTiketWeb(self):
        self.send_message("Isi tiket")
        self.send_message("noTiket: {}".format(self.noTiket))
        hasil_sql=select_review(self)
        
        print('{}/{}/{}'.format(hasil_sql[15],hasil_sql[16],hasil_sql[0]))
        
        
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[0]),'Gambar ODP A sebelum')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[1]),'Gambar ODP A progres')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[2]),'Gambar ODP A sesudah')
        
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[3]),'Gambar ODP B sebelum')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[4]),'Gambar ODP B progres')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[5]),'Gambar ODP B sesudah')
        
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[6]),'Gambar ODP C sebelum')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[7]),'Gambar ODP C progres')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[8]),'Gambar ODP C sesudah')
        
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[9]),'Gambar saluran sebelum')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[10]),'Gambar saluran progres')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[11]),'Gambar saluran sesudah')
        
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[12]),'Gambar tiang sebelum')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[13]),'Gambar tiang progres')
        self.sendImage('{}/{}/{}.jpg'.format(hasil_sql[15],hasil_sql[16],hasil_sql[14]),'Gambar tiang sesudah')
        
    
        
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
                
