# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:32:43 2019

@author: Ditzy
"""

import json 
class Keyboard():
    data2={"keyboard": [["/input_keterangan"],["/input_gambar_ODP-RP"],["/input_gambar_saluran_penanggal"],["/input_gambar_tiang"],["/input_lokasi"],["/review_tiket"],["/review_web"],["/kirim_contoh"]],"one_time_keyboard": True,"resize_keyboard": True}
    json_all_comm=json.dumps(data2)
    data6={"keyboard": [["ODC A"],["ODC B"],["/cancel"]],"one_time_keyboard": True}
    data7={"keyboard": [["ODP A"],["ODP B"],["ODP C"],["/cancel"]],"one_time_keyboard": True}
    data8={"keyboard": [["sebelum"],["progres"],["sesudah"],["/cancel"]],"one_time_keyboard": True}
    json_odc_lv2=json.dumps(data6)
    json_odp_lv2=json.dumps(data7)
    json_bfraft=json.dumps(data8)
    
    def __init__(self, json_lvl_1=json_all_comm,json_ODP_lvl_2=json_odp_lv2,json_ODPA_lvl_3=json_bfraft,json_ODPB_lvl_3=json_bfraft,json_ODPC_lvl_3=json_bfraft,json_tiang_lvl_2=json_bfraft, json_saluran_lvl_2=json_bfraft):
        self.json_lvl_1=json_lvl_1
        self.json_ODP_lvl_2=json_ODP_lvl_2
        self.json_ODPA_lvl_3=json_ODPA_lvl_3
        self.json_ODPB_lvl_3=json_ODPB_lvl_3
        self.json_ODPC_lvl_3=json_ODPC_lvl_3
        self.json_tiang_lvl_2=json_tiang_lvl_2
        self.json_saluran_lvl_2=json_saluran_lvl_2
    
    def cekKeyboardGambar(self):
        a= json.dumps({"keyboard": [["/cancel"]], "one_time_keyboard": True})
        '''
        if(self.json_ODCA_lvl_3==a):
            self.json_ODC_lvl_2=self.json_ODC_lvl_2.replace('["ODC A"], ','')
        if(self.json_ODCB_lvl_3==a):
            self.json_ODC_lvl_2=self.json_ODC_lvl_2.replace('["ODC B"], ','')
        '''
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
        self.json_lvl_1=self.json_all_comm
        self.json_ODP_lvl_2=self.json_odp_lv2
        self.json_ODPA_lvl_3=self.json_bfraft
        self.json_ODPB_lvl_3=self.json_bfraft
        self.json_ODPC_lvl_3=self.json_bfraft
        self.json_tiang_lvl_2=self.json_bfraft
        self.json_saluran_lvl_2=self.json_bfraft