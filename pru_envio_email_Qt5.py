#http://jquery-manual.blogspot.com/2015/07/24-python-pyqt-interfaz-grafica-smtp.html
import sys, smtplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QMessageBox, QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QCheckBox


class FileDialog(QFileDialog):
 def __init__(self):
  QFileDialog.__init__(self)
  self.setFileMode(QFileDialog.ExistingFiles) #Selección múltiple
  self.files = [] #Lista que guardará las rutas de los archivos
  self.filesSelected.connect(self.getFiles) #Activar la señal al seleccionar archivos
 def getFiles(self):
  self.files = self.selectedFiles() #Agregar las rutas de archivos a la lista

class Dialogo(QDialog):
 def __init__(self):
  QDialog.__init__(self)
  self.setWindowTitle("Enviar email SMTP")
  self.resize(450, 600)
  #Crear objetos en el cuadro de diálogo
  self.layout = QGridLayout()
  self.setLayout(self.layout)
  self.label_host = QLabel("Host SMTP:")
  self.txt_host = QLineEdit()
  self.chk_tls = QCheckBox("STARTTLS")
  self.chk_tls.setChecked(True)
  self.label_port = QLabel("Puerto:")
  self.txt_port = QLineEdit()
  self.label_user = QLabel("Usuario:")
  self.txt_user = QLineEdit()
  self.label_pass = QLabel("Password:")
  self.txt_pass = QLineEdit()
  self.txt_pass.setEchoMode(QLineEdit.Password)
  self.label_from = QLabel("Remitente:")
  self.txt_from = QLineEdit()
  self.label_to = QLabel("Destinatario/s:")
  self.txt_to = QLineEdit()
  self.label_subject = QLabel("Asunto:")
  self.txt_subject = QLineEdit()
  self.label_dialog = QLabel("Adjunto:")
  self.btn_dialog = QPushButton("Seleccionar ...")
  self.label_body = QLabel("Mensaje: ")
  self.txt_body = QTextEdit()
  self.label_state = QLabel("")
  self.btn_send = QPushButton("Enviar")
  #Crear objeto de la clase FileDialog()
  self.fileDialog = FileDialog()
  
  #Agregar objetos al layout grid
  self.layout.addWidget(self.label_host)
  self.layout.addWidget(self.txt_host)
  self.layout.addWidget(self.chk_tls)
  self.layout.addWidget(self.label_port)
  self.layout.addWidget(self.txt_port)
  self.layout.addWidget(self.label_user)
  self.layout.addWidget(self.txt_user)
  self.layout.addWidget(self.label_pass)
  self.layout.addWidget(self.txt_pass)
  self.layout.addWidget(self.label_from)
  self.layout.addWidget(self.txt_from)
  self.layout.addWidget(self.label_to)
  self.layout.addWidget(self.txt_to)
  self.layout.addWidget(self.label_subject)
  self.layout.addWidget(self.txt_subject)
  self.layout.addWidget(self.label_dialog)
  self.layout.addWidget(self.btn_dialog)
  self.layout.addWidget(self.label_body)
  self.layout.addWidget(self.txt_body)
  self.layout.addWidget(self.label_state)
  self.layout.addWidget(self.btn_send)
  
  #Señal para abrir el cuadro de diálogo de selección de archivos
  self.btn_dialog.clicked.connect(self.openDialog)
  #Señal para proceder a enviar los correos
  self.btn_send.clicked.connect(self.sendMail)
  
 #Método encargado de abrir el cuadro de diálogo de selección de archivos
 def openDialog(self):
  self.fileDialog.open()
  
 #Método encargado de procesar el envío de correos
 def sendMail(self):
  To = self.txt_to.text().split(", ") #Lista con los destinatarios
  #Capturar cualquier posible excepción y mostrarlo en el label label_state
  try:
   #Recorrer los destinatarios
   for destinatario in To:
    #Guardar los valores del formulario
    Host = self.txt_host.text()
    Port = self.txt_port.text()
    User = self.txt_user.text()
    Pass = self.txt_pass.text()
    From = self.txt_from.text()
    Subject = self.txt_subject.text()
    Body = self.txt_body.toPlainText()
    
    #Objeto para procesar el envío de correo
    smtp = smtplib.SMTP(Host, Port)
    #Si el servidor utilizar el protocolo starttls activarlo
    if self.chk_tls.isChecked(): smtp.starttls()
    #Credenciales
    smtp.login(User, Pass)
    #Iniciar la cabecera
    header = MIMEMultipart()
    header['From'] = From
    header['To'] = destinatario
    header["Subject"] = Subject
    msg = MIMEText(Body, 'html') #Content-type:text/html
    header.attach(msg)
    #Lista para agregrar en la cabecera los archivos a enviar
    parts = []
    for file in self.fileDialog.files:
     parts.append(MIMEBase('application', "octet-stream"))
    
    #Nos permite indexar la ruta de los archivos que se encuentran
    #en el atributo files del objeto fileDialog
    x = 0
    #Recorrer archivo a archivo
    for part in parts:
     #Lectura del archivo
     part.set_payload(open(self.fileDialog.files[x], "rb").read())
     #Codificar el archivo en base64
     encoders.encode_base64(part)
     #Extracción del nombre del archivo
     explode = self.fileDialog.files[x].split("/")
     filename = explode[len(explode)-1]
     #Añadir archivo a la cabecera
     part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')
     header.attach(part)
     x = x + 1
    #Enviar el correo al destinatario
    smtp.sendmail(From, destinatario, header.as_string())
    #Terminar la conexión con el servidor
    smtp.quit()
    #Mostrar el proceso
    self.label_state.setText("Enviando a " + destinatario + " ... ")
    
  except Exception as e: 
   #Capturar cualquier posible excepción y mostrarla
   self.label_state.setText(str(e))
    
  parts[:] = [] #Limpiar la lista de archivos
  self.fileDialog.files[:] = [] #Limpiar la lista de archivos
  self.label_state.setText("Envío finalizado")
     
app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()
