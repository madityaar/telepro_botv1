# -*- coding: utf-8 -*-
from collections import defaultdict
import time

import tiketcls  
import updatecls 
import general
import database

#from tiket2 import Tiket, Update

###########

def main():
    database.connect_db()
    update = updatecls.Update()
    tiket= defaultdict(dict)
    update.setKonten(general.get_updates(update.offset))
    last_textchat = (update.konten, update.chatId)
    while True:
        update.setKonten(general.get_updates(update.offset))
        if(not bool(tiket[update.chatId])):
            if(bool(database.isApproved(update.chatId))):
                tiket[update.chatId]=tiketcls.Tiket(chatId=update.chatId,isApproved=1)
            else:
                tiket[update.chatId]=tiketcls.Tiket(chatId=update.chatId,isApproved=0)
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
                                database.daftar(update.chatId,array)
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
