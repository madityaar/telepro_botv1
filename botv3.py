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
#from tiket2 import Tiket, Update


TOKEN = "743391112:AAF60UYlsEhkgb9qU-APK5nqxffhTb9LMbY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
URL_FILE = "https://api.telegram.org/file/bot{}/".format(TOKEN)
###########
try:
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="dtest")        # name of the data base
    
    # you must create a Cursor object. It will let
    # you execute all the queries you need
    cur = db.cursor()
except:
    print("database not connected")
    
def insert_row(data):
    cur.execute("INSERT INTO tiket (no_tiket,gambar_sebelum,gambar_sesudah,keterangan,latitude,longitude) VALUES ('"+data['no_tiket']+"','"+data['gambar_sebelum']+"','"+data['gambar_sesudah']+"','"+data['keterangan']+"','"+data['latitude'] +"','"+data['longitude']+"')")
    db.commit()
    db.close()

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
    sql="update mytable set photo_before='"+tiket.noTiket+"-a"+"', photo_process='"+tiket.noTiket+"-b"+"', photo_after='"+tiket.noTiket+"-c"+"', longitude_u="+str(tiket.longitude)+", latitude_u="+str(tiket.longitude)+", distance="+str(dist)+", updated_by="+tiket.chatId+", updated_date=SYSDATE(),keterangan='"+tiket.keterangan+"' where ticket_id='"+tiket.noTiket+"'"
    cur.execute(sql)
    db.commit()
    db.close()

def daftar(chatid,array):
    sql="INSERT INTO userapproval VALUES ('"+str(chatid)+"','"+array[0]+"','"+array[1].upper()+"','"+array[2].upper()+"',1)"
    cur.execute(sql)
    db.commit()
    db.close()

def select_ticket(ticket):
    sql="select ticket_id,ODP, longitude, latitude from mytable where ticket_id='"+str(ticket)+"'"
    cur.execute(sql)
    records = cur.fetchall()
    return records[0]
###########

data1={"keyboard": [["/input_tiket"]],"one_time_keyboard": True}
data2={"keyboard": [["/input_keterangan"],["/input_gambar_sebelum"],["/input_gambar_progres"],["/input_gambar_sesudah"],["/input_lokasi"],["/review_tiket"]],"one_time_keyboard": True,"resize_keyboard": True}
data3={"keyboard": [[{"text":"kirim lokasi","request_location":True}]],"one_time_keyboard": True,"resize_keyboard": True}
data4={"keyboard": [["Edit Data"],["/input_selesai"]],"one_time_keyboard": True}

json_input_tiket=json.dumps(data1)
json_all_comm=json.dumps(data2)
json_req_location=json.dumps(data3)
json_aft_review=json.dumps(data4)

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
    def __init__(self, chatId='',noTiket='',keterangan = '',gambarSebelum = '',gambarProgres = '',gambarSesudah = '',latitude='',longitude='', state="none", isApproved=0, ODP={"nama":"","lat":None,"long":None}):
        self.chatId = str(chatId)
        self.noTiket = noTiket
        self.keterangan = keterangan 
        self.gambarSebelum = gambarSebelum
        self.gambarProgres = gambarProgres
        self.gambarSesudah = gambarSesudah
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
        self.ODP["lat"]=float(records[2])
        self.ODP["long"]=float(records[3])
    
    def setKeterangan(self,keterangan):
        self.keterangan = keterangan
    def setIsApproved(self, isApproved):
        self.isApproved = isApproved
    
    def setGambar(self,fileId,nama):
        if(nama=='sebelum'):
            self.gambarSebelum = str(fileId)
        elif(nama=='progres'):
            self.gambarProgres = str(fileId)
        elif(nama=='sesudah'):
            self.gambarSesudah = str(fileId)
            
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
        now = datetime.datetime.now()
        
        file_path=str(now.year)+"/"+str(now.month)
        try:
            os.mkdir(str(now.year))
            os.mkdir(file_path)
        except FileExistsError:
            True
        try:
            dist=self.calc_distance()
            
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
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)
            self.send_message("Tiket dengan No. "+self.noTiket+" selesai diinputkan")
            
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
        self.send_message("noTiket: "+self.noTiket)
        status=True
        if(self.keterangan!=""):
            self.send_message("keterangan: "+self.keterangan)
        else:
            status=False
        if(self.gambarSebelum!=""):
            self.send_file(self.gambarSebelum,"Gambar Sebelum")
        else:
            status=False
        if(self.gambarProgres!=""):
            self.send_file(self.gambarProgres,"Gambar Progres")
        else:
            status=False
        if(self.gambarSesudah!=""):
            self.send_file(self.gambarSesudah,"Gambar Sesudah")
        else:
            status=False
        if(self.latitude!=""):
            self.send_location()
        else:
            status=False
        if(status):   
            reply_keyboard("Edit Kembali atau Submit?",self.chatId,json_aft_review)
        else:
            reply_keyboard("Data belum lengkap. Sila lengkapi kembali",self.chatId,json_all_comm)
        
    def save_file(self, fileId,path):
        url = URL + "getFile?file_id={}".format(fileId)
        js = get_json_from_url(url)
        file_path = js["result"]["file_path"]
        url = URL_FILE + file_path
        print(path)
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
    
        a = math.sin(delta1/2) * math.sin(delta1/2) + math.cos(o1) * math.cos(o2) * math.sin(delta2/2) * math.sin(delta2/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return(d)
        
    def send_message(self, text):
        url = URL + "sendMessage?text={}&chat_id={}".format(text, self.chatId)
        get_url(url)
            
    def send_file(self, file_id,text):
        url = URL + "sendPhoto?photo={}&chat_id={}&caption={}".format(file_id, self.chatId,text)
        get_url(url)
    
    def send_location(self):
        url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}".format(self.chatId, self.latitude, self.longitude)
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
            if(bool(isApproved(update.chatId))):
                tiket[update.chatId]=Tiket(chatId=update.chatId,isApproved=1)
            else:
                tiket[update.chatId]=Tiket(chatId=update.chatId,isApproved=0)
        if (update.konten, update.chatId) != last_textchat:
            if(update.chatId!=0):
                if(tiket[update.chatId].isApproved==1):
                    if(tiket[update.chatId].state=="none"):
                        if "/input_tiket" in update.konten[0]:
                            tiket[update.chatId].setState("notiket")
                            remove_keyboard("Silakan input nomor tiket",update.chatId)
                        if(tiket[update.chatId].noTiket!=''):
                            if "/input_keterangan" in update.konten[0]:
                                tiket[update.chatId].setState("keterangan")
                                remove_keyboard("Silakan input keterangan",update.chatId)
                            elif "/input_gambar_sebelum" in update.konten[0]:
                                tiket[update.chatId].setState("gambar sebelum")
                                remove_keyboard("Silakan input gambar",update.chatId)
                            elif "/input_gambar_progres" in update.konten[0]:
                                tiket[update.chatId].setState("gambar progres")
                                remove_keyboard("Silakan input gambar",update.chatId)
                            elif "/input_gambar_sesudah" in update.konten[0]:
                                tiket[update.chatId].setState("gambar sesudah")
                                remove_keyboard("Silakan input gambar",update.chatId)
                            elif "/input_lokasi" in update.konten[0]:
                                tiket[update.chatId].setState("lokasi")
                                reply_keyboard("Silakan input lokasi",update.chatId,json_req_location)
                            elif "/input_selesai" in update.konten[0]:
                                tiket[update.chatId].saveData()
                            elif "/review_tiket" in update.konten[0]:
                                tiket[update.chatId].reviewTiket()
                            elif "Edit Data" in update.konten[0]:
                                reply_keyboard("Silakan pilih data yang akan diedit",update.chatId,json_all_comm)
                            else:
                                tiket[update.chatId].send_message("Silakan masukkan perintah yang sesuai")
                        elif (tiket[update.chatId].state!="notiket"):
                            reply_keyboard("Silakan masukkan nomor tiket terlebih dahulu",update.chatId,json_input_tiket)
                    else:
                        if(tiket[update.chatId].state=="notiket"):
                            if(update.tipeKonten=="text"):
                                records=None
                                records=select_ticket(update.konten[0])
                                if(bool(records)):
                                    tiket[update.chatId].setNoTiket(update.konten[0])
                                    tiket[update.chatId].setODP(records)
                                    reply_keyboard("Nomor Tiket: "+tiket[update.chatId].noTiket+" berhasil diinput",update.chatId,json_all_comm)
                                    tiket[update.chatId].setState("none")
                                else:
                                    tiket[update.chatId].send_message("Tiket yang diinputkan tidak terdaftar. Mohon masukkan kembali")
                            else:
                                tiket[update.chatId].send_message("Nomor tiket harus berupa teks")
                        elif(tiket[update.chatId].state=="keterangan"):
                            if(update.tipeKonten=="text"):
                                tiket[update.chatId].setKeterangan(update.konten[0])
                                reply_keyboard("Keterangan berhasil terinput",update.chatId,json_all_comm)
                                tiket[update.chatId].setState("none")
                            else:
                                tiket[update.chatId].send_message("Isi keterangan harus berupa teks")
                        elif(tiket[update.chatId].state=="gambar sebelum"):
                            if(update.tipeKonten=="gambar"):
                                tiket[update.chatId].setGambar(update.konten[0],"sebelum")
                                reply_keyboard("Gambar tampak 'sebelum' berhasil terinput",update.chatId,json_all_comm)
                                tiket[update.chatId].setState("none")
                            else:
                                tiket[update.chatId].send_message("Input gambar harus berupa gambar")
                        elif(tiket[update.chatId].state=="gambar progres"):
                            if(update.tipeKonten=="gambar"):
                                tiket[update.chatId].setGambar(update.konten[0],"progres")
                                reply_keyboard("Gambar tampak 'progres' berhasil terinput",update.chatId,json_all_comm)
                                tiket[update.chatId].setState("none")
                            else:
                                tiket[update.chatId].send_message("Input gambar harus berupa gambar")
                        elif(tiket[update.chatId].state=="gambar sesudah"):
                            if(update.tipeKonten=="gambar"):
                                tiket[update.chatId].setGambar(update.konten[0],"sesudah")
                                reply_keyboard("Gambar tampak 'sesudah' berhasil terinput",update.chatId,json_all_comm)
                                tiket[update.chatId].setState("none")
                            else:
                                tiket[update.chatId].send_message("Input gambar harus berupa gambar")
                        elif(tiket[update.chatId].state=="lokasi"):
                            if(update.tipeKonten=="location"):
                                tiket[update.chatId].setLokasi(update.konten[0],update.konten[1])
                                reply_keyboard("Lokasi berhasil terinput",update.chatId,json_all_comm)
                                tiket[update.chatId].setState("none")
                            else:
                                tiket[update.chatId].send_message("Input lokasi harus berupa lokasi")
                    try:
                        tiket[update.chatId].print_all()
                    except AttributeError:
                        True
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
            
if __name__ == '__main__':
    main()
