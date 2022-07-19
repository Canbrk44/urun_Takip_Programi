# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 01:06:26 2022

@author: Smurf
"""

import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from Anasayfa import *

#------------------Uygulama Yarat----------------------#
#------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

#------------------VeriTabanı Yarat----------------------#
#--------------------------------------------------------#
import sqlite3
global curs
global conn

conn=sqlite3.connect("kardesler.db")
curs=conn.cursor()
curs.execute("CREATE TABLE IF NOT EXISTS project (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,u_kod INTEGER NOT NULL,u_adi TEXT NOT NULL,birim_fiyat REAL NOT NULL,stok_miktar INTEGER NOT NULL,u_aciklama TEXT,katagori TEXT NOT NULL )")
conn.commit()
#------------------Kayıt Yarat---------------------------#
#--------------------------------------------------------#
def EKLE():
    ürün_kodu = int(ui.line_urunkodu.text())
    ürün_adi = ui.line_urunadi.text()
    birim_fiyat= float(ui.line_birimfiyati.text())
    stok_miktar = int(ui.line_stokMiktari.text())
    ürün_aciklama=ui.line_urunaciklamasi.text()
    ürün_katagori=ui.combo_urunkatagori.currentText()
    ui.line_urunkodu.clear()
    ui.line_urunadi.clear()
    ui.line_stokMiktari.clear()
    ui.line_birimfiyati.clear()
    ui.line_urunaciklamasi.clear()
    
    try:
        curs.execute("INSERT INTO project (u_kod,u_adi,birim_fiyat,stok_miktar,u_aciklama,katagori)VALUES(?,?,?,?,?,?)",(ürün_kodu,ürün_adi,birim_fiyat,stok_miktar,ürün_aciklama,ürün_katagori))
        conn.commit()
        ui.statusbar.showMessage("Ürün Başarıyla Eklendi")
        LISTELE()
    except Exception as HATA:
        ui.statusbar.showMessage("Ürün Eklenme Sırasında Hata!!")
        
#--------------------Listele--------------------------------------------#
#-----------------------------------------------------------------------# 
def LISTELE():
    ui.table_bilgileri.clear()
    ui.table_bilgileri.setHorizontalHeaderLabels(('ID','ÜRÜN KODU','ÜRÜN ADI','BİRİM FİYATI','STOK MİKTARI','ÜRÜN AÇIKLAMASI','ÜRÜN KATAGORİSİ')) 
    ui.table_bilgileri.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM project")
    for satirIN,satirVAL in enumerate(curs):
        for sutunIN,sutunVAL in enumerate(satirVAL):
            ui.table_bilgileri.setItem(satirIN, sutunIN, QTableWidgetItem(str(sutunVAL)))
LISTELE()
#--------------------Kayıt-Sil--------------------------------------------#
#-------------------------------------------------------------------------# 
def SIL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Silmek İstediğinize Emin misiniz ?",QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.table_bilgileri.selectedItems()
        silinecek=secili[1].text()
        try:
            curs.execute("DELETE FROM project WHERE u_kod = '%s' " %(silinecek))
            conn.commit()
            LISTELE()
            ui.statusbar.showMessage("Kayıt Başarıyla Silinmiştir")
        except Exception as HATA:
            ui.statusbar.showMessage("Kayıt Silme İşlemi Tamamlanamadı !"+str(HATA))
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")
        
#--------------------Kayıt-Sil--------------------------------------------#
#-------------------------------------------------------------------------# 
def ARA():
    aranan1=ui.line_urunadi.text()
    aranan2=ui.line_urunkodu.text()
    curs.execute("SELECT * FROM project WHERE u_adi = ? OR u_kod = ?",(aranan1,aranan2))
    conn.commit()
    ui.table_bilgileri.clear()
    
    for satirIN,satırVAL in enumerate(curs):
        for sutIN,sutVal in enumerate(satırVAL):
            ui.table_bilgileri.setItem(satirIN, sutIN, QTableWidgetItem(str(sutVal)))
            

#--------------------Güncelle------------------------------------------------#
#-------------------------------------------------------------------------#
def GUNCELLE():
    cevap=QMessageBox.question(penAna,"KAYIT Güncelle ","Güncellemek İstediğinize Emin misiniz ? ", QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        try:
            secili=ui.table_bilgileri.selectedItems()
            ID=int(secili[0].text())
            u_kod=ui.line_urunkodu.text()
            u_ad=ui.line_urunadi.text()
            birimF=ui.line_birimfiyati.text()
            stok_miktar=ui.line_stokMiktari.text()
            u_ack=ui.line_urunaciklamasi.text()
            katagori=ui.combo_urunkatagori.currentText()
            curs.execute("UPDATE project SET u_kod=?,u_adi=?,birim_fiyat=?,stok_miktar=?,u_aciklama=?,katagori=?",(u_kod,u_ad,birimF,stok_miktar,u_ack,katagori))      
            conn.commit()
            LISTELE()
        except Exception as HATA:
            ui.statusbar.showMessage("Kayıt Güncellenemedi")
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")
            
        
#--------------------DOLDUR----------------------------------------------------#
#------------------------------------------------------------------------------#
def KatList():
    katagori=ui.combo_listele.currentText()
    curs.execute("SELECT * FROM project WHERE katagori = ?",(katagori,))
    conn.commit()
    ui.table_bilgileri.clear()
    for satirIN,satırVAL in enumerate(curs):
        for sutIN,sutVal in enumerate(satırVAL):
            ui.table_bilgileri.setItem(satirIN, sutIN, QTableWidgetItem(str(sutVal)))
            
#--------------------DOLDUR----------------------------------------------------#
#------------------------------------------------------------------------------#

def DOLDUR():
    secili=ui.table_bilgileri.selectedItems()
    ui.line_urunkodu.setText(secili[1].text())
    ui.line_urunadi.setText(secili[2].text())
    ui.line_birimfiyati.setText(secili[3].text())
    ui.line_stokMiktari.setText(secili[4].text())
    ui.line_urunaciklamasi.setText(secili[5].text())
    ui.combo_urunkatagori.setCurrentText(secili[6].text())
    
    
#------------------Buton Action--------------------------#
#--------------------------------------------------------#
ui.Buton_ekle.clicked.connect(EKLE) 
ui.buton_listele.clicked.connect(LISTELE)
ui.buton_sil.clicked.connect(SIL)
ui.Buton_ara.clicked.connect(ARA)
ui.table_bilgileri.itemSelectionChanged.connect(DOLDUR)
ui.buton_gncelle.clicked.connect(GUNCELLE)
ui.buton_katliste.clicked.connect(KatList)












































sys.exit(Uygulama.exec_())