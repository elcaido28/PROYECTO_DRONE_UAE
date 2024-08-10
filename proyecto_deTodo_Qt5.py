import sys, re
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QDialog,QPushButton,QLabel
from PyQt5 import uic
from PyQt5.QtGui import QFont #para trabajar con fuentes
from PyQt5.QtCore import Qt #para trabajar con tipos de cursor


import ctypes #para obtener alto y ancho del escritorio



class informacion(QDialog):    
 def __init__(self):
  QDialog.__init__(self)
  uic.loadUi("Ven_dialogo.ui", self)
  self.resize(520,500)
  self.setWindowTitle("Cuadro de dialogo")
  self.n_propietario.textChanged.connect(self.validar_nombre)
  self.registrar.clicked.connect(self.validar_formulario)
  
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
  else:
   QMessageBox.warning(self, "Formulario incorrecto", "Validación incorrecta", QMessageBox.Discard)
		

			
##  def validar_email(self):
##    email = self.email.text()
##    validar = re.match('^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$', email, re.I)
##    if email == "":
##        self.email.setStyleSheet("border: 1px solid yellow;")
##        return False
##    elif not validar:
##        self.email.setStyleSheet("border: 1px solid red;")
##        return False
##    else:
##        self.email.setStyleSheet("border: 1px solid green;")
##        return True
		
  
  

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
  #fijar tamaño minimo de la pantalla
  #self.setMinimumSize(500,500)
  #fijar tamaño maximo
  #self.setMaximumSize(800,600)
  #posisionar interfaz en la pantalla (centrar ventana)
##  resolucion=ctypes.windll.user32
##  resolucion_ancho=resolucion.GetSystemMetrics(0)
##  resolucion_alto=resolucion.GetSystemMetrics(1)
##  left=(resolucion_ancho/2)-(self.frameSize().width()/2)
##  top=(resolucion_alto/2)-(self.frameSize().height()/2)
##  self.move(left,top)
  #seabilitar ventana(bloquear)
  #self.setEnabled(false)
  #asignar fuente  
  fuente=QFont("Arial",10,QFont.Bold)
  self.setFont(fuente)
  #asignar un tipo de cursor
  #self.setCursor(Qt.SizeAllCursor)
  #asignar estilos
  #self.setStyleSheet("background-color: #fff; color: #000")
  #self.boton1.setStyleSheet("background-color: #000; color: #fff")
## def showEvent(self,event):
##     self.bienvenido.setText(" BIENVENIDO..!!!")
##  self.boton=QPushButton(self)
##  self.boton.setText("Abrir nueva ventana")
##  self.boton.resize(200,30)
  
  self.formu_info=informacion()
  self.boton.clicked.connect(self.abrirDialogo)
  
  #self.menubar.actionInformacion.clicked.connect(self.abrirDialogo)
  
 def closeEvent(self,event):
     resultado=QMessageBox.question(self,"Salir...","¿Seguro que quiere salir del Sistema",QMessageBox.Yes|QMessageBox.No)
     if resultado==QMessageBox.Yes:event.accept()
     else:event.ignore()
## def moveEvent(self,event):
##     X=str(event.pos().x())
##     Y=str(event.pos().y())
##     self.posicion.setText("x: "+X+" y: "+Y)
 def abrirDialogo(self):
     #self.dialogo.etiqueta.setText("nueva ventana")
     self.formu_info.exec_()
     
     
     

  
    
  
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()
