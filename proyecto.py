from tkinter import *
#from tkessageBox import *
from PIL import ImageTk, Image
##import tk
##import tkFont
##import ttk
import os
import sys
#import numpy as np
import webbrowser
import platform
import pymysql
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import subprocess
import datetime


def conexionBD():
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()

  
#$$$$$$$$$$$$$  FUNCIONES NUEVAS VENTANAS $$$$$$$$$$$
def ven_informacion():
    w2 = 500
    h2 = 500

    extraW2=ventana.winfo_screenwidth() - w2
    extraH2=ventana.winfo_screenheight() - h2
    ven_inf=Toplevel(ventana, bg="Light Blue")
    ven_inf.title("INFORMACION DE LA HACIENDA")
    ven_inf.geometry("%dx%d%+d%+d" % (w2, h2, extraW2 / 2, extraH2 / 2))
    ven_inf.resizable(width=False, height=False)
    img=PhotoImage(file="imagen/fondo_pantalla2.pgm")
    fondo_pantalla=Label(ven_inf,image=img).place(x=0,y=0, relwidth=1, relheight=1)
    
        
    #&&&&&&&&&&&&&&& CONTENIDO INTERFAZ INFORMACION &&&&&&&&&&&&
    global t1
    global t2
    global t3
    global t4
    global t5
    global t6
    global t7
    t1= StringVar()
    t2= StringVar()
    t3= StringVar()
    t5= StringVar()
    t4= StringVar()
    t6= StringVar()
    t7= StringVar()
    sms= StringVar()
    etiq1=Label(ven_inf, text="Registro de Informacion", font=("Helvetica",18))
    etiq1.place(x=120,y=10)
    
    etiq1=Label(ven_inf, text="Nombre de la Hacienda :", font=("Helvetica",12), bg="Light Blue")
    etiq1.place(x=30,y=60)
    txt1=Entry(ven_inf, textvariable=t1)
    #txt1.insert(0,"1")
    #txt1.bind('<KeyPress>',keyPressCI)
    txt1.place(x=230, y=60, width=200, height=30)

    etiq2=Label(ven_inf, text="Nombre del Propietario :", font=("Helvetica",12), bg="Light Blue")
    etiq2.place(x=30,y=100)
    txt2=Entry(ven_inf, textvariable=t2)
    #txt2.insert(0,"1")
    #txt2.bind('<KeyPress>',keyPressCI)
    txt2.place(x=230, y=100, width=200, height=30)

    etiq3=Label(ven_inf, text="Nº de Hectareas :", font=("Helvetica",12), bg="Light Blue")
    etiq3.place(x=30,y=140)
    txt3=Entry(ven_inf, textvariable=t3)
    #txt3.insert(0,"1")
    #txt3.bind('<KeyPress>',keyPressCI)
    txt3.place(x=230, y=140, width=200, height=30)

    etiq4=Label(ven_inf, text="Nº de Parcelas x Hectarea :", font=("Helvetica",12), bg="Light Blue")
    etiq4.place(x=30,y=180)
    txt4=Entry(ven_inf, textvariable=t4)
    #txt4.insert(0,"1")
    #txt4.bind('<KeyPress>',keyPressCI)
    txt4.place(x=230, y=180, width=200, height=30)

    etiq5=Label(ven_inf, text="Dirección :", font=("Helvetica",12), bg="Light Blue")
    etiq5.place(x=30,y=220)
    txt5=Entry(ven_inf, textvariable=t5)
    #txt5.insert(0,"1")
    #txt5.bind('<KeyPress>',keyPressCI)
    txt5.place(x=230, y=220, width=200, height=30)

    etiq6=Label(ven_inf, text="Telefono :", font=("Helvetica",12), bg="Light Blue")
    etiq6.place(x=30,y=260)
    txt6=Entry(ven_inf, textvariable=t6)
    #txt6.insert(0,"1")
    #txt6.bind('<KeyPress>',keyPressCI)
    txt6.place(x=230, y=260, width=200, height=30)

    btn1=Button(ven_inf, text="Guardar", fg='#0B1447', font=("Helvetica",16),command=guardar_infromacion)
    btn1.place(x=210,y=400)
    
    

def guardar_infromacion():
  
    a=t1.get()
    b=t2.get()
    c=t3.get()
    d=t4.get()
    e=t5.get()
    f=t6.get()
    g=t7.get()
    
    t33=str(c)
    t44=str(d)
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    print("conect_exito..")
    sql = "INSERT INTO informacion (nombre_hacienda,nombre_propietario,n_hectareas,n_parcela_hectarea,direccion,telefono) VALUES('"+a+"','"+b+"','"+t33+"','"+t44+"','"+e+"','"+f+"')"
    cursor.execute(sql)
    conn.commit()
    print("insert_exito..")

    
def usuarios(valor1):
    w2 = 500
    h2 = 300
    extraW2=ventana.winfo_screenwidth() - w2
    extraH2=ventana.winfo_screenheight() - h2
    ven_usu=Toplevel(ventana, bg="Light Blue")
    ven_usu.title("USUARIOS")
    ven_usu.geometry("%dx%d%+d%+d" % (w2, h2, extraW2 / 2, extraH2 / 2))
    ven_usu.resizable(width=False, height=False)
    img=PhotoImage(file="imagen/fondo_pantalla2.pgm")
    fondo_pantalla=Label(ven_usu,image=img).place(x=0,y=0, relwidth=1, relheight=1)
    
        
    #&&&&&&&&&&&&&&& CONTENIDO INTERFAZ INFORMACION &&&&&&&&&&&&
    global t8
    global t9
    global t10
    #global id_dato
    t8= StringVar()
    t9= StringVar()
    t10= StringVar()
    
    etiq1=Label(ven_usu, text="Registro de Usuarios", font=("Helvetica",18))
    etiq1.place(x=120,y=10)
    
    etiq1=Label(ven_usu, text="Nombre de Usuario :", font=("Helvetica",12), bg="Light Blue")
    etiq1.place(x=30,y=60)
    txt1=Entry(ven_usu, textvariable=t8)
    #txt1.insert(0,valor1)
    #txt1.bind('<KeyPress>',keyPressCI)
    txt1.place(x=230, y=60, width=200, height=30)

    etiq2=Label(ven_usu, text="Contraseña :", font=("Helvetica",12), bg="Light Blue")
    etiq2.place(x=30,y=100)
    txt2=Entry(ven_usu, textvariable=t9)
    #txt2.insert(0,"1")
    #txt2.bind('<KeyPress>',keyPressCI)
    txt2.place(x=230, y=100, width=200, height=30)

    etiq3=Label(ven_usu, text="Privilegios :", font=("Helvetica",12), bg="Light Blue")
    etiq3.place(x=30,y=140)
    combo_privi1 = ttk.Combobox(ven_usu,validate ='focus',validatecommand=t10, font=("Helvetica",14),state = NORMAL)
    combo_privi1.insert(0,'PRIVILEGIO')
    combo_privi1.register("")

    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    sql = "SELECT privilegio FROM privilegio"
    cursor.execute(sql)
    print("conect_exito..")
    rows3 = cursor.fetchall()    
    combo_privi1.configure(values = rows3)
    
    combo_privi1.place(x=230, y=140, width=200, height=30)

    
    btn2=Button(ven_usu, text="Guardar", fg='#0B1447', font=("Helvetica",16),command=guardar_usuario)
    btn2.place(x=210,y=200)
    


def guardar_usuario():
  
    a=t8.get()
    b=t9.get()
    c=t10.get()
    d="1"
    
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    print("conect_exito..")
    sql = "INSERT INTO usuarios (usuario,clave,id_empleado,id_privilegio) VALUES('"+a+"','"+b+"','"+d+"','"+str(c)+"')"
    cursor.execute(sql)
    conn.commit()
    print("insert_exito..")

def privilegios():
    w2 = 500
    h2 = 150
    extraW2=ventana.winfo_screenwidth() - w2
    extraH2=ventana.winfo_screenheight() - h2
    ven_usu=Toplevel(ventana, bg="Light Blue")
    ven_usu.title("USUARIOS")
    ven_usu.geometry("%dx%d%+d%+d" % (w2, h2, extraW2 / 2, extraH2 / 2))
    ven_usu.resizable(width=False, height=False)
    img=PhotoImage(file="imagen/fondo_pantalla2.pgm")
    fondo_pantalla=Label(ven_usu,image=img).place(x=0,y=0, relwidth=1, relheight=1)
    
        
    #&&&&&&&&&&&&&&& CONTENIDO INTERFAZ INFORMACION &&&&&&&&&&&&
    global t12
    #global id_dato
    t12= StringVar()
    
    etiq1=Label(ven_usu, text="Registro de Usuarios", font=("Helvetica",18))
    etiq1.place(x=120,y=10)
    
    etiq1=Label(ven_usu, text="Nombre de la Hacienda :", font=("Helvetica",12), bg="Light Blue")
    etiq1.place(x=30,y=60)
    txt1=Entry(ven_usu, textvariable=t12)
    #txt1.insert(0,valor1)
    #txt1.bind('<KeyPress>',keyPressCI)
    txt1.place(x=230, y=60, width=200, height=30)
    
    btn3=Button(ven_usu, text="Guardar", fg='#0B1447', font=("Helvetica",16),command=guardar_priv)
    btn3.place(x=210,y=100)
    
    

def guardar_priv():
  
    a=t12.get()
    
    conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
    cursor = conn.cursor()
    print("conect_exito..")
    sql = "INSERT INTO privilegio (privilegio) VALUES('"+a+"')"
    cursor.execute(sql)
    conn. commit()
    print("insert_exito..")
    

def ven_Empleados():
    LABEL_BG = "#ccc"  # Light gray.
    ROWS, COLS = 2, 5  # Size of grid.
    ROWS_DISP = 3  # Number of rows to display.
    COLS_DISP = 4  # Number of columns to display.

    class MyApp(tk.Tk):
        def __init__(self, title="Sample App", *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.title(title)
            self.configure(background="Gray")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            master_frame = tk.Frame(self, bg="Light Gray", bd=3, relief=tk.RIDGE)
            
            
            master_frame.grid(sticky=tk.NSEW)
            master_frame.columnconfigure(0, weight=1)
            

            label1 = tk.Label(master_frame, text="Lista de Empleados Contents", font=("Helvetica",18))
            label1.grid(row=0, column=0, padx=290, pady=10, sticky=tk.NW)



            # Create a frame for the canvas and scrollbar(s).
            frame2 = tk.Frame(master_frame)
            frame2.grid(row=3, column=0, sticky=tk.NW,padx=(10,10),pady=(60,40))

            # Add a canvas in that frame.
            canvas = tk.Canvas(frame2, bg="Light Gray")
            canvas.grid(row=0, column=0)

            # Create a vertical scrollbar linked to the canvas.
            vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
            vsbar.grid(row=0, column=1, sticky=tk.NS)
            canvas.configure(yscrollcommand=vsbar.set)
    
            # Create a horizontal scrollbar linked to the canvas.
            hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
            hsbar.grid(row=1, column=0, sticky=tk.EW)
            canvas.configure(xscrollcommand=hsbar.set)

            # Create a frame on the canvas to contain the buttons.
            buttons_frame = tk.Frame(canvas, bg="Gray", bd=2)

            # Add the buttons to the frame.
            Helvfont = tkFont.Font(family="Helvetica", size=10, weight="bold")

            button= tk.Label(buttons_frame,text="Asignar",font=Helvfont,relief="ridge",width=10)
            button.grid(column=1,row=1)    
            button= tk.Label(buttons_frame,text="Cedula",font=Helvfont,relief="ridge",width=10)
            button.grid(column=2,row=1)
    
            button= tk.Label(buttons_frame,text="Nombres",font=Helvfont,relief="ridge",width=20)
            button.grid(column=3,row=1)
            button= tk.Label(buttons_frame,text="Apellidos", font=Helvfont,relief="ridge",width=20)
            button.grid(column=4,row=1)
            button= tk.Label(buttons_frame,text="Telefono", font=Helvfont,relief="ridge",width=10)
            button.grid(column=5,row=1)
            button= tk.Label(buttons_frame,text="Direccion", font=Helvfont,relief="ridge",width=60)
            button.grid(column=6,row=1)

            

            conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
            cursor = conn.cursor()
            sql = "SELECT * FROM empleados"
            cursor.execute(sql)
            print("conect_exito..")
            #resul = cursor.fetchone()   o   resul = cursor.fetchall()   numero_de_registros= cursor.rowcount
            rows1 = cursor.fetchall()
            i=1
            

            for row1 in rows1:
                i=i+1
                #id_E[i] = str(row1[0])
                nombre = str(row1[1])
                apellido = str(row1[2])
                cedula = str(row1[3])
                direccion = str(row1[4])
                telefono = str(row1[5])

                #button= tk.Label(buttons_frame,text=cedula, font=Helvfont,relief="ridge",width=10)
                btn1=tk.Button(buttons_frame, text=row1[0], fg='#0B1447', font=("Helvetica",14),command=lambda:usuarios(row1[0]))
                btn1.grid(column=1,row=i)
                button= tk.Label(buttons_frame,text=cedula, font=Helvfont,relief="ridge",width=10)
                button.grid(column=2,row=i)
                button= tk.Label(buttons_frame,text=nombre, font=Helvfont,relief="ridge",width=20)
                button.grid(column=3,row=i)
                button= tk.Label(buttons_frame,text=apellido, font=Helvfont,relief="ridge",width=20)
                button.grid(column=4,row=i)
                button= tk.Label(buttons_frame,text=telefono, font=Helvfont,relief="ridge",width=10)
                button.grid(column=5,row=i)
                button= tk.Label(buttons_frame,text=direccion, font=Helvfont,relief="ridge",width=60)
                button.grid(column=6,row=i)



            # Create canvas window to hold the buttons_frame.
            canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

            buttons_frame.update_idletasks()  # Needed to make bbox info available.
            bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
            #print('canvas.bbox(tk.ALL): {}'.format(bbox))

            # Define the scrollable region as entire canvas with only the desired
            # number of rows and columns displayed.
            w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)


            frame3 = tk.Frame(master_frame, bg="yellow", bd=2, relief=tk.GROOVE)
            frame3.grid(row=5, column=0, sticky=tk.NW)

        

    if __name__ == "__main__":
        app = MyApp("EMPLEADOS")

def ven_Lista_usuario():
    LABEL_BG = "#ccc"  # Light gray.
    ROWS, COLS = 2, 5  # Size of grid.
    ROWS_DISP = 4  # Number of rows to display.
    COLS_DISP = 4  # Number of columns to display.

    class MyApp(tk.Tk):
        def __init__(self, title="Sample App", *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.title(title)
            self.configure(background="Gray")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            master_frame = tk.Frame(self, bg="Light Gray", bd=3, relief=tk.RIDGE)
            
            
            master_frame.grid(sticky=tk.NSEW)
            master_frame.columnconfigure(0, weight=1)
            

            label1 = tk.Label(master_frame, text="Lista de Empleados Contents", font=("Helvetica",18))
            label1.grid(row=0, column=0, padx=290, pady=10, sticky=tk.NW)



            # Create a frame for the canvas and scrollbar(s).
            frame2 = tk.Frame(master_frame)
            frame2.grid(row=3, column=0, sticky=tk.NW,padx=(10,10),pady=(60,40))

            # Add a canvas in that frame.
            canvas = tk.Canvas(frame2, bg="Light Gray")
            canvas.grid(row=0, column=0)

            # Create a vertical scrollbar linked to the canvas.
            vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
            vsbar.grid(row=0, column=1, sticky=tk.NS)
            canvas.configure(yscrollcommand=vsbar.set)
    
            # Create a horizontal scrollbar linked to the canvas.
            hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
            hsbar.grid(row=1, column=0, sticky=tk.EW)
            canvas.configure(xscrollcommand=hsbar.set)

            # Create a frame on the canvas to contain the buttons.
            buttons_frame = tk.Frame(canvas, bg="Gray", bd=2)

            # Add the buttons to the frame.
            Helvfont = tkFont.Font(family="Helvetica", size=10, weight="bold")

            button= tk.Label(buttons_frame,text="Nombres",font=Helvfont,relief="ridge",width=20)
            button.grid(column=1,row=1)    
            button= tk.Label(buttons_frame,text="Apellidos",font=Helvfont,relief="ridge",width=20)
            button.grid(column=2,row=1)
            
            button= tk.Label(buttons_frame,text="Usuario", font=Helvfont,relief="ridge",width=15)
            button.grid(column=3,row=1)
            button= tk.Label(buttons_frame,text="Contraseña", font=Helvfont,relief="ridge",width=15)
            button.grid(column=4,row=1)

            conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
            cursor = conn.cursor()
            sql = "SELECT nombres,apellidos,usuario,clave FROM empleados E inner join usuarios U on U.id_empleado=E.id_empleado"
            cursor.execute(sql)
            print("conect_exito..")
            #resul = cursor.fetchone()   o   resul = cursor.fetchall()
            rows1 = cursor.fetchall()
            i=1
            for row1 in rows1:
                i=i+1
                nombre = str(row1[0])
                apellido = str(row1[1])
                user = str(row1[2])
                clave = str(row1[3])

                #button= tk.Label(buttons_frame,text=cedula, font=Helvfont,relief="ridge",width=10)
                button= tk.Label(buttons_frame,text=nombre, font=Helvfont,relief="ridge",width=20)
                button.grid(column=1,row=i)
                button= tk.Label(buttons_frame,text=apellido, font=Helvfont,relief="ridge",width=20)
                button.grid(column=2,row=i)
                button= tk.Label(buttons_frame,text=user, font=Helvfont,relief="ridge",width=15)
                button.grid(column=3,row=i)
                button= tk.Label(buttons_frame,text=clave, font=Helvfont,relief="ridge",width=15)
                button.grid(column=4,row=i)



            # Create canvas window to hold the buttons_frame.
            canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

            buttons_frame.update_idletasks()  # Needed to make bbox info available.
            bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
            #print('canvas.bbox(tk.ALL): {}'.format(bbox))

            # Define the scrollable region as entire canvas with only the desired
            # number of rows and columns displayed.
            w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)


            frame3 = tk.Frame(master_frame, bg="yellow", bd=2, relief=tk.GROOVE)
            frame3.grid(row=5, column=0, sticky=tk.NW)

        

    if __name__ == "__main__":
        app = MyApp("USUARIOS")

    
def ven_Lista_imagenes():
    LABEL_BG = "#ccc"  # Light gray.
    ROWS, COLS = 2, 5  # Size of grid.
    ROWS_DISP = 3  # Number of rows to display.
    COLS_DISP = 4  # Number of columns to display.

    class MyApp(tk.Tk):
        def __init__(self, title="Sample App", *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            self.title(title)
            self.configure(background="Gray")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            master_frame = tk.Frame(self, bg="Light Gray", bd=3, relief=tk.RIDGE)
            master_frame.grid(sticky=tk.NSEW)
            master_frame.columnconfigure(0, weight=1)
            
            label1 = tk.Label(master_frame, text="Lista de Empleados Contents", font=("Helvetica",18))
            label1.grid(row=0, column=0, padx=290, pady=10, sticky=tk.NW)
            
            



            # Create a frame for the canvas and scrollbar(s).
            frame2 = tk.Frame(master_frame)
            frame2.grid(row=3, column=0, sticky=tk.NW,padx=(10,10),pady=(60,40))
            # Add a canvas in that frame.
            canvas = tk.Canvas(frame2, bg="Light Gray")
            canvas.grid(row=0, column=0)

            # Create a vertical scrollbar linked to the canvas.
            vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
            vsbar.grid(row=0, column=1, sticky=tk.NS)
            canvas.configure(yscrollcommand=vsbar.set)
    
            # Create a horizontal scrollbar linked to the canvas.
            hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
            hsbar.grid(row=1, column=0, sticky=tk.EW)
            canvas.configure(xscrollcommand=hsbar.set)

            # Create a frame on the canvas to contain the buttons.
            buttons_frame = tk.Frame(canvas, bg="Gray", bd=2)

            # Add the buttons to the frame.
            Helvfont = tkFont.Font(family="Helvetica", size=10, weight="bold")
    
            button= tk.Label(buttons_frame,text="Imagen",font=Helvfont,relief="ridge",width=10)
            button.grid(column=1,row=1)    
            button= tk.Label(buttons_frame,text="Imagen Termica",font=Helvfont,relief="ridge",width=20)
            button.grid(column=2,row=1)
            
            button= tk.Label(buttons_frame,text="pocisi", font=Helvfont,relief="ridge",width=20)
            button.grid(column=3,row=1)
            button= tk.Label(buttons_frame,text="temperatura", font=Helvfont,relief="ridge",width=10)
            button.grid(column=4,row=1)
            button= tk.Label(buttons_frame,text="Hectarea", font=Helvfont,relief="ridge",width=10)
            button.grid(column=5,row=1)
            button= tk.Label(buttons_frame,text="Parcela", font=Helvfont,relief="ridge",width=10)
            button.grid(column=6,row=1)
    

            conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
            cursor = conn.cursor()
            sql = "SELECT * FROM captura_imagen"
            cursor.execute(sql)
            print("conect_exito..")
            #resul = cursor.fetchone()   o   resul = cursor.fetchall()
            rows1 = cursor.fetchall()
            i=1
            for row1 in rows1:
                i=i+1
                imagen1 = str(row1[1])
                imagen2 = str(row1[2])
                latitud = str(row1[3])
                longitud = str(row1[4])
                temperatura = str(row1[5])
                hectarea = str(row1[6])
                parcela = str(row1[7])
                
                
                #img2 = ImageTk.PhotoImage(Image.open(imagen2))   OJO

                gata=imagen1
                img = ImageTk.PhotoImage(Image.open(gata))
            
                button= tk.Label(buttons_frame,text=img)
                button.grid(column=1,row=i)
                button= tk.Label(buttons_frame,text=imagen2,width=20)
                button.grid(column=2,row=i)
                
                button= tk.Label(buttons_frame,text=latitud+" - "+longitud, font=Helvfont,relief="ridge",width=20)
                button.grid(column=3,row=i)
                button= tk.Label(buttons_frame,text=temperatura, font=Helvfont,relief="ridge",width=10)
                button.grid(column=4,row=i)
                button= tk.Label(buttons_frame,text=hectarea, font=Helvfont,relief="ridge",width=10)
                button.grid(column=5,row=i)
                button= tk.Label(buttons_frame,text=parcela, font=Helvfont,relief="ridge",width=10)
                button.grid(column=6,row=i)



            # Create canvas window to hold the buttons_frame.
            canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

            buttons_frame.update_idletasks()  # Needed to make bbox info available.
            bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.
            #print('canvas.bbox(tk.ALL): {}'.format(bbox))

            # Define the scrollable region as entire canvas with only the desired
            # number of rows and columns displayed.
            w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)


            frame3 = tk.Frame(master_frame, bg="Blue", bd=2, relief=tk.GROOVE)
            frame3.grid(row=5, column=0, sticky=tk.NW)

        

    if __name__ == "__main__":
        app = MyApp("LISTA DE IMAGENES")
        
        


#$$$$$$$$$$$$$  VENTANA INICIO DEL SISITEMA $$$$$$$$$$$
ventana = Tk()
w = 900
h = 600
pad=3
extraW=ventana.winfo_screenwidth() - w
extraH=ventana.winfo_screenheight() - h
ventana.geometry("{0}x{1}+0+0".format(ventana.winfo_screenwidth()-pad, ventana.winfo_screenheight()-pad))
canvas = Canvas(ventana, width=1000, height=500)
canvas.pack()
img=PhotoImage(file="imagen/fondo_pantalla2.pgm")
fondo_pantalla=Label(ventana,image=img).place(x=0,y=0, relwidth=1, relheight=1)
ventana.title("SISTEMA - HACIENDA ROSALIA")

##eti_m1=Label(ventana,relief="ridge" )
##eti_m1.place(x=46,y=96, width=156, height=136)
##path = 'img_campo/icono_menu1.jpg' 
##img = ImageTk.PhotoImage(Image.open(path)) 
##eti_m2=Label(ventana, image=img)
##eti_m2.place(x=50,y=100, width=150, height=100)
##eti_m3=Label(ventana, text="Lista de Imagenes", font=("Helvetica",12))
##eti_m3.place(x=50,y=200, width=150, height=30)




############################ MENU ######################################
"""Creacion De Los Menus"""
barraMenu = Menu(ventana, tearoff=0)

#barraMenu.setbg("red")

mnuOpciones = Menu(barraMenu)
mnuUnidad1 = Menu(barraMenu)
mnuUnidad2 = Menu(barraMenu)
mnuUnidad3 = Menu(barraMenu)
mnuUnidad4 = Menu(barraMenu)
mnuUnidad5 = Menu(barraMenu)
mnuUnidad6 = Menu(barraMenu)
mnuUnidad6_sub = Menu(barraMenu)
############################################################################################
"""Menu Unidad I"""


mnuUnidad1.add_command(label = "Información", command = ven_informacion)
mnuUnidad1.add_separator()
mnuUnidad1.add_command(label = "Asignación De Trabajo", command = "")

############################################################################################
"""Menu Unidad II"""
mnuUnidad2.add_command(label = "Lista de imagenes", command = "")

############################################################################################
"""Menu Unidad III"""
mnuUnidad3.add_command(label = "Metricas Termograficas", command = "")
mnuUnidad3.add_separator()
mnuUnidad3.add_command(label = "Temperatura", command = "")

############################################################################################
"""Menu Unidad IV"""
mnuUnidad4.add_command(label = "Imagenes", command =ven_Lista_imagenes)
mnuUnidad4.add_separator()
mnuUnidad4.add_command(label = "Tamaño De Imagenes", command = "")
mnuUnidad4.add_separator()
mnuUnidad4.add_command(label = "Corte De imagen", command = "")
############################################################################################
"""Menu Unidad V"""
mnuUnidad5.add_command(label = "Asignación de Imagen", command = "")
mnuUnidad5.add_separator()
mnuUnidad5.add_command(label = "Interpolado", command = "")

############################################################################################
"""Menu Unidad V"""
#mnuUnidad6.add_command(label = "Login", command = "")
mnuUnidad6.add_cascade(label = "Login", menu = mnuUnidad6_sub)
mnuUnidad6_sub.add_command(label = "Usuarios", command = ven_Lista_usuario)
mnuUnidad6_sub.add_command(label = "Privilegios", command = privilegios)

mnuUnidad6.add_separator()
mnuUnidad6.add_command(label = "Empleados", command = ven_Empleados)

############################################################################################
"""Menu Opciones"""
mnuOpciones.add_command(label = "LIMPIAR", command = "")
mnuOpciones.add_separator()
mnuOpciones.add_command(label = "SALIR", command = "")
############################################################################################

barraMenu.add_cascade(label = "Mantenimiento", font=("Calibri",20), menu = mnuUnidad1)
barraMenu.add_cascade(label = "GPS", menu = mnuUnidad2)
barraMenu.add_cascade(label = "Termografia", menu = mnuUnidad3)
barraMenu.add_cascade(label = "Procesamientos", menu = mnuUnidad4)
barraMenu.add_cascade(label = "Interpolación", menu = mnuUnidad5)
barraMenu.add_cascade(label = "Administracón", menu = mnuUnidad6)
barraMenu.add_cascade(label = "Reportes", menu = mnuOpciones)
ventana.config(menu = barraMenu)
############################################################################################

ventana.mainloop()
 
