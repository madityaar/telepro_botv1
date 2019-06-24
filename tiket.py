#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:10:00 2019

@author: madityaar
"""
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
                try:
                    self.konten[0] = updates["result"][last_update]["message"]["photo"][2]["file_id"]
                except IndexError:
                    try:
                        self.konten[0] = updates["result"][last_update]["message"]["photo"][0]["file_id"]
                    except IndexError:
                        True
                try:
                    self.konten[1] = updates["result"][last_update]["message"]["caption"]
                except IndexError:
                    True
                self.tipeKonten="gambar"
            except KeyError:
                self.konten[0] = updates["result"][last_update]["message"]["photo"][2]["file_id"]
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
            send_message(self.chatId,"Gambar tampak 'sebelum' berhasil terinput")
        elif(nama=='progres'):
            self.gambarProgres = str(fileId)
            send_message(self.chatId,"Gambar tampak 'progres' berhasil terinput")
        elif(nama=='sesudah'):
            self.gambarSesudah = str(fileId)
            send_message(self.chatId,"Gambar tampak 'sesudah' berhasil terinput")
    
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
        print("longitude: "+str(self.longitude)+"\n")
    
    def saveData(self):
        try:
            os.mkdir(self.noTiket)
        except FileExistsError:
            True
        save_file(self.gambarSebelum,self.chatId,self.noTiket,'sebelum')
        save_file(self.gambarProgres,self.chatId,self.noTiket,'progres')
        save_file(self.gambarSesudah,self.chatId,self.noTiket,'sesudah')
        save_text(self.keterangan,self.chatId,self.noTiket,'keterangan')
        loc_lengkap='Latitude: '+str(self.latitude)+' \nLongitude: '+str(self.longitude)+' \nDistance: '+str(calc_distance(self.latitude,self.longitude))
        save_text(loc_lengkap,self.chatId,self.noTiket,'lokasi')
    
    
    def reviewTiket(self):
        send_message(self.chatId,"isi tiket")
        send_message(self.chatId,"noTiket: "+self.noTiket)
        if(self.keterangan!=""):
            send_message(self.chatId,"keterangan: "+self.keterangan)
        if(self.gambarSebelum!=""):
            send_file(self.chatId,self.gambarSebelum,"Gambar Sebelum")
        if(self.gambarProgres!=""):
            send_file(self.chatId,self.gambarProgres,"Gambar Progres")
        if(self.gambarSesudah!=""):
            send_file(self.chatId,self.gambarSesudah,"Gambar Sesudah")
        if(self.latitude!=""):
            send_location(self.chatId,self.latitude,self.longitude)
