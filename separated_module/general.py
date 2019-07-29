# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:36:58 2019

@author: Ditzy
"""

import json 
import requests


max_dist=50
max_keterangan=200
max_tiket_str=10

TOKEN = "743391112:AAF60UYlsEhkgb9qU-APK5nqxffhTb9LMbY"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
URL_FILE = "https://api.telegram.org/file/bot{}/".format(TOKEN)

data1={"keyboard": [["/input_tiket"]],"one_time_keyboard": True}
data3={"keyboard": [[{"text":"kirim lokasi","request_location":True}],["/cancel"]],"one_time_keyboard": True,"resize_keyboard": True}
data4={"keyboard": [["Edit Data"],["/input_selesai"]],"one_time_keyboard": True}
data5={"keyboard": [["/cancel"]],"one_time_keyboard": True}
json_input_tiket=json.dumps(data1)
json_req_location=json.dumps(data3)
json_aft_review=json.dumps(data4)
json_cancel=json.dumps(data5)


###########
def reply_keyboard(text,chatId,djson):
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, djson)
    get_url(url)
    
def remove_keyboard(text, chatId):
    json_remove=json.dumps({"remove_keyboard":True})
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text,chatId, json_remove)
    get_url(url)
######



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