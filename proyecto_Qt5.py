import sys, re, smtplib, email,os
from os import getcwd,makedirs
import time
import imagenes
import pymysql
import threading
from PyQt5.QtWidgets import QApplication,QGridLayout, QMainWindow,QMessageBox,QDialog,QPushButton,QLabel,QLineEdit,QSpinBox,QAction,QTableWidget,QTableWidgetItem,QFileDialog, QCheckBox, QPlainTextEdit

from PyQt5 import uic
from PIL import Image #para tratamiento de imagenes
import matplotlib.pyplot as plt #para mapa bits(RBG) histogramas, graicas de imagenes
from PyQt5.QtGui import QFont,QIcon, QPixmap #para trabajar con fuentes
from PyQt5.QtCore import Qt , pyqtSignal,QFile,QByteArray, QIODevice,QBuffer  ,QUrl, QFileInfo #para trabajar con tipos de cursor
from PyQt5.QtSql import QSqlDatabase,QSqlQuery #para trabajar con base de datos
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

import ctypes #para obtener alto y ancho del escritorio
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#&&&&&&&&&&&& VARIABLES GLOBALES &&&&&&&&&&&

id_emple=""
nombre_imag=Image.open("imagen/conec16x16.png")
region=""
nombre_de_la_imagen=""
url_img=""
url_img2=""
id_imagen=""
id_imgT1=""
id_termo=""
url_array1=[]
url_array2=[]

    
comb_color=""
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class Barra_progreso(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("barra_progreso.ui", self)
  self.setWindowTitle("Barra De Progreso")

  total_progreso=300
  
  if comb_color!="Normal":
    self.progressBar.setMaximum(total_progreso)
    for i in range(total_progreso+1):
      load_progreso=i
      self.progressBar.setValue(load_progreso)





class Login(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("login.ui", self)
  self.setWindowFlags(Qt.FramelessWindowHint)
  self.setWindowTitle("Login")
  self.ingresar.clicked.connect(self.ingresar_sis) 
  self.cerrar_prog.clicked.connect(self.Fin_cerrar_Prog)

 def ingresar_sis(self):
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   usu=self.txt_usuario.text()
   pas=self.txt_clave.text()
   if(usu!="" and pas!=""):
       sql = "SELECT nombres,apellidos,privilegio,E.id_empleado,U.id_usuario FROM usuarios U inner join empleados E on E.id_empleado=U.id_empleado inner join privilegio P on P.id_privilegio=U.id_privilegio where U.usuario='"+usu+"' and U.clave='"+pas+"' and E.id_estado='1' "
       cursor.execute(sql)
       row1 = cursor.fetchone()
       if(row1):
         nom=str(row1[0])
         ape=str(row1[1])
         priv=str(row1[2])
         id_emple=str(row1[3])
         id_usu=str(row1[4])
         self.close()
         QMessageBox.question(self, priv, "BIENVENIDO "+nom+" "+ape+"... ", QMessageBox.Yes)
       else:
         QMessageBox.question(self, 'INFORMACION', "El Usuario o Contraseña son Erroneos... ", QMessageBox.Yes)
   else:
       QMessageBox.question(self, 'INFORMACION', "Porfavor llene todos los Campos... ", QMessageBox.Yes)

 def Fin_cerrar_Prog(self):
     resultado=QMessageBox.question(self,"Salir...","¿Seguro que quiere Cerrar el Programa?",QMessageBox.Yes|QMessageBox.No)
     if resultado==QMessageBox.Yes:sys.exit()

     









class Union_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("union_imagenes.ui", self)
  self.setWindowTitle("Union de Imagenes - Interpolación ")
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   fecha = QTableWidgetItem(str(row1[8]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,latitu)
   self.table.setItem(i,3,longitu)
   self.table.setItem(i,4,hecta)
   self.table.setItem(i,5,parce)  
   i=i+1

  self.buscar.clicked.connect(self.buacar) 
  self.mostrar_imagen.clicked.connect(self.muestra_img)  
  self.btn_unir.clicked.connect(self.Union)  
##  self.guardar_interpolacion.clicked.connect(self.guardar_interpolado)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(6)
   self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%'or fecha like '%"+dato+"%'  or latitud like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))    
    fecha = QTableWidgetItem(str(row1[8]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
   
    self.table.setItem(i,0,codigo)    
    self.table.setItem(i,1,fecha)
    self.table.setItem(i,2,latitu)
    self.table.setItem(i,3,longitu)
    self.table.setItem(i,4,hecta)
    self.table.setItem(i,5,parce)  
    i=i+1

 def muestra_img(self):
  global nombre_imag
  global nombre_de_la_imagen
  global url_img
  global url_img2
  global id_imagen
  global url_array1
  global url_array2
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  k=0
  if self.table.selectionModel().selectedRows() :
    rows=self.table.selectionModel().selectedRows()
    index=[]
    for i in rows:
      index.append(i.row())
    for i in index:       
      idI=self.table.item(i,0).text()      
      print("id-cedula="+idI)
      sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
      cursor.execute(sql2)
      row2 = cursor.fetchone()
      url_array1.append(str(row2[0]))
      url_array2.append(str(row2[1]))
      k+=1

    l=0    
    for i in url_array2:
##      nada=QPixmap("").scaled(100, 40, Qt.KeepAspectRatio,Qt.SmoothTransformation)
##      self.label1.setPixmap(nada)  para poner en blanco
##      self.label2.setText("-")      
      
      if l==0:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label1.setPixmap(foto)
      if l==1:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label2.setPixmap(foto)
      if l==2:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label3.setPixmap(foto)
      if l==3:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label4.setPixmap(foto)
      if l==4:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label5.setPixmap(foto)
      if l==5:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label6.setPixmap(foto)
      if l==6:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label7.setPixmap(foto)
      if l==7:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label8.setPixmap(foto)
      if l==8:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label9.setPixmap(foto)
      if l==9:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label10.setPixmap(foto)
      if l==10:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label11.setPixmap(foto)
      if l==11:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label12.setPixmap(foto)
      if l==12:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label13.setPixmap(foto)
      if l==13:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label14.setPixmap(foto)
      if l==14:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label15.setPixmap(foto)
      if l==15:
        foto=QPixmap(i).scaled(100, 50, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label16.setPixmap(foto)
        
      l+=1
    
      
  else :
    print("seleccione una imagen")
    QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

 def Union(self):
    #for i in url_array2:
        imagen1 = Image.open(url_array2[0])
        imagen2 = Image.open(url_array2[1])
        imagen3 = Image.open(url_array2[2])
        imagen4 = Image.open(url_array2[3])
        imagen5 = Image.open(url_array2[0])


        def changeImageSize(maxWidth,maxHeight,image):    
            widthRatio  = maxWidth/image.size[0]
            heightRatio = maxHeight/image.size[1]
            newWidth    = int(widthRatio*image.size[0])
            newHeight   = int(heightRatio*image.size[1])
            newImage    = image.resize((newWidth, newHeight))
            return newImage
          # Make the sizes of images uniform
        imagen3 = changeImageSize(int(imagen1.size[0]), int(imagen1.size[1]), imagen3)
        

        img_acum=int(imagen1.size[0])+int(imagen2.size[0])+int(imagen3.size[0])+int(imagen4.size[0])
        img_acum2=int(imagen1.size[1])+int(imagen1.size[1])
        final = Image.new("RGB",(img_acum,img_acum2),"black")

        final.paste(imagen1, (0,0))
        final.paste(imagen2, (int(imagen1.size[0]),0))
        final.paste(imagen3, (int(imagen1.size[0])+int(imagen2.size[0]),0))
        final.paste(imagen4, (img_acum-int(imagen4.size[0]),0))                                                               
        final.paste(imagen5, (0,int(imagen1.size[1])))
        final.show()
        final.save("img_union/img-unidas2.jpg")

        foto_final = Image.open("img_union/img-unidas2.jpg")
        foto_final = changeImageSize(1200, 900, foto_final)
        foto_final.save("img_union/img-unidas2.jpg")
        foto_final=QPixmap("img_union/img-unidas2.jpg").scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.imag_unida.setPixmap(foto_final)
        

    
  












class Lista_termo_division_color(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_division_color.ui", self)
  self.setWindowTitle("Lista De División De Color - Termografia")  
  self.table.setColumnCount(4)
  self.table.setHorizontalHeaderLabels(['ID','Fecha','Titulo','Descripcion'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM termografia_divi_color  Order by fecha ASC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   id_TD = QTableWidgetItem(str(row1[0]))
   fecha = QTableWidgetItem(str(row1[1]))
   titulo = QTableWidgetItem(str(row1[2]))
   descrip = QTableWidgetItem(str(row1[3]))

   self.table.setItem(i,0,id_TD)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,titulo)
   self.table.setItem(i,3,descrip)
   i=i+1
  conn.close()
  self.buscar.clicked.connect(self.buacar)
  self.cerrar.clicked.connect(self.cancelar_cerrar) 
  self.actualiza.clicked.connect(self.Actualizar) 
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(4)
   self.table.setHorizontalHeaderLabels(['ID','Fecha','Titulo','Descripcion'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM termografia_divi_color where fecha like '%"+dato+"%' or titulo like '%"+dato+"%' Order by fecha ASC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
       print("consulta exitosa..")
       self.table.insertRow(i)
       id_TD = QTableWidgetItem(str(row1[0]))
       fecha = QTableWidgetItem(str(row1[1]))
       titulo = QTableWidgetItem(str(row1[2]))
       descrip = QTableWidgetItem(str(row1[3]))
       

       self.table.setItem(i,0,id_TD)
       self.table.setItem(i,1,fecha)
       self.table.setItem(i,2,titulo)
       self.table.setItem(i,3,descrip)
       i=i+1
     
 def cancelar_cerrar(self):
  self.close()
  
 def Actualizar(self):
  if self.table.selectedItems():
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      columna=self.table.currentColumn()
      row=self.table.currentRow()
      idTD=self.table.item(row,0).text()
      value=self.table.currentItem().text()
      columnas=['id_termografia_divi_color','fecha','titulo','descripcion']
      colu=columnas[columna]
      print(colu+" = "+value+" id:"+idTD)
      sql = "UPDATE termografia_divi_color SET "+columnas[columna]+"='"+str(value)+"' WHERE id_termografia_divi_color='"+str(idTD)+"'"
      dat=cursor.execute(sql)
      conn.commit()
      if dat==False:
       print("modificaion fallida..")
      else:
       print("modificaion exitosa..")
       QMessageBox.information(self, "Tabla Modificada", "Modificación Exitosa", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero Edite un Registro", QMessageBox.Yes)
    
  








class Lista_termo_procentaje_color(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_porcentaje_color.ui", self)
  self.setWindowTitle("Lista De Porcentaje De Color - Termografia")  
  self.table.setColumnCount(7)
  self.table.setHorizontalHeaderLabels(['Fecha','rojo','Amarillo','Naranja','Blanco','Azul','Morado'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM termografia_proce_color  Order by fecha ASC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   fecha = QTableWidgetItem(str(row1[1]))
   rojo = QTableWidgetItem(str(row1[2]))
   amar = QTableWidgetItem(str(row1[3]))
   naran = QTableWidgetItem(str(row1[4]))
   blan = QTableWidgetItem(str(row1[5]))
   azul = QTableWidgetItem(str(row1[6]))
   mora = QTableWidgetItem(str(row1[7]))

   self.table.setItem(i,0,fecha)
   self.table.setItem(i,1,rojo)
   self.table.setItem(i,2,amar)
   self.table.setItem(i,3,naran)
   self.table.setItem(i,4,blan)
   self.table.setItem(i,5,azul)
   self.table.setItem(i,6,mora)
   i=i+1
  conn.close()
  self.buscar.clicked.connect(self.buacar)
  self.cerrar.clicked.connect(self.cancelar_cerrar)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(7)
   self.table.setHorizontalHeaderLabels(['Fecha','rojo','Amarillo','Naranja','Blanco','Azul','Morado'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM termografia_proce_color where fecha like '%"+dato+"%' Order by fecha ASC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
       print("consulta exitosa..")
       self.table.insertRow(i)
       fecha = QTableWidgetItem(str(row1[1]))
       rojo = QTableWidgetItem(str(row1[2]))
       amar = QTableWidgetItem(str(row1[3]))
       naran = QTableWidgetItem(str(row1[4]))
       blan = QTableWidgetItem(str(row1[5]))
       azul = QTableWidgetItem(str(row1[6]))
       mora = QTableWidgetItem(str(row1[7]))

       self.table.setItem(i,0,fecha)
       self.table.setItem(i,1,rojo)
       self.table.setItem(i,2,amar)
       self.table.setItem(i,3,naran)
       self.table.setItem(i,4,blan)
       self.table.setItem(i,5,azul)
       self.table.setItem(i,6,mora)
       i=i+1
 
  
 def cancelar_cerrar(self):
  self.close()
  









class Lista_gps(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_gps.ui", self)
  self.setWindowTitle("Lista GPS")  
  self.table.setColumnCount(5)
  self.table.setHorizontalHeaderLabels(['Latitud','Longitud','Hectarea','Parcela','Fecha'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT latitud,longitud,hectarea,parcela,fecha FROM captura_imagen  Order by fecha ASC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   lati = QTableWidgetItem(str(row1[0]))
   longi = QTableWidgetItem(str(row1[1]))
   hect = QTableWidgetItem(str(row1[2]))
   parc = QTableWidgetItem(str(row1[3]))
   fecha = QTableWidgetItem(str(row1[4]))

   self.table.setItem(i,0,lati)
   self.table.setItem(i,1,longi)
   self.table.setItem(i,2,hect)
   self.table.setItem(i,3,parc)
   self.table.setItem(i,4,fecha)
   i=i+1
  conn.close()
  self.buscar.clicked.connect(self.buacar)
  self.cerrar.clicked.connect(self.cancelar_cerrar)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(5)
   self.table.setHorizontalHeaderLabels(['Latitud','Longitud','Hectarea','Parcela','Fecha'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT latitud,longitud,hectarea,parcela,fecha FROM captura_imagen where latitud like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' or fecha like '%"+dato+"%' Order by fecha ASC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
       print("consulta exitosa..")
       self.table.insertRow(i)
       lati = QTableWidgetItem(str(row1[0]))
       longi = QTableWidgetItem(str(row1[1]))
       hect = QTableWidgetItem(str(row1[2]))
       parc = QTableWidgetItem(str(row1[3]))
       fecha = QTableWidgetItem(str(row1[4]))

       self.table.setItem(i,0,lati)
       self.table.setItem(i,1,longi)
       self.table.setItem(i,2,hect)
       self.table.setItem(i,3,parc)
       self.table.setItem(i,4,fecha)
       i=i+1
   
 def cancelar_cerrar(self):
  self.close()
    









class Interpolacion_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("interpolacion.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   fecha = QTableWidgetItem(str(row1[8]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,latitu)
   self.table.setItem(i,3,longitu)
   self.table.setItem(i,4,hecta)
   self.table.setItem(i,5,parce)  
   i=i+1

  self.buscar.clicked.connect(self.buacar) 
  self.mostrar_imagen.clicked.connect(self.muestra_img)  
  self.interpolar.clicked.connect(self.interpolado_img)  
  self.guardar_interpolacion.clicked.connect(self.guardar_interpolado)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(6)
   self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%'or fecha like '%"+dato+"%'  or latitud like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))    
    fecha = QTableWidgetItem(str(row1[8]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
   
    self.table.setItem(i,0,codigo)    
    self.table.setItem(i,1,fecha)
    self.table.setItem(i,2,latitu)
    self.table.setItem(i,3,longitu)
    self.table.setItem(i,4,hecta)
    self.table.setItem(i,5,parce)  
    i=i+1

 def muestra_img(self):
  global nombre_imag
  global nombre_de_la_imagen
  global url_img
  global url_img2
  global id_imagen
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  if self.table.selectionModel().selectedRows() :
    rows=self.table.selectionModel().selectedRows()
    index=[]
    for i in rows:
      index.append(i.row())
    index.sort(reverse=True)
    for i in index:
      idI=self.table.item(i,0).text()
      print("id-cedula="+idI)
    id_imagen=idI
    sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
    cursor.execute(sql2)
    row2 = cursor.fetchone()
    img1=str(row2[0])
    img2=str(row2[1])
    
    foto=QPixmap(img1).scaled(200, 150, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    nombre_de_la_imagen=os.path.basename(img1)
    self.imag_1.setPixmap(foto)
    url_img=img1
      
    foto=QPixmap(img2).scaled(200, 150, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    nombre_de_la_imagen=os.path.basename(img2)
    self.imag_2.setPixmap(foto)
    url_img2=img2
      
  else :
    print("seleccione una imagen")
    QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

      
 def interpolado_img(self):
  global url_img
  global url_img2
  global nombre_de_la_imagen
  nom_cade=str(nombre_de_la_imagen)
  nom_cade=nom_cade.split(".")
  nom_cade=nom_cade[0]
  
  ####### interpolacion ########
  # transparentar imagen  y convirtiendo a png
  img=plt.imread(url_img2)
  plt.imshow(img)
  cropped_img=img[0:3000,0:3000]
  img=plt.imsave('img_interpolada/interpolado2.png',cropped_img)  

  img2=plt.imread('img_interpolada/interpolado2.png')
  opr=img2 * 0.864 # 0.964 nivel de transparencia imagen 
  plt.imshow(opr)
  #plt.show()
  img2=plt.imsave('img_interpolada/interpolado2.png',opr)  
  image1 = Image.open(url_img)
  image1.save('img_interpolada/interpolado1.png')

  image1 = Image.open('img_interpolada/interpolado1.png')
  image2 = Image.open('img_interpolada/interpolado2.png')
 

  # Function to change the image size
  def changeImageSize(maxWidth,maxHeight,image):    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]
    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])
    newImage    = image.resize((newWidth, newHeight))
    return newImage
  # Make the sizes of images uniform
  image3 = changeImageSize(1300, 900, image1)
  image4 = changeImageSize(1300, 900, image2)
  # Make sure the images have alpha channels
  image3.putalpha(1)
  image4.putalpha(1)
  # Do an alpha composite of image4 over image3
  alphaComposited = Image.alpha_composite(image3, image4)
  # Display the alpha composited image  
  alphaBlended = Image.blend(image4, image3,.2)
  # armado,presentacion y guardado 
  interp1=alphaComposited.convert ("RGB")
  interp2=alphaBlended.convert ("RGB")
  interp1.show()
  interp2.show()
  interp1.save('img_interpolada/'+nom_cade+'_1.png') #no guarda bien
  interp2.save('img_interpolada/'+nom_cade+'_2.png')  #no guarda bien  
  
  foto=QPixmap('img_interpolada/'+nom_cade+'_1.png').scaled(450, 400, Qt.KeepAspectRatio,Qt.SmoothTransformation)
  #nombre_de_la_imagen=os.path.basename(img2)
  self.imag_interpo.setPixmap(foto)
  #url_img2=img2

 def guardar_interpolado(self):
  global nombre_de_la_imagen
  global id_imagen
  nom_cade=str(nombre_de_la_imagen)
  nom_cade=nom_cade.split(".")
  nom_cade=nom_cade[0]
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  
  fecha= time.strftime("%Y-%m-%d")
  sql1 = "SELECT imagen_inter FROM interpolacion where id_captura_imagen='"+str(id_imagen)+"' "
  compro=cursor.execute(sql1)
  if compro==False:
      sql2 = "INSERT INTO interpolacion(fecha,imagen_inter,id_captura_imagen) VALUES('"+str(fecha)+"','img_interpolada/"+str(nom_cade)+"_1.png','"+str(id_imagen)+"')"
      cursor.execute(sql2)
      conn.commit()
      QMessageBox.question(self, 'INFORMACION', "Registro GUARDADO correctamente", QMessageBox.Yes)
  else:
      QMessageBox.question(self, 'INFORMACION', "Este Registro ya fue GUARDADO", QMessageBox.Yes)













class Termografia_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("termografica.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   fecha = QTableWidgetItem(str(row1[8]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,latitu)
   self.table.setItem(i,3,longitu)
   self.table.setItem(i,4,hecta)
   self.table.setItem(i,5,parce)  
   i=i+1

  self.buscar.clicked.connect(self.buacar) 
  self.mostrar_imagen.clicked.connect(self.muestra_img) 
  self.histograma.clicked.connect(self.histograma_img) 
  self.porcentajes_color.clicked.connect(self.escala_max) 
  self.division_color.clicked.connect(self.escala_dividida)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(6)
   self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%'or fecha like '%"+dato+"%'  or latitud like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))    
    fecha = QTableWidgetItem(str(row1[8]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
   
    self.table.setItem(i,0,codigo)    
    self.table.setItem(i,1,fecha)
    self.table.setItem(i,2,latitu)
    self.table.setItem(i,3,longitu)
    self.table.setItem(i,4,hecta)
    self.table.setItem(i,5,parce)  
    i=i+1

 def muestra_img(self):
  global nombre_imag
  global nombre_de_la_imagen
  global url_img
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  if self.table.selectionModel().selectedRows() :
    rows=self.table.selectionModel().selectedRows()
    index=[]
    for i in rows:
      index.append(i.row())
    index.sort(reverse=True)
    for i in index:
      idI=self.table.item(i,0).text()
      print("id-cedula="+idI)
   
    sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
    cursor.execute(sql2)
    row2 = cursor.fetchone()
    img1=str(row2[0])
    img2=str(row2[1])
    if self.img_normal.isChecked():
      foto=QPixmap(img1).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img1)
      imagen_show = Image.open(img1)
      imagen_show.show()
      self.lblimgen.setPixmap(foto)
      url_img=img1
      self.histograma.setEnabled(True)
      self.porcentajes_color.setEnabled(True)
      self.division_color.setEnabled(True)
      
        
    if self.img_termica.isChecked():
      foto=QPixmap(img2).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img2)
      imagen_show = Image.open(img2)
      imagen_show.show()
      self.lblimgen.setPixmap(foto)
      url_img=img2
      self.histograma.setEnabled(True)
      self.porcentajes_color.setEnabled(True)
      self.division_color.setEnabled(True)
      
  else :
    print("seleccione una imagen")
    QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

      
#$$$$$$$$$$$$$$$$ HISTOGRAMA    

 def histograma_img(self):
    print("12345")
    global url_img
    def getRed(redVal):
        return '#%02x%02x%02x' % (redVal, 0, 0)
    def getGreen(greenVal):
        return '#%02x%02x%02x' % (0, greenVal, 0)
    def getBlue(blueVal):
        return '#%02x%02x%02x' % (0, 0, blueVal)
    # Create an Image with specific RGB value
    image = Image.open(url_img) 

    # Modify the color of two pixels
    image.putpixel((0,1), (1,1,5))
    image.putpixel((0,2), (2,1,5))
    # Display the image
    #image.show()
    # Get the color histogram of the image
    histogram = image.histogram()
    # Take only the Red counts
    l1 = histogram[0:256]
    # Take only the Blue counts
    l2 = histogram[256:512]
    # Take only the Green counts
    l3 = histogram[512:768]
    plt.figure(0)
    # R histogram
    for i in range(0, 256):
        plt.bar(i, l1[i], color = getRed(i), edgecolor=getRed(i), alpha=0.3)
    # G histogram
    plt.figure(0)
    for i in range(0, 256):
        plt.bar(i, l2[i], color = getGreen(i), edgecolor=getGreen(i),alpha=0.3)
    # B histogram
    plt.figure(0)
    for i in range(0, 256):
        plt.bar(i, l3[i], color = getBlue(i), edgecolor=getBlue(i),alpha=0.3)
    plt.show()

    
 def escala_max(self):
    global url_img  
    if self.table.selectionModel().selectedRows() and url_img!="":
      global id_imgT1
      print("entra a capturar dato")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        id_imgT1=self.table.item(i,0).text()
        print("id-cedula="+id_imgT1)    
      self.termo_porcen=Termo_porcentaje()
      self.termo_porcen.exec_()
    else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

 def escala_dividida(self):
    global url_img  
    if self.table.selectionModel().selectedRows() and url_img!="":
      global id_imgT1
      print("entra a capturar dato")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        id_imgT1=self.table.item(i,0).text()
        print("id-cedula="+id_imgT1)    
      self.termo_divi=Termo_division()
      self.termo_divi.exec_()
    else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

   

#####################################
      #############################333
      #####################3

class Termo_porcentaje(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("termo_porcentaje.ui", self)
  self.setWindowTitle("Porcentajes Por Color De Imagene")
  global id_termo

  foto=QPixmap(url_img).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
  self.lblimgen.setPixmap(foto)
  #ruta=('imagen/atardecer.jpg')
  img=Image.open(url_img)
  #img.show()
  QMessageBox.question(self, 'INFORMACION', "EL Proceso puede tardar algunos segundos...", QMessageBox.Yes)
  img2=img
  i=0
  r2=0
  b2=0
  g2=0
  a2=0
  r3=0
  b3=0
  g3=0
  a3=0
  b4=0
  amari=0
  amari2=0
  azu=0
  azu2=0
  anar=0
  anar2=0
  mora=0
  mora2=0
  roj=0
  roj2=0
  
  while i<img2.size[0]:
      j=0      
      while j<img2.size[1]:
         #r,g,b,a=img2.getpixel((i,j))   #para  .png
          r,g,b=img2.getpixel((i,j))  
          #print(r,b,r,a)  #para  .png
          r2+=+r
          if r>200:
              r3+=+1
          g2+=+g
          if g>100:
              g3+=+1
          b2+=+b
          if r>110 and g<100 and b<90 :
              roj+=+1
              lo=(r+g+b)/2
              roj2+=+int(lo)
              
          if r>155 and (g>140 and g<250) and b<125:
              amari+=+1
              llo=(r+g+b)/2
              amari2+=+int(llo)
              
          if r>225 and g>225 and b>215:
              b3+=+1
              b4+=+b
              #a2+=+a  #para  .png
              #g=(r+g+b+a)/6    #para  .png
          if r<80 and g<80 and b>70:
              azu+=+1
              azu2+=+b
          if r>156 and (g>100 and g<180) and  b<80:
              anar+=+1
              va=(r+g+b)/2
              anar2+=+int(va)
          if (r>50 and r<215) and g<80 and  b>63:
              mora+=+1
              ma=(r+g+b)/2
              mora2+=+int(ma)
              
          g=(r+g+b)/6
          gris=int(g)
          #pixel=tuple([gris,gris,gris,gris])   #para  .png
          pixel=tuple([gris,gris,gris])    
          img2.putpixel((i,j),pixel)
          j+=1
      i+=1
        
  ran=j*i
  r2=r2/ran
  r3=(int(r3)*100)/ran
  g2=g2/ran
  g3=(int(g3)*100)/ran
  b2=b2/ran
  #a2=a2/ran     #para  .png
  #print(int(r2),b2,r2,a2)     #para  .png
  print(int(r2),int(g2),int(b2),)
##  rojo=(int(r2)*100)/255
##  amarillo=(int(r2)+int(g2))/2
##  amarillo=(int(amarillo)*100)/255
  blanco=3

  if roj>0:
      rojo=(int(roj2/roj)*100)/255
  else:
      rojo=0
  print("rojo",roj)    
  rojop=(int(roj)*100)/ran
  
  if amari>0:
      amarillo=(int(amari2/amari)*100)/255
  else:
      amarillo=0
  amarillop=(int(amari)*100)/ran
  
  if b3 > 0 :
       blanco=(int(b4/b3)*100)/255
       b3=(int(b2)*100)/255
       
  if azu>0:
      azul=(int(azu2/azu)*100)/255
  else:
      azul=0
  azulp=(int(azu)*100)/ran

  if anar>0:
      naran=(int(anar2/anar)*100)/255
  else:
      naran=0
  naranp=(int(anar)*100)/ran

  if mora>0:
      morado=(int(mora2/mora)*100)/255
  else:
      morado=0
  moradop=(int(mora)*100)/ran


  
  amarillop2=amarillop-naranp
  if amarillop2<1:
      amarillop2=0
     
  print(int(r2),int(g3))
  self.txt_rojo.setText(str(int(rojo))+" - "+str(int(rojop))+" %")
  self.txt_amarillo.setText(str(int(amarillo))+" - "+str(int(amarillop2))+" %")
  self.txt_blanco.setText(str(int(blanco))+" - "+str(int(b3))+" %")
  self.txt_azul.setText(str(int(azul))+" - "+str(int(azulp))+" %")
  self.txt_naranja.setText(str(int(naran))+" - "+str(int(naranp))+" %")
  self.txt_morado.setText(str(int(morado))+" - "+str(int(moradop))+" %")
  #print("% rojo="+str(int(rojo)),"% amarillo="+str(int(amarillo)),"% blanco="+str(int(blanco)))

  id_img=id_imgT1
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  sql1 = "SELECT id_termografia_proce_color FROM termografia_proce_color where id_captura_imagen='"+str(id_img)+"' "
  compro=cursor.execute(sql1)
  if compro==False:
      print("no existe")
  else:
      row1 = cursor.fetchone()
      id_termo =str(row1[0])
      print("si existe",id_termo)
      self.registro_anali.setEnabled(True)
      
      sql3 = "SELECT fecha,titulo,descripcion FROM detalle_termogra_proce_color where id_termografia_proce_color='"+str(id_termo)+"' "
      compro=cursor.execute(sql3)
      if compro==False:
          print("no existe")
      else:
          row3 = cursor.fetchone()
          fecha =str(row3[0])
          titulo =str(row3[1])
          descrip =str(row3[2])

          txt="Fecha: "+str(fecha)+" \n"+"Titulo:"+str(titulo)+" \n"+"Descripción: \n"+str(titulo)+". "          
          self.mues_anali.setPlainText(txt) #  _fromUtf8()
  
  self.guardar_pro_color.clicked.connect(self.guardar_porcen_img)
  self.registro_anali.clicked.connect(self.Abrir_formu_analisis)
  

 def guardar_porcen_img(self):
   global id_termo  
   id_img=id_imgT1
   rojo=self.txt_rojo.text()
   amarillo=self.txt_amarillo.text()
   blanco=self.txt_blanco.text()
   azul=self.txt_azul.text()
   morado=self.txt_morado.text()
   naranja=self.txt_naranja.text()
   fecha= time.strftime("%Y-%m-%d")
   print("captura de datos exitosa..")
   if rojo!="" and amarillo!="" and blanco!="" and azul!="" and morado!="" and naranja!="" :
     conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
     cursor = conn.cursor()
     sql1 = "SELECT fecha FROM termografia_proce_color where id_captura_imagen='"+str(id_img)+"' "
     compro=cursor.execute(sql1)
     if compro==False:
       sql2 = "INSERT INTO termografia_proce_color(fecha,rojo,amarillo,naranja,blanco,azul,morado,id_captura_imagen) VALUES('"+str(fecha)+"','"+str(rojo)+"','"+str(amarillo)+"','"+str(naranja)+"','"+str(blanco)+"','"+str(azul)+"','"+str(morado)+"','"+str(id_img)+"')"
       dat=cursor.execute(sql2)
       conn.commit()
       sql3 = "SELECT id_termografia_proce_color FROM termografia_proce_color where id_captura_imagen='"+str(id_img)+"' "
       compro=cursor.execute(sql3)
       row1 = cursor.fetchone()
       id_termo =str(row1[0])
       self.registro_anali.setEnabled(True)
       QMessageBox.question(self, 'INFORMACION', "Registro GUARDADO correctamente", QMessageBox.Yes)
     else:
       QMessageBox.question(self, 'INFORMACION', "Este Registro ya fue GUARDADO", QMessageBox.Yes)
   else:
       QMessageBox.question(self, 'INFORMACION', "Llene todos los campos y vuelva a intentarlo", QMessageBox.Yes)

 def Abrir_formu_analisis(self): 
    self.Regis_anali_color_termo=Registro_anali_color_termo()
    self.Regis_anali_color_termo.exec_()

class Registro_anali_color_termo(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("resitro_analisis_color_termo.ui", self)
  self.setWindowTitle("Registro De Analisis Termografia")
  
  self.registrar.clicked.connect(self.Guardar_regis_anali_color_termo)
  self.cancelar.clicked.connect(self.cancelar_cerrar)
  
 def cancelar_cerrar(self):
  self.close()
  
 def Guardar_regis_anali_color_termo(self):
  global id_termo     
  id_termogra=id_termo
  titulo=self.titulo.text()
  descrip=self.descrip.toPlainText()
  fecha= time.strftime("%Y-%m-%d")
  print("captura de datos exitosa..")
  if titulo!="" and descrip!="" :
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    sql1 = "SELECT fecha FROM detalle_termogra_proce_color where id_termografia_proce_color='"+str(id_termogra)+"' "
    print("sdnasjns 125615")
    compro=cursor.execute(sql1)
    if compro==False:
      sql2 = "INSERT INTO detalle_termogra_proce_color(fecha,titulo,descripcion,id_termografia_proce_color) VALUES('"+str(fecha)+"','"+str(titulo)+"','"+str(descrip)+"','"+str(id_termogra)+"')"
      dat=cursor.execute(sql2)
      conn.commit()
      QMessageBox.question(self, 'INFORMACION', "Registro GUARDADO correctamente", QMessageBox.Yes)
    else:
      QMessageBox.question(self, 'INFORMACION', "Este Registro ya fue GUARDADO", QMessageBox.Yes)
  else:
      QMessageBox.question(self, 'INFORMACION', "Llene todos los campos y vuelva a intentarlo", QMessageBox.Yes)

#####################################
      #############################333
      #####################3
      
class Termo_division(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("termo_division.ui", self)
  self.setWindowTitle("División Por Color De Imagenen")

  id_img=id_imgT1
  foto=QPixmap(url_img).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
  self.lblimgen.setPixmap(foto)
  #ruta=('imagen/atardecer.jpg')
  self.combo_colores.addItem("Normal")
  self.combo_colores.addItem("Blanco")
  self.combo_colores.addItem("Azul")
  self.combo_colores.addItem("Rojo")
  self.combo_colores.addItem("Amarillo")
  self.combo_colores.addItem("Naranja")
  self.combo_colores.addItem("Morado")

  #self.combo_colores.selectedItems(self.)  
  self.procesar.clicked.connect(self.proceso_divi_color) 
  self.registro_anali.clicked.connect(self.Abrir_formu_analisis)
  
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  sql3 = "SELECT fecha,titulo,descripcion FROM termografia_divi_color where id_captura_imagen='"+str(id_img)+"' "
  compro=cursor.execute(sql3)
  if compro==False:
       print("no existe")
  else:
       row3 = cursor.fetchone()
       fecha =str(row3[0])
       titulo =str(row3[1])
       descrip =str(row3[2])
       txt="Fecha: "+str(fecha)+" \n"+"Titulo: "+str(titulo)+" \n"+"Descripción: \n"+str(titulo)+". "          
       self.mues_anali.setPlainText(txt) #  _fromUtf8()
  
 def Ver_progre(self):
    global comb_color 
    comb_color=self.combo_colores.currentText()
    self.Barra_progre=Barra_progreso()
    self.Barra_progre.exec_()

  
 def proceso_divi_color(self):     
  img=Image.open(url_img)
  #img.show()
  QMessageBox.question(self, 'INFORMACION', "EL Proceso puede tardar algunos segundos...", QMessageBox.Yes)
  img2=img
  i=0
  anar=0
  anar2=0
  global comb_color
  #thread= threading.Thread(target=self.Ver_progre)
  #thread.start()
      
  comb_color=self.combo_colores.currentText()
  if comb_color=="Normal":
      foto=QPixmap(url_img).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      self.lblimgen.setPixmap(foto)
  else:
      
      while i<img2.size[0]:
          j=0
          load_progreso=i
          while j<img2.size[1]:
              
              r,g,b=img2.getpixel((i,j))
        # PARA EL COLOR NARANJA
              if comb_color=="Naranja":
                  if r>156 and (g>100 and g<180) and  b<80:
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])
        
        # PARA EL COLOR MORADO
              if comb_color=="Morado":
                  if (r>50 and r<215) and g<80 and  b>63:
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])
                 
        # PARA EL COLOR AZUL
              if comb_color=="Azul":
                  if r<80 and g<80 and b>70:
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])
                     
        # PARA EL COLOR BLANCO
              if comb_color=="Blanco":
                  if r>225 and g>225 and b>215:
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])
                 
        # PARA EL COLOR AMARILLO
              if comb_color=="Amarillo":
                  if r>155 and (g>140 and g<250) and b<125:
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])
                 
        # PARA EL COLOR ROJO
              if comb_color=="Rojo":
                  if r>110 and g<100 and b<90 :
                     pixel=tuple([r,g,b])
                  else:
                     g=(r+g+b)/7
                     gris=int(g)
                     pixel=tuple([gris,gris,gris])

                 
              img2.putpixel((i,j),pixel)
              j+=1
          i+=1
      #img2.show()
      img2.save("img_division_color/img_divi.jpg")
      url="img_division_color/img_divi.jpg"
      foto=QPixmap(url).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      self.lblimgen.setPixmap(foto)

 def Abrir_formu_analisis(self): 
    self.regis_divi_anali_color_termo=Registro_divi_anali_color_termo()
    self.regis_divi_anali_color_termo.exec_()

class Registro_divi_anali_color_termo(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("resitro_analisis_divi_color_termo.ui", self)
  self.setWindowTitle("Registro De Analisis Termografia")
  
  self.registrar.clicked.connect(self.Guardar_regis_anali_color_termo_divi)
  self.cancelar.clicked.connect(self.cancelar_cerrar)
  
 def cancelar_cerrar(self):
  self.close()
  
 def Guardar_regis_anali_color_termo_divi(self):   
  id_img=id_imgT1
  titulo=self.titulo.text()
  descrip=self.descrip.toPlainText()
  fecha= time.strftime("%Y-%m-%d")
  print("captura de datos exitosa..")
  if titulo!="" and descrip!="" :
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    sql1 = "SELECT fecha FROM termografia_divi_color where id_captura_imagen='"+str(id_img)+"' "
    print("sdnasjns 125615")
    compro=cursor.execute(sql1)
    if compro==False:
      sql2 = "INSERT INTO termografia_divi_color(fecha,titulo,descripcion,id_captura_imagen) VALUES('"+str(fecha)+"','"+str(titulo)+"','"+str(descrip)+"','"+str(id_img)+"')"
      dat=cursor.execute(sql2)
      conn.commit()
      QMessageBox.question(self, 'INFORMACION', "Registro GUARDADO correctamente", QMessageBox.Yes)
    else:
      QMessageBox.question(self, 'INFORMACION', "Este Registro ya fue GUARDADO", QMessageBox.Yes)
  else:
      QMessageBox.question(self, 'INFORMACION', "Llene todos los campos y vuelva a intentarlo", QMessageBox.Yes)

   








class Reducir_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("reducir_imagenes.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))   
   fecha = QTableWidgetItem(str(row1[8]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,latitu)
   self.table.setItem(i,3,longitu)
   self.table.setItem(i,4,hecta)
   self.table.setItem(i,5,parce)  
   i=i+1

  self.buscar.clicked.connect(self.buacar) 
  self.mostrar_imagen.clicked.connect(self.muestra_img)
  self.reducir.clicked.connect(self.reducir_img) 
  self.guarda_corte.clicked.connect(self.guardar_img_cortada)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(6)
   self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%' or latitud like '%"+dato+"%' or fecha like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))
    fecha = QTableWidgetItem(str(row1[8]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
   
    self.table.setItem(i,0,codigo)
    self.table.setItem(i,1,fecha)
    self.table.setItem(i,2,latitu)
    self.table.setItem(i,3,longitu)
    self.table.setItem(i,4,hecta)
    self.table.setItem(i,5,parce)  
    i=i+1

 def muestra_img(self):
  global nombre_imag
  global nombre_de_la_imagen
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  if self.table.selectionModel().selectedRows() :
    rows=self.table.selectionModel().selectedRows()
    index=[]
    for i in rows:
      index.append(i.row())
    index.sort(reverse=True)
    for i in index:
      idI=self.table.item(i,0).text()
      print("id-cedula="+idI)
   
    sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
    cursor.execute(sql2)
    row2 = cursor.fetchone()
    img1=str(row2[0])
    img2=str(row2[1])
    if self.img_normal.isChecked():
      foto=QPixmap(img1).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img1)
      self.lblimgen.setPixmap(foto)
      nombre_imag=Image.open(img1)    
      self.img_x.setText(""+str(nombre_imag.size))
        
    if self.img_termica.isChecked():
      foto=QPixmap(img2).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img2)
      self.lblimgen.setPixmap(foto)
      nombre_imag=Image.open(img2)    
      self.img_x.setText(""+str(nombre_imag.size)) 
  else :
    print("seleccione una imagen")
    QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

 def reducir_img(self):
    print("12345")
    global nombre_imag
    global region
    derecha=self.dere.value()
    abajo=self.aba.value()
    
    cadena=str(nombre_imag.size)
    mostrar=cadena.split(",")
    # tamaño de imagen para validar
    der=mostrar[0][1:8]
    aba=mostrar[1][0:-1]
    derecha=int(der)+int(derecha)
    abajo=int(aba)+int(abajo)

    caja = (derecha, abajo)
    # Obtener de la imagen original la región de la caja
    region = nombre_imag.resize((caja))
    #region.show()  # Mostrar imagen de la region
    region.save("cortes/corte.jpg")
    url="cortes/corte.jpg"
    pixmapImg = QPixmap(url).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    self.lblimgen.setPixmap(pixmapImg)

 def guardar_img_cortada(self):
    global region
    global nombre_de_la_imagen
    buttonReply = QMessageBox.question(self, 'Guardar', "Desea guardar la imagen?", QMessageBox.Yes | QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        buttonReply = QMessageBox.question(self, 'ADVERTENCIA', "Los cambios serán IRREVERSIBLES, Realmente desea guardar?", QMessageBox.Yes | QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            guardar=region
            guardar.save("img_campo/"+nombre_de_la_imagen)
        else:
            print('No clicked.')
        
    else:
        print('No clicked.')
    








class Cortar_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("cortar_imagenes.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   fecha = QTableWidgetItem(str(row1[8]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,fecha)
   self.table.setItem(i,2,latitu)
   self.table.setItem(i,3,longitu)
   self.table.setItem(i,4,hecta)
   self.table.setItem(i,5,parce)  
   i=i+1
  self.buscar.clicked.connect(self.buacar) 
  self.mostrar_imagen.clicked.connect(self.muestra_img)
  self.corte.clicked.connect(self.corte_img) 
  self.guarda_corte.clicked.connect(self.guardar_img_cortada)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(6)
   self.table.setHorizontalHeaderLabels(['Cod','Fecha','Latitud','Longitud','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%' or latitud like '%"+dato+"%' or fecha like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))
    fecha = QTableWidgetItem(str(row1[8]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
   
    self.table.setItem(i,0,codigo)
    self.table.setItem(i,1,fecha)
    self.table.setItem(i,2,latitu)
    self.table.setItem(i,3,longitu)
    self.table.setItem(i,4,hecta)
    self.table.setItem(i,5,parce)  
    i=i+1


 def muestra_img(self):
  global nombre_imag
  global nombre_de_la_imagen
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  if self.table.selectionModel().selectedRows() :
    rows=self.table.selectionModel().selectedRows()
    index=[]
    for i in rows:
      index.append(i.row())
    index.sort(reverse=True)
    for i in index:
      idI=self.table.item(i,0).text()
      print("id-cedula="+idI)
   
    sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
    cursor.execute(sql2)
    row2 = cursor.fetchone()
    img1=str(row2[0])
    img2=str(row2[1])
    if self.img_normal.isChecked():
      foto=QPixmap(img1).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img1)
      self.lblimgen.setPixmap(foto)
      nombre_imag=Image.open(img1)    
      self.img_x.setText("(0 , 0)"+str(nombre_imag.size))
        
    if self.img_termica.isChecked():
      foto=QPixmap(img2).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      nombre_de_la_imagen=os.path.basename(img2)
      self.lblimgen.setPixmap(foto)
      nombre_imag=Image.open(img2)    
      self.img_x.setText("(0 , 0)"+str(nombre_imag.size)) 
  else :
    print("seleccione una imagen")
    QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)
 
 def corte_img(self):
    print("12345")
    global nombre_imag
    global region
    izquierda=self.izq.value()
    arriba=self.arri.value()
    derecha=self.dere.value()
    abajo=self.aba.value()
    
    cadena=str(nombre_imag.size)
    mostrar=cadena.split(",")
    der=mostrar[0][1:8]
    aba=mostrar[1][0:-1]
    derecha=int(der)-int(derecha)
    abajo=int(aba)-int(abajo)

    caja = (izquierda, arriba, derecha, abajo)
    # Obtener de la imagen original la región de la caja
    region = nombre_imag.crop(caja)
    #region.show()  # Mostrar imagen de la region
    region.save("cortes/corte.jpg")
    url="cortes/corte.jpg"
    pixmapImg = QPixmap(url).scaled(400, 350, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    self.lblimgen.setPixmap(pixmapImg)

 def guardar_img_cortada(self):
    global region
    global nombre_de_la_imagen
    buttonReply = QMessageBox.question(self, 'Guardar', "Desea guardar la imagen?", QMessageBox.Yes | QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        buttonReply = QMessageBox.question(self, 'ADVERTENCIA', "Los cambios serán IRREVERSIBLES, Realmente desea guardar?", QMessageBox.Yes | QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            guardar=region
            guardar.save("img_campo/"+nombre_de_la_imagen)
        else:
            print('No clicked.')
        
    else:
        print('No clicked.')
    










class Lista_privilegios(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_privilegios.ui", self)
  self.setWindowTitle("Lista De Privilegios")

  self.table.setColumnCount(2)
  self.table.setHorizontalHeaderLabels(['Cod','Privilegio'])

  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT id_privilegio,privilegio FROM privilegio Order by id_privilegio ASC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   privi = QTableWidgetItem(str(row1[1]))

   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,privi)
   i=i+1
  conn.close()
  self.buscar.clicked.connect(self.buacar)
  self.actualiza.clicked.connect(self.Actualizar)      
  #self.table.itemChanged.connect(self.Actualizar)
  self.cerrar.clicked.connect(self.cancelar_cerrar)
  
 def buacar(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(2)
   self.table.setHorizontalHeaderLabels(['Cod','Privilegio'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   dato=self.txt_buscar.text()
   sql = "SELECT id_privilegio,privilegio FROM privilegio where privilegio like '%"+dato+"%' Order by id_privilegio ASC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))
    privi = QTableWidgetItem(str(row1[1]))

    self.table.setItem(i,0,codigo)
    self.table.setItem(i,1,privi) 
    i=i+1
 
  
 def cancelar_cerrar(self):
  self.close()
  
 def Actualizar(self):
  if self.table.selectedItems():
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      columna=self.table.currentColumn()
      row=self.table.currentRow()
      idP=self.table.item(row,0).text()
      value=self.table.currentItem().text()
      columnas=['id_pricilegio','privilegio']
      colu=columnas[columna]
      print(colu+" = "+value+" id:"+idP)
      sql = "UPDATE privilegio SET "+columnas[columna]+"='"+str(value)+"' WHERE id_privilegio='"+str(idP)+"'"
      dat=cursor.execute(sql)
      conn.commit()
      if dat==False:
       print("modificaion fallida..")
      else:
       print("modificaion exitosa..")
       QMessageBox.information(self, "Tabla Modificada", "Modificación Exitosa", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero Edite un Registro", QMessageBox.Yes)
    





class Lista_usuarios(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_usuarios.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
##  self.layout=QGridLayout()
##  self.setLayout(self.layout)
##  self.table=QTableWidget()
##  self.eliminar=QPushButton("ELIMINAR")
##  self.layout.addWidget(self.eliminar)
##  self.layout.addWidget(self.table)
  
  self.table.setColumnCount(5)
  self.table.setHorizontalHeaderLabels(['Cod','Nombres','Privilegio','Usuario','Contraseña'])

  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT U.id_usuario,P.privilegio,U.usuario,U.clave,E.nombres,E.apellidos FROM empleados E inner join usuarios U on U.id_empleado=E.id_empleado inner join privilegio P on P.id_privilegio=U.id_privilegio Order by U.id_usuario DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   privi = QTableWidgetItem(str(row1[1]))
   usua = QTableWidgetItem(str(row1[2]))
   clave = QTableWidgetItem(str(row1[3]))
   nombre_completo = QTableWidgetItem(str(row1[4])+" "+str(row1[5]))

   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,nombre_completo)
   self.table.setItem(i,2,privi)
   self.table.setItem(i,3,usua)
   self.table.setItem(i,4,clave)
   i=i+1
  conn.close()
  self.editar.clicked.connect(self.Actualizar)
  self.buscar.clicked.connect(self.Buscar)
  self.cerrar.clicked.connect(self.cancelar_cerrar)
  
  
 def cancelar_cerrar(self):
  self.close()
  
 def Actualizar(self):
  if self.table.selectedItems():
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      columna=self.table.currentColumn()
      row=self.table.currentRow()
      idU=self.table.item(row,0).text()
      value=self.table.currentItem().text()
      columnas=['id_usuario','nombres','privilegio','usuario','calve']
      colu=columnas[columna]
      print(colu+" = "+value+" id:"+idU)
      sql = "UPDATE usuarios SET "+columnas[columna]+"='"+str(value)+"' WHERE id_usuario='"+str(idU)+"'"
      dat=cursor.execute(sql)
      conn.commit()
      if dat==False:
       print("modificaion fallida..")
      else:
       print("modificaion exitosa..")
       QMessageBox.information(self, "Tabla Modificada", "Modificación Exitosa", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero Edite un Registro", QMessageBox.Yes)

 def Buscar(self):
  self.table.clear()
  #self.table.removeRow()
  self.table.setRowCount(0)  
  self.table.setColumnCount(5)
  self.table.setHorizontalHeaderLabels(['Cod','Nombres','Privilegio','Usuario','Contraseña'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito123..")
  dato=self.txt_buscar.text()
  sql = "SELECT U.id_usuario,P.privilegio,U.usuario,U.clave,E.nombres,E.apellidos FROM empleados E inner join usuarios U on U.id_empleado=E.id_empleado inner join privilegio P on P.id_privilegio=U.id_privilegio where E.nombres like '%"+dato+"%' or E.apellidos like '%"+dato+"%' or P.privilegio like '%"+dato+"%' Order by U.id_usuario DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   privi = QTableWidgetItem(str(row1[1]))
   usua = QTableWidgetItem(str(row1[2]))
   clave = QTableWidgetItem(str(row1[3]))
   nombre_completo = QTableWidgetItem(str(row1[4])+" "+str(row1[5]))

   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,nombre_completo)
   self.table.setItem(i,2,privi)
   self.table.setItem(i,3,usua)
   self.table.setItem(i,4,clave)
   i=i+1








class Lista_imagenes(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("lista_imagenes.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
##  self.layout=QGridLayout()
##  self.setLayout(self.layout)
##  self.table=QTableWidget()
##  self.eliminar=QPushButton("ELIMINAR")
##  self.layout.addWidget(self.eliminar)
##  self.layout.addWidget(self.table)
##  self.lblimg=QLabel("holamundo")
  #self.layout.addWidget(self.lblimg)
 
  
  self.table.setColumnCount(9)
  self.table.setHorizontalHeaderLabels(['Cod','Imagen','Imagen Termica', 'Fecha','Latitud','Longitud','Temperatura','Hectarea','Parcela'])

  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT * FROM captura_imagen Order by id_captura_imagen DESC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   codigo = QTableWidgetItem(str(row1[0]))
   image1 = QTableWidgetItem(str(row1[1]))
   image2 = QTableWidgetItem(str(row1[2]))
   latitu = QTableWidgetItem(str(row1[3]))
   longitu = QTableWidgetItem(str(row1[4]))
   tempera = QTableWidgetItem(str(row1[5]))
   hecta = QTableWidgetItem(str(row1[6]))
   parce = QTableWidgetItem(str(row1[7]))
   fecha = QTableWidgetItem(str(row1[8]))
   
   self.table.setItem(i,0,codigo)
   self.table.setItem(i,1,image1)
   self.table.setItem(i,2,image2)
   self.table.setItem(i,3,fecha)
   self.table.setItem(i,4,latitu)
   self.table.setItem(i,5,longitu)
   self.table.setItem(i,6,tempera)
   self.table.setItem(i,7,hecta)
   self.table.setItem(i,8,parce)  
   i=i+1
  conn.close()
  
  self.editar.clicked.connect(self.Actualizar)
  self.buscar.clicked.connect(self.buscarI)
  self.eliminar.clicked.connect(self.Elimi)
  self.verimg.clicked.connect(self.verImg)
  self.cerrar.clicked.connect(self.cancelar_cerrar)
  
  
  
 def cancelar_cerrar(self):
  self.close()
  
 def verImg(self):
  if self.table.selectionModel().selectedRows() :
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        idI=self.table.item(i,0).text()
        print("id-cedula="+idI)
      
      sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
      cursor.execute(sql2)
      row2 = cursor.fetchone()
      img1=str(row2[0])
      img2=str(row2[1])

      foto=QPixmap(img1).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      self.lblimgen1.setPixmap(foto)
      foto2=QPixmap(img2).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
      self.lblimgen2.setPixmap(foto2)
  else :
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)
  
 def Actualizar(self):
  if self.table.selectedItems():
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      columna=self.table.currentColumn()
      row=self.table.currentRow()
      idI=self.table.item(row,0).text()
      value=self.table.currentItem().text()
      columnas=['id_captura_imagen','imagen1','imagen2','fecha','latitud', 'longitud','temperatura', 'hectarea','parcela']
      colu=columnas[columna]
      print(colu+" = "+value+" id:"+idI)
    ##  
    ##  sql2 = "SELECT imagen1, imagen2 FROM captura_imagen where id_captura_imagen='"+str(idI)+"' "
    ##  cursor.execute(sql2)
    ##  row2 = cursor.fetchone()
    ##  img1=str(row2[0])
    ##  img2=str(row2[1])
    ##
    ##  foto=QPixmap(img1).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    ##  self.lblimgen1.setPixmap(foto)
    ##  foto2=QPixmap(img2).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
    ##  self.lblimgen2.setPixmap(foto2)


      
    ##  sql2 = "SELECT nombres,apellidos,cedula,direccion,telefono FROM empleados WHERE cedula='"+ide+"'"
    ##  cursor.execute(sql2)
    ##  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
    ##  row2 = cursor.fetchone()
    ##  print("consulta exitosa..")
    ##  nombre2 = str(row2[0])
    ##  apellido2 = str(row2[1])
    ##  cedula2 = str(row2[2])
    ##  direccion2 = str(row2[3])
    ##  telefono2 = str(row2[4])
    ##  
    ##  if columnas[columna]=="cedula":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',"+columnas[columna]+"='"+str(value)+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="nombre":
    ##    sql = "UPDATE empleados SET "+columnas[columna]+"='"+str(value)+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="apellido":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',"+columnas[columna]+"='"+str(value)+"',cedula='"+cedula2+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="direccion":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',"+columnas[columna]+"='"+str(value)+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="telefono":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',direccion='"+direccion2+"',"+columnas[columna]+"='"+str(value)+"' WHERE cedula='"+str(ide)+"'"
    ##  else:
    ##    print("no entro a ningun if : "+columnas[columna]+"='"+str(value))
      sql = "UPDATE captura_imagen SET "+columnas[columna]+"='"+str(value)+"' WHERE id_captura_imagen='"+str(idI)+"'"
      dat=cursor.execute(sql)
      conn.commit()
      if dat==False:
       print("modificaion fallida..")
      else:
       print("modificaion exitosa..")
       QMessageBox.information(self, "Tabla Modificada", "Modificación Exitosa", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero Edite un Registro", QMessageBox.Yes)
    
       
 def Elimi(self):
  if self.table.selectionModel().selectedRows() :
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        idI=self.table.item(i,0).text()
        self.table.removeRow(i)
        print("id-cedula="+idI)
        sql = "DELETE FROM captura_imagen WHERE id_captura_imagen='"+str(idI)+"'"
        dat=cursor.execute(sql)
        conn.commit()
        if dat==False:
          print("eliminacion lofica fallida..")
        else:
          print("eliminacion lofica exitosa..")
          QMessageBox.information(self, "Tabla Modificada", "Imagen Eliminada", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)
   
 def buscarI(self):
   self.table.clear()
   #self.table.removeRow()
   self.table.setRowCount(0)
   self.table.setColumnCount(9)
   self.table.setHorizontalHeaderLabels(['Cod','Imagen','Imagen Termica', 'Fecha','Latitud','Longitud','Temperatura','Hectarea','Parcela'])
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito123..")
   dato=self.txt_buscar.text()
   sql = "SELECT * FROM captura_imagen where id_captura_imagen like '%"+dato+"%' or latitud like '%"+dato+"%' or fecha like '%"+dato+"%' or longitud like '%"+dato+"%' or hectarea like '%"+dato+"%' or parcela like '%"+dato+"%' Order by id_captura_imagen DESC "
   cursor.execute(sql)
   #resul = cursor.fetchone()   o   resul = cursor.fetchall()
   rows1 = cursor.fetchall()
   i=0
   for row1 in rows1:
    print("consulta exitosa1234..")
    self.table.insertRow(i)
    codigo = QTableWidgetItem(str(row1[0]))
    image1 = QTableWidgetItem(str(row1[1]))
    image2 = QTableWidgetItem(str(row1[2]))
    latitu = QTableWidgetItem(str(row1[3]))
    longitu = QTableWidgetItem(str(row1[4]))
    tempera = QTableWidgetItem(str(row1[5]))
    hecta = QTableWidgetItem(str(row1[6]))
    parce = QTableWidgetItem(str(row1[7]))
    fecha = QTableWidgetItem(str(row1[8]))
   
    self.table.setItem(i,0,codigo)
    self.table.setItem(i,1,image1)
    self.table.setItem(i,2,image2)
    self.table.setItem(i,3,fecha)
    self.table.setItem(i,4,latitu)
    self.table.setItem(i,5,longitu)
    self.table.setItem(i,6,tempera)
    self.table.setItem(i,7,hecta)
    self.table.setItem(i,8,parce)
    i=i+1
   print("123")










class Ingreso_imagen(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("ingreso_imagenes.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  
  #Señal para abrir el cuadro de diálogo de selección de archivos
  self.temperatura.setValue(30)
  self.btn_imagen.clicked.connect(self.openDialog)
  self.btn_imagen_2.clicked.connect(self.openDialog2)
  self.registrar.clicked.connect(self.validar_formulario)
  self.cancelar.clicked.connect(self.cancelar_cerrar)
  
 #Método encargado de abrir el cuadro de diálogo de selección de archivos
 def openDialog(self):
   imagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),"Archivos de imagen (*.png *.jpg *.jpeg)",options=QFileDialog.Options())
   nombre_imag=os.path.basename(imagen)
   if imagen:
       # Adaptar imagen
       pixmapImagen = QPixmap(imagen).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
       # Mostrar imagen
       self.labelImagen.setPixmap(pixmapImagen)
       self.btn_imagen.setText(nombre_imag)

 def openDialog2(self):
   imagen, extension = QFileDialog.getOpenFileName(self, "Seleccionar imagen", getcwd(),"Archivos de imagen (*.png *.jpg *.jpeg)",options=QFileDialog.Options())
   #guardar_acrvhivo_en_algun_ligar = QFileDialog.getSaveFileName(self, "Guardar fichero", imagen)
   nombre_imag=os.path.basename(imagen)
   if imagen:
       # Adaptar imagen
       pixmapImagen = QPixmap(imagen).scaled(200, 120, Qt.KeepAspectRatio,Qt.SmoothTransformation)
       # Mostrar imagen
       self.labelImagen_2.setPixmap(pixmapImagen)
       self.btn_imagen_2.setText(nombre_imag)
       
       
 def cancelar_cerrar(self):
  self.close()
 
 def validar_formulario(self):
   QMessageBox.information(self, "Formulario correcto", "Validación correcta", QMessageBox.Discard)
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   if cursor == False:
       print("no open conexion..")
   else:
       print("open conexion..")    
   img2=self.btn_imagen.text()
   img1=self.btn_imagen_2.text()
   
   ruta_img1="img_campo/"+img1
   ruta_img2="img_campo/"+img2
   longi=self.longitud.text()
   lati=self.latitud.text()
   tempera=self.temperatura.value()
   hecta=self.hectarea.value()
   parce=self.parcela.value()
   fecha= time.strftime("%Y-%m-%d")
   print("captura de datos exitosa..")
   if ruta_img1!="" and ruta_img2!="" and longi!="" and lati!="" and tempera!=0 or tempera!="" and hecta!=0 or hecta!="" and parce!=0 or parce!="" :
       sql2 = "INSERT INTO captura_imagen(imagen1,imagen2,latitud,longitud,temperatura,hectarea,parcela,fecha) VALUES('"+ruta_img1+"','"+ruta_img2+"','"+longi+"','"+lati+"','"+str(tempera)+"','"+str(hecta)+"','"+str(parce)+"','"+str(fecha)+"')"
       dat=cursor.execute(sql2)
       conn.commit()
       self.latitud.setText("")
       self.longitud.setText("")
       self.temperatura.setValue(0)
       self.hectarea.setValue(0)
       self.parcela.setValue(0)
       ruta_img1=""
       ruta_img2=""
   else:
       print("llene todos los campos")
       QMessageBox.question(self, 'INFORMACION', "Llene todos los campos y vuelva a intentarlo", QMessageBox.Yes)
   if dat==False:
    print("registro fallido..")
   else:
    print("registro exitoso..")
   





class Ingreso_privilegio(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("ingreso_privilegios.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.privilegio.textChanged.connect(self.validar_nombre)  
  self.registrar.clicked.connect(self.validar_formulario)
  self.cancelar.clicked.connect(self.cancelar_cerrar)

 def cancelar_cerrar(self):
  self.close()
     
 def validar_nombre(self):
  nombre = self.privilegio.text()
  validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
  if nombre == "":
   self.privilegio.setStyleSheet("border: 1px solid yellow;")
   return False
  elif not validar:
   self.privilegio.setStyleSheet("border: 1px solid red;")
   return False
  else:
   self.privilegio.setStyleSheet("border: 1px solid green;")
   return True


 def validar_formulario(self):
  if self.validar_nombre():
   QMessageBox.information(self, "Formulario correcto", "Validación correcta", QMessageBox.Discard)
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   if cursor == False:
       print("no open conexion..")
   else:
       print("open conexion..")    
   privilegio=self.privilegio.text()      
   print("captura de datos exitosa..")
   
   sql2 = "INSERT INTO privilegio(privilegio) VALUES('"+privilegio+"')"
   dat=cursor.execute(sql2)
   conn.commit()
   if dat==False:
    print("registro fallido..")
   else:
    print("registro exitoso..")
   
  else:
   QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Discard)






class Ingreso_empleado(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("ingreso_empleados.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.nombres.textChanged.connect(self.validar_nombre)
  self.apellidos.textChanged.connect(self.validar_apellido)
  
  self.registrar.clicked.connect(self.validar_formulario)
  self.cancelar.clicked.connect(self.cancelar_cerrar)

 def cancelar_cerrar(self):
  self.close()
     
 def validar_nombre(self):
  nombre = self.nombres.text()
  validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
  if nombre == "":
   self.nombres.setStyleSheet("border: 1px solid yellow;")
   return False
  elif not validar:
   self.nombres.setStyleSheet("border: 1px solid red;")
   return False
  else:
   self.nombres.setStyleSheet("border: 1px solid green;")
   return True

 def validar_apellido(self):
  apellido = self.apellidos.text()
  validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', apellido, re.I)
  if apellido == "":
   self.apellidos.setStyleSheet("border: 1px solid yellow;")
   return False
  elif not validar:
   self.apellidos.setStyleSheet("border: 1px solid red;")
   return False
  else:
   self.apellidos.setStyleSheet("border: 1px solid green;")
   return True


 def validar_formulario(self):
  if self.validar_nombre() and self.validar_apellido():
   QMessageBox.information(self, "Formulario correcto", "Registro Exitoso", QMessageBox.Discard)
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   if cursor == False:
       print("no open conexion..")
   else:
       print("open conexion..")    
   id_estado="1"
   cedula3=self.cedula.text()
   nombre3=self.nombres.text()
   apellido3=self.apellidos.text()
   direccion3=self.direccion.text()
   telefono3=self.telefono.value()      
   print("captura de datos exitosa..")
   
   if cedula3!="" and nombre3!="" and apellido3!="" and direccion3!="" and telefono3!=0 or telefono3!="" :
       sql2 = "INSERT INTO empleados(nombres,apellidos,cedula,direccion,telefono,id_estado) VALUES('"+nombre3+"','"+apellido3+"','"+cedula3+"','"+direccion3+"','"+str(telefono3)+"','"+id_estado+"')"
       dat=cursor.execute(sql2)
       conn.commit()
       id_estado="1"
       self.cedula.text("")
       self.nombres.text("")
       self.apellidos.text("")
       self.direccion.text("")
       self.telefono.value("")
   else:
       print("llene todos los campos")
       QMessageBox.question(self, 'INFORMACION', "Llene todos los campos y vuelva a intentarlo", QMessageBox.Yes)
       
   if dat==False:
    print("registro fallido..")
   else:
    print("registro exitoso..")
   
  else:
   QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Discard)









class Lista_empleados(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("ven_list_empleados.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
##  self.layout=QGridLayout()
##  self.setLayout(self.layout)
##  self.table=QTableWidget()
##  self.eliminar=QPushButton("ELIMINAR")
##  self.layout.addWidget(self.eliminar)
##  self.layout.addWidget(self.table)
  
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cedula','Nombres','Apellidos','Dirección','Telefono','Estado'])

  ##  self.n_propietario.textChanged.connect(self.validar_nombre)
##  self.registrar.clicked.connect(self.validar_formulario)
##  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT nombres,apellidos,cedula,direccion,telefono,id_estado FROM empleados Order by id_estado ASC "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows1 = cursor.fetchall()
  i=0
  for row1 in rows1:
   print("consulta exitosa..")
   self.table.insertRow(i)
   nombre = QTableWidgetItem(str(row1[0]))
   apellido = QTableWidgetItem(str(row1[1]))
   cedula = QTableWidgetItem(str(row1[2]))
   direccion = QTableWidgetItem(str(row1[3]))
   telefono = QTableWidgetItem(str(row1[4]))
   if str(row1[5])=="1":
       estado ="Activo"
   else:
       estado ="Inactivo"
   estado = QTableWidgetItem(str(estado))
   self.table.setItem(i,0,cedula)
   self.table.setItem(i,1,nombre)
   self.table.setItem(i,2,apellido)
   self.table.setItem(i,3,direccion)
   self.table.setItem(i,4,telefono)
   self.table.setItem(i,5,estado) 
   i=i+1
  conn.close()
  self.recargar.clicked.connect(self.recargar_list)
  self.buscar.clicked.connect(self.buscar_list)
  self.editar.clicked.connect(self.Actualizar)

  self.restablecer.clicked.connect(self.Agreg_logico)
  self.eliminar.clicked.connect(self.Elimi_logico)
 
  self.asi_usu=Asig_usuario()
  self.aisg_usuario.clicked.connect(self.asignar_usuario_emple)
  self.cerrar.clicked.connect(self.cancelar_cerrar)


 def recargar_list(self):
  self.table.clear()
  #self.table.removeRow()
  self.table.setRowCount(0)  
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cedula','Nombres','Apellidos','Dirección','Telefono','estado'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito123..")
  sql2 = "SELECT nombres,apellidos,cedula,direccion,telefono,id_estado FROM empleados order by id_estado ASC "
  cursor.execute(sql2)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows2 = cursor.fetchall()
  i=0
  for row2 in rows2:
   print("consulta exitosa123..")
   nombre2 = QTableWidgetItem(str(row2[0]))
   apellido2 = QTableWidgetItem(str(row2[1]))
   cedula2 = QTableWidgetItem(str(row2[2]))
   direccion2 = QTableWidgetItem(str(row2[3]))
   telefono2 = QTableWidgetItem(str(row2[4]))
   if str(row2[5])=="1":
       estado ="Activo"
   else:
       estado ="Inactivo"
   estado = QTableWidgetItem(str(estado))

   self.table.insertRow(i)
   self.table.setItem(i,0,cedula2)
   self.table.setItem(i,1,nombre2)
   self.table.setItem(i,2,apellido2)
   self.table.setItem(i,3,direccion2)
   self.table.setItem(i,4,telefono2)
   self.table.setItem(i,5,estado)
   i=i+1


 def buscar_list(self):
  self.table.clear()
  #self.table.removeRow()
  self.table.setRowCount(0)  
  self.table.setColumnCount(6)
  self.table.setHorizontalHeaderLabels(['Cedula','Nombres','Apellidos','Dirección','Telefono','estado'])
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito123..")

  dato=self.txt_buscar.text()
  sql2 = "SELECT nombres,apellidos,cedula,direccion,telefono,id_estado FROM empleados where nombres like '%"+dato+"%' or apellidos like '%"+dato+"%' or cedula like '%"+dato+"%' order by id_estado ASC "
  cursor.execute(sql2)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  rows2 = cursor.fetchall()
  i=0
  for row2 in rows2:
   print("consulta exitosa123..")
   nombre2 = QTableWidgetItem(str(row2[0]))
   apellido2 = QTableWidgetItem(str(row2[1]))
   cedula2 = QTableWidgetItem(str(row2[2]))
   direccion2 = QTableWidgetItem(str(row2[3]))
   telefono2 = QTableWidgetItem(str(row2[4]))
   if str(row2[5])=="1":
       estado ="Activo"
   else:
       estado ="Inactivo"
   estado = QTableWidgetItem(str(estado))

   self.table.insertRow(i)
   self.table.setItem(i,0,cedula2)
   self.table.setItem(i,1,nombre2)
   self.table.setItem(i,2,apellido2)
   self.table.setItem(i,3,direccion2)
   self.table.setItem(i,4,telefono2)
   self.table.setItem(i,5,estado)
   i=i+1


 def cancelar_cerrar(self):
  self.close()
     
 def Actualizar(self):
  if self.table.selectedItems():
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      columna=self.table.currentColumn()
      row=self.table.currentRow()
      ide=self.table.item(row,0).text()
      value=self.table.currentItem().text()
      columnas=['cedula','nombres','apellidos', 'direccion','telefono']
      colu=columnas[columna]
      print(colu+" = "+value+" id:"+ide)
    ##  sql2 = "SELECT nombres,apellidos,cedula,direccion,telefono FROM empleados WHERE cedula='"+ide+"'"
    ##  cursor.execute(sql2)
    ##  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
    ##  row2 = cursor.fetchone()
    ##  print("consulta exitosa..")
    ##  nombre2 = str(row2[0])
    ##  apellido2 = str(row2[1])
    ##  cedula2 = str(row2[2])
    ##  direccion2 = str(row2[3])
    ##  telefono2 = str(row2[4])
    ##  
    ##  if columnas[columna]=="cedula":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',"+columnas[columna]+"='"+str(value)+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="nombre":
    ##    sql = "UPDATE empleados SET "+columnas[columna]+"='"+str(value)+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="apellido":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',"+columnas[columna]+"='"+str(value)+"',cedula='"+cedula2+"',direccion='"+direccion2+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="direccion":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',"+columnas[columna]+"='"+str(value)+"',telefono='"+telefono2+"' WHERE cedula='"+str(ide)+"'"
    ##  elif columnas[columna]=="telefono":
    ##    sql = "UPDATE empleados SET nombres='"+nombre2+"',apellidos='"+apellido2+"',cedula='"+cedula2+"',direccion='"+direccion2+"',"+columnas[columna]+"='"+str(value)+"' WHERE cedula='"+str(ide)+"'"
    ##  else:
    ##    print("no entro a ningun if : "+columnas[columna]+"='"+str(value))
      sql = "UPDATE empleados SET "+columnas[columna]+"='"+str(value)+"' WHERE cedula='"+str(ide)+"'"
      dat=cursor.execute(sql)
      conn.commit()
      if dat==False:
       print("modificaion fallida..")
      else:
       print("modificaion exitosa..")
       QMessageBox.information(self, "Tabla Modificada", "Modificación Exitosa", QMessageBox.Discard)
       
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero Edite un Registro", QMessageBox.Yes)
      
 def Elimi_logico(self):
  if self.table.selectionModel().selectedRows() :
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        ide=self.table.item(i,0).text()
        self.table.removeRow(i)
        print("id-cedula="+ide)
        sql = "UPDATE empleados SET id_estado='2' WHERE cedula='"+str(ide)+"'"
        dat=cursor.execute(sql)
        conn.commit()
        if dat==False:
          print("eliminacion lofica fallida..")
        else:
          print("eliminacion lofica exitosa..")
          QMessageBox.information(self, "Tabla Modificada", "Empleado Eliminado", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)  

 def Agreg_logico(self):
  if self.table.selectionModel().selectedRows() :
      conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
      cursor = conn.cursor()
      print("conect_exito..")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        ide=self.table.item(i,0).text()
        print("id-cedula="+ide)
        sql = "UPDATE empleados SET id_estado='1' WHERE cedula='"+str(ide)+"'"
        dat=cursor.execute(sql)
        conn.commit()
        if dat==False:
          print("eliminacion lofica fallida..")
        else:
          print("eliminacion lofica exitosa..")
          QMessageBox.information(self, "Tabla Modificada", "Empleado Restablecido", QMessageBox.Discard)
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)

      
 def asignar_usuario_emple(self):
  if self.table.selectionModel().selectedRows() :
      global id_emple
      print("entra a capturar dato")
      rows=self.table.selectionModel().selectedRows()
      index=[]
      for i in rows:
        index.append(i.row())
      index.sort(reverse=True)
      for i in index:
        id_emple=self.table.item(i,0).text()
        print("id-cedula="+id_emple)    
      self.asi_usu=Asig_usuario()
      self.asi_usu.exec_()
  else:
      print("seleccione una imagen")
      QMessageBox.question(self, 'INFORMACION', "Primero seleccione un REGISTRO", QMessageBox.Yes)








class Asig_usuario(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("add_usuario.ui", self)
  self.setWindowTitle("Cuadro de dialogo")
  self.usuario.textChanged.connect(self.validar_nombre)
  self.registrar.clicked.connect(self.validar_formulario)
  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
 
      
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  ide="0950048892"
  if str(id_emple)!="":
      ide=str(id_emple)
      sql = "SELECT nombres,apellidos,cedula FROM empleados WHERE cedula='"+ide+"' Order by id_estado ASC "
  else:
      sql = "SELECT nombres,apellidos,cedula FROM empleados Order by id_estado ASC "
      
  
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  row1 = cursor.fetchone()
  print("consulta exitosa..")
  nombre = str(row1[0])
  apellido = str(row1[1])
  cedula = str(row1[2])
  self.nombres.setText(nombre+" "+apellido)
  print("asin_usu mostrar datos")
  self.cedula.setText(cedula)

  sql2 = "SELECT privilegio FROM privilegio Order by privilegio ASC "
  cursor.execute(sql2)
  rows1 = cursor.fetchall()
  for row1 in rows1:
   print("consulta exitosa..")
   self.privilegios.addItem(str(row1[0]))
   
  conn.close()
  

 def cancelar_cerrar(self):
  self.close()
     
 def validar_nombre(self):
  nombre = self.usuario.text()
  validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
  if nombre == "":
   self.usuario.setStyleSheet("border: 1px solid yellow;")
   return False
  elif not validar:
   self.usuario.setStyleSheet("border: 1px solid red;")
   return False
  else:
   self.usuario.setStyleSheet("border: 1px solid green;")
   return True

 def validar_formulario(self):
  if self.validar_nombre():
   QMessageBox.information(self, "Formulario correcto", "Validación correcta", QMessageBox.Discard)
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   
   nombres=self.nombres.text()
   cedula=self.cedula.text()
   usua=self.usuario.text()
   clave=self.clave.text()
   privi=self.privilegios.currentText()
   print("datos capturados..")
   if cursor == False:
       print("no open conexion..")
   else:
       print("open conexion..")
            
   print("captura de datos exitosa..")
   sql = "SELECT id_empleado FROM empleados where cedula='"+str(cedula)+"' "
   cursor.execute(sql)
   row1 = cursor.fetchone()
   id_emp=str(row1[0])
   print("consul emple exito.. "+str(id_emp))
   
   sql2 = "SELECT id_privilegio FROM privilegio where privilegio='"+str(privi)+"' "
   cursor.execute(sql2)
   row2 = cursor.fetchone()
   id_privi=str(row2[0])
   print("consul privi exito.. "+str(id_privi))

   
   
   #sql = "UPDATE informacion SET id_informacion='"+str(idi)+"',nombre_hacienda='"+hacienda+"',nombre_propietario='"+propie+"',n_hectareas='"+str(hectareas)+"',n_parcela_hectarea='"+str(parcelas)+"',direccion='"+direccion+"',telefono='"+str(telefono)+"' WHERE id_informacion='"+str(idi)+"'"
   sql3 = "INSERT INTO usuarios (usuario,clave,id_empleado,id_privilegio) VALUES('"+usua+"','"+clave+"','"+str(id_emp)+"','"+str(id_privi)+"')" 
   dat=cursor.execute(sql3)
   conn.commit()
   if dat==False:
    print("modificaion fallida..")
   else:
    print("modificaion exitosa..")
   
  else:
   QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Discard)
		




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class informacion(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("Ven_dialogo.ui", self)
  self.resize(520,500)
  self.setWindowTitle("Cuadro de dialogo")
  self.n_propietario.textChanged.connect(self.validar_nombre)
  self.registrar.clicked.connect(self.validar_formulario)
  self.cancelar.clicked.connect(self.cancelar_cerrar)
  #cargar datos de la base en el formulario
  conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
  cursor = conn.cursor()
  print("conect_exito..")
  sql = "SELECT nombre_hacienda,nombre_propietario,n_hectareas,n_parcela_hectarea,direccion,telefono FROM informacion where id_informacion='1' "
  cursor.execute(sql)
  #resul = cursor.fetchone()   o   resul = cursor.fetchall()
  row1 = cursor.fetchone()
  print("consulta exitosa..")
  nhacienda = str(row1[0])
  npropietario = str(row1[1])
  nhectareas = int(row1[2])
  nparcela_hectarea = int(row1[3])
  direccion = str(row1[4])
  telefono = str(row1[5])
  self.n_hacienda.setText(nhacienda)
  self.n_propietario.setText(npropietario)
  self.hectareas.setValue(nhectareas)
  self.parcelas.setValue(nparcela_hectarea)
  self.direccion.setText(direccion)
  self.telefono.setText(telefono)
  conn.close()

 def cancelar_cerrar(self):
  self.close()
     
 def validar_nombre(self):
  nombre = self.n_propietario.text()
  validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$', nombre, re.I)
  if nombre == "":
   self.n_propietario.setStyleSheet("border: 1px solid yellow;")
   return False
  elif not validar:
   self.n_propietario.setStyleSheet("border: 1px solid red;")
   return False
  else:
   self.n_propietario.setStyleSheet("border: 1px solid green;")
   return True

 def validar_formulario(self):
  if self.validar_nombre():
   QMessageBox.information(self, "Formulario correcto", "Validación correcta", QMessageBox.Discard)
   conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
   cursor = conn.cursor()
   print("conect_exito..")
   idi="1"
   hacienda=self.n_hacienda.text()
   propie=self.n_propietario.text()
   hectareas=self.hectareas.value()
   parcelas=self.parcelas.value()
   direccion=self.direccion.text()
   telefono=self.telefono.text()
   print("datos capturados..")
   if cursor == False:
       print("no open conexion..")
   else:
       print("open conexion..")
            
   print("captura de datos exitosa..")
   sql = "UPDATE informacion SET id_informacion='"+str(idi)+"',nombre_hacienda='"+hacienda+"',nombre_propietario='"+propie+"',n_hectareas='"+str(hectareas)+"',n_parcela_hectarea='"+str(parcelas)+"',direccion='"+direccion+"',telefono='"+str(telefono)+"' WHERE id_informacion='"+str(idi)+"'"
   #sql = "INSERT INTO informacion (nombre_hacienda,nombre_propietario,n_hectareas,n_parcela_hectarea,direccion,telefono) VALUES('"+hacienda+"','"+propie+"','"+str(hectareas)+"','"+str(parcelas)+"','"+direccion+"','"+str(telefono)+"')" 
   dat=cursor.execute(sql)
   conn.commit()
   if dat==False:
    print("modificaion fallida..")
   else:
    print("modificaion exitosa..")
   
  else:
   QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Discard)
		

#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("inicio.ui", self)
  self.setWindowTitle("HACIENDA ROSALIA")
  #maximizar ventana
  self.showMaximized()
  #asignar fuente  
  fuente=QFont("Arial",10,QFont.Bold)
  self.setFont(fuente)
  #asignar funcion de formulario a variable de ejecucion en FUN 
  self.formu_info=informacion()
  self.lista_emple=Lista_empleados()
  self.ingre_emple=Ingreso_empleado()
  self.ingre_privi=Ingreso_privilegio()
  self.ingre_image=Ingreso_imagen()
  self.lista_image=Lista_imagenes()
  self.lista_usuari=Lista_usuarios()
  self.lista_privile=Lista_privilegios()
  self.cortar_image=Cortar_imagenes()
  self.reducir_image=Reducir_imagenes()
  self.termogra_image=Termografia_imagenes()
  self.login_i=Login()
  self.interpo_image=Interpolacion_imagenes() 
  self.lista_gps=Lista_gps() 
  self.lista_termo_procen_color=Lista_termo_procentaje_color() 
  self.lista_termo_divi_color=Lista_termo_division_color()  
  self.union_imagene=Union_imagenes() 

  #ejecutar accion-funcion a opcion de menu
  self.actionInformacion.triggered.connect(self.InformacionH)
  self.actionLista_3.triggered.connect(self.List_emple)
  self.actionNuevo_3.triggered.connect(self.Ingre_emple)
  self.actionNuevo_4.triggered.connect(self.Ingre_privi)
  self.actionCargar_Imagenes.triggered.connect(self.Ingre_image)
  self.actionLista_de_Imagenes.triggered.connect(self.Lista_img)
  self.actionUsuarios.triggered.connect(self.Lista_usu)
  self.actionLista_4.triggered.connect(self.Lista_privi)
  self.actionCortar.triggered.connect(self.Corta_img)
  self.actionTama_os.triggered.connect(self.Reducir_img)
  self.actionMetricas_Termograficas.triggered.connect(self.Termografia_img)
  self.actionInterpolado.triggered.connect(self.Interpola_img) 
  self.actionListado_ubicaciones.triggered.connect(self.listas_gps)
  self.actionLista_Porcentajes_Termografia.triggered.connect(self.Lista_termo_procent_color) 
  self.actionLista_Divisi_n_Termografia.triggered.connect(self.Lista_termo_divis_color)  
  self.actionUnion_de_IMG.triggered.connect(self.Union_imagen)
  self.Login_session()
  
 def closeEvent(self,event):
     resultado=QMessageBox.question(self,"Salir...","¿Seguro que quiere salir del Sistema",QMessageBox.Yes|QMessageBox.No)
     if resultado==QMessageBox.Yes:event.accept()
     else:event.ignore()
     
 def InformacionH(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.formu_info.exec_()
 def List_emple(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.lista_emple.exec_()
 def Ingre_emple(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.ingre_emple.exec_()    
 def Ingre_privi(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.ingre_privi.exec_()
 def Ingre_image(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.ingre_image.exec_()    
 def Lista_img(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.lista_image.exec_()
 def Lista_usu(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.lista_usuari.exec_()    
 def Lista_privi(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.lista_privile.exec_()
 def Corta_img(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.cortar_image.exec_()
 def Reducir_img(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.reducir_image.exec_()
 def Termografia_img(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.termogra_image.exec_()   
 def Login_session(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.login_i.exec_()
 def Interpola_img(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.interpo_image.exec_()
 def listas_gps(self):
     #self.dialogo.etiqueta.setText("nueva ventana") 
     self.lista_gps.exec_()   
 def Lista_termo_procent_color(self):
     #self.dialogo.etiqueta.setText("nueva ventana") 
     self.lista_termo_procen_color.exec_()   
 def Lista_termo_divis_color(self):
     #self.dialogo.etiqueta.setText("nueva ventana")  
     self.lista_termo_divi_color.exec_()   
 def Union_imagen(self):
     #self.dialogo.etiqueta.setText("nueva ventana")  
     self.union_imagene.exec_()

     
  
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()
