# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:02:13 2019

@author: Ditzy
"""
import MySQLdb
cur=None
db=None

def connect_db():
    global db, cur
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
    global db, cur
    cur.execute("INSERT INTO tiket (no_tiket,gambar_sebelum,gambar_sesudah,keterangan,latitude,longitude) VALUES ('{}','{}','{}','{}','{}','{}')".format(data['no_tiket'],data['gambar_sebelum'],data['gambar_sesudah'],data['keterangan'],data['latitude'],data['longitude']))
    db.commit()

def isApproved(idchat):
    global db, cur
    sql="select isApproved from UserApproval where idUserApproval='"+str(idchat)+"'"
    cur.execute(sql)
    records = cur.fetchall()
    return records

def insert_row_user(data):
    global db, cur
    sql=""
    cur.execute(sql)
    db.commit()
    db.close()

def update_row_odp(tiket,dist):
    global db, cur
    sql="update mytable set odpa_before='{}-a', odpa_process='{}-b', odpa_after='{}-c',odpb_before='{}-a', odpb_process='{}-b', odpb_after='{}-c',odpc_before='{}-a', odpc_process='{}-b', odpc_after='{}-c', saluran_before='{}-a', saluran_process='{}-b', saluran_after='{}-c', tiang_before='{}-a', tiang_process='{}-b', tiang_after='{}-c', longitude_u={}, latitude_u={}, distance={}, updated_by={}, updated_date=SYSDATE(),keterangan='{}' where ticket_id='{}'".format(str(tiket.noTiket)+'-ODPA',str(tiket.noTiket)+'-ODPA',str(tiket.noTiket)+'-ODPA',str(tiket.noTiket)+'-ODPB',str(tiket.noTiket)+'-ODPB',str(tiket.noTiket)+'-ODPB',str(tiket.noTiket)+'-ODPC',str(tiket.noTiket)+'-ODPC',str(tiket.noTiket)+'-ODPC',str(tiket.noTiket)+'-saluran',str(tiket.noTiket)+'-saluran',str(tiket.noTiket)+'-saluran',str(tiket.noTiket)+'-tiang',str(tiket.noTiket)+'-tiang',str(tiket.noTiket)+'-tiang',str(tiket.longitude),str(tiket.latitude),str(dist),tiket.chatId,tiket.keterangan,tiket.noTiket)
    cur.execute(sql)
    db.commit()

def select_review(tiket):
    global db, cur
    sql="select odpa_before, odpa_process, odpa_after,odpb_before, odpb_process, odpb_after,odpc_before, odpc_process, odpc_after, saluran_before, saluran_process, saluran_after, tiang_before, tiang_process, tiang_after, YEAR(updated_date), MONTH(updated_date) from mytable where ticket_id='{}'".format(tiket.noTiket)
    cur.execute(sql)
    empty=()
    records = cur.fetchall()
    if(records==empty):
        return None
    else:
        return records[0]
    
def daftar(chatid,array):
    global db, cur
    sql="INSERT INTO userapproval VALUES ('{}','{}','{}','{}',1)".format(str(chatid),array[0],array[1].upper(),array[2].upper())
    cur.execute(sql)
    db.commit()

def select_ticket(ticket):
    global db, cur
    sql="select ticket_id,ODP, longitude, latitude from mytable where ticket_id='{}'".format(str(ticket))
    cur.execute(sql)
    empty=()
    records = cur.fetchall()
    if(records==empty):
        return None
    else:
        return records[0]