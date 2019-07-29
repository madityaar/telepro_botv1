# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:36:20 2019

@author: Ditzy
"""

import general
import database

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
            general.reply_keyboard("Silakan input nomor tiket",self.chatId,general.json_cancel)
        if(tiket[self.chatId].noTiket!=''):
            if "/input_keterangan" in self.konten[0]:
                tiket[self.chatId].setState("keterangan")
                general.reply_keyboard("Silakan input keterangan",self.chatId,general.json_cancel)
                '''
            elif "/input_gambar_ODC-RK-MSAN" in self.konten[0]:
                tiket[self.chatId].setState("gambar ODC")
                general.reply_keyboard("Pilih ODC",self.chatId,tiket[self.chatId].keyboard.json_ODC_lvl_2)'''
            elif "/input_gambar_ODP-RP" in self.konten[0]:
                tiket[self.chatId].setState("gambar ODP")
                general.reply_keyboard("Pilih ODP",self.chatId,tiket[self.chatId].keyboard.json_ODP_lvl_2)
            elif "/input_gambar_saluran_penanggal" in self.konten[0]:
                tiket[self.chatId].setState("gambar saluran")
                general.reply_keyboard("Silakan pilih kondisi ",self.chatId,tiket[self.chatId].keyboard.json_saluran_lvl_2)
            elif "/input_gambar_tiang" in self.konten[0]:
                tiket[self.chatId].setState("gambar tiang")
                general.reply_keyboard("Silakan pilih kondisi ",self.chatId,tiket[self.chatId].keyboard.json_tiang_lvl_2)
            elif "/input_lokasi" in self.konten[0]:
                tiket[self.chatId].setState("lokasi")
                general.reply_keyboard("Silakan input lokasi",self.chatId,general.json_req_location)
            elif "/input_selesai" in self.konten[0]:
                tiket[self.chatId].saveData()
            elif "/review_tiket" in self.konten[0]:
                tiket[self.chatId].reviewTiket()
            elif "/review_web" in self.konten[0]:
                tiket[self.chatId].reviewTiketWeb()
            elif "/cancel" in self.konten[0]:
                tiket[self.chatId].setState('none')
            elif "/kirim_contoh" in self.konten[0]:
                try:
                    tiket[self.chatId].kirimContoh()
                except:
                    print('error sending image')
            elif "Edit Data" in self.konten[0]:
                tiket[self.chatId].keyboard.resetKeyboard()
                general.reply_keyboard("Silakan pilih data yang akan diedit",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                
            else:
                tiket[self.chatId].send_message("Silakan masukkan perintah yang sesuai")
        elif (tiket[self.chatId].state!="notiket"):
            general.reply_keyboard("Silakan masukkan nomor tiket terlebih dahulu",self.chatId,general.json_input_tiket)
        return tiket
            
    def cek_konten_sesuai_state(self,tiket):
        if(self.konten[0]=="/cancel"):
            string_rep="Input {} dibatalkan".format(tiket[self.chatId].state)
            tiket[self.chatId].setState("none")
            if(tiket[self.chatId].state=="notiket"):
                general.reply_keyboard(string_rep,self.chatId,general.json_input_tiket)
            else:
                general.reply_keyboard(string_rep,self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
        elif(tiket[self.chatId].state=="notiket"):
            if(self.tipeKonten=="text"):
                if(len(self.konten[0])==general.max_tiket_str):
                    records=None
                    records=database.select_ticket(self.konten[0])
                    if(bool(records)):
                        tiket[self.chatId].setNoTiket(self.konten[0])
                        tiket[self.chatId].setODP(records)
                        general.reply_keyboard("Nomor Tiket: {} berhasil diinput".format(tiket[self.chatId].noTiket),self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                        tiket[self.chatId].setState("none")
                    else:
                        tiket[self.chatId].send_message("Tiket yang diinputkan tidak terdaftar. Mohon masukkan kembali")
                else:
                    tiket[self.chatId].send_message("Tiket harus terdiri 10 karakter")
            else:
                tiket[self.chatId].send_message("Nomor tiket harus berupa teks")
        elif(tiket[self.chatId].state=="keterangan"):
            if(self.tipeKonten=="text"):
                if(len(self.konten[0])<=general.max_keterangan):
                    tiket[self.chatId].setKeterangan(self.konten[0])
                    general.reply_keyboard("Keterangan berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                    tiket[self.chatId].setState("none")
                else:
                    tiket[self.chatId].send_message("Keterangan tidak boleh lebih dari 30 karakter")
            else:
                tiket[self.chatId].send_message("Isi keterangan harus berupa teks")
        elif(tiket[self.chatId].state=="gambar ODP"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="ODP A"):
                    tiket[self.chatId].setState("gambar ODP A")   
                    general.reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPA_lvl_3)
                elif(self.konten[0]=="ODP B"):
                    tiket[self.chatId].setState("gambar ODP B")
                    general.reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPB_lvl_3)
                elif(self.konten[0]=="ODP C"):
                    tiket[self.chatId].setState("gambar ODP C")
                    general.reply_keyboard("Silakan pilih kondisi",self.chatId,tiket[self.chatId].keyboard.json_ODPC_lvl_3)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 ODP
        elif(tiket[self.chatId].state=="gambar ODP A"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP A sebelum")    
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP A progres")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP A sesudah")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
                
        elif(tiket[self.chatId].state=="gambar ODP B"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP B sebelum")    
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP B progres")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP B sesudah")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
                
        elif(tiket[self.chatId].state=="gambar ODP C"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar ODP C sebelum")    
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar ODP C progres")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar ODP C sesudah")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 4
        elif(tiket[self.chatId].state=="gambar ODP A sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP A sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP A progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP A progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP A sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP A sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### Menu Tingkat 4 ODP B
        elif(tiket[self.chatId].state=="gambar ODP B sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP B sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP B progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP B progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP B sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP B sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### Menu Tingkat 4 ODP C
        elif(tiket[self.chatId].state=="gambar ODP C sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP C sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar ODP C progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP C progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar ODP C sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar ODP C sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### MENU TINGKAT 2 SALURAN        
        elif(tiket[self.chatId].state=="gambar saluran"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar saluran sebelum")    
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar saluran progres")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar saluran sesudah")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 SALURAN
        elif(tiket[self.chatId].state=="gambar saluran sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar saluran sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar saluran progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar saluran progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar saluran sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar saluran sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
#### MENU TINGKAT 2 TIANG
        elif(tiket[self.chatId].state=="gambar tiang"):
            if(self.tipeKonten=="text"):
                if(self.konten[0]=="sebelum"):
                    tiket[self.chatId].setState("gambar tiang sebelum")    
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="progres"):
                    tiket[self.chatId].setState("gambar tiang progres")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
                elif(self.konten[0]=="sesudah"):
                    tiket[self.chatId].setState("gambar tiang sesudah")
                    general.reply_keyboard("Silakan input gambar",self.chatId,general.json_cancel)
            else:
                tiket[self.chatId].send_message("Pilih menu sesuai yang tersedia")
#### MENU TINGKAT 3 TIANG
        elif(tiket[self.chatId].state=="gambar tiang sebelum"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar tiang sebelum berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg") 
        elif(tiket[self.chatId].state=="gambar tiang progres"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar tiang progres berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        elif(tiket[self.chatId].state=="gambar tiang sesudah"):
            if(self.tipeKonten=="gambar"):
                tiket[self.chatId].setGambar(self.konten[0],tiket[self.chatId].state)
                general.reply_keyboard("Gambar tiang sesudah berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input gambar harus berupa .jpeg")
        
        
        elif(tiket[self.chatId].state=="lokasi"):
            if(self.tipeKonten=="location"):
                tiket[self.chatId].setLokasi(self.konten[0],self.konten[1])
                general.reply_keyboard("Lokasi berhasil terinput",self.chatId,tiket[self.chatId].keyboard.json_lvl_1)
                tiket[self.chatId].setState("none")
            else:
                tiket[self.chatId].send_message("Input lokasi harus berupa lokasi")
        return tiket