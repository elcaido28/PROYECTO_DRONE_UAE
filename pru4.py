import Tkinter as tk
import tkFont
import pymysql
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

        master_frame = tk.Frame(self, bg="Light Blue", bd=3, relief=tk.RIDGE)
        master_frame.grid(sticky=tk.NSEW)
        master_frame.columnconfigure(0, weight=1)

        label1 = tk.Label(master_frame, text="Lista de Empleados Contents", font=("Helvetica",18))
        label1.grid(row=0, column=0, padx=250, pady=10, sticky=tk.NW)



        # Create a frame for the canvas and scrollbar(s).
        frame2 = tk.Frame(master_frame)
        frame2.grid(row=3, column=0, sticky=tk.NW,padx=(10,10),pady=(60,40))

        # Add a canvas in that frame.
        canvas = tk.Canvas(frame2, bg="Yellow")
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
        buttons_frame = tk.Frame(canvas, bg="Red", bd=2)

        # Add the buttons to the frame.
        Helvfont = tkFont.Font(family="Helvetica", size=10, weight="bold")
    
        button= tk.Label(buttons_frame,text="Cedula",font=Helvfont,relief="ridge",width=10)
        button.grid(column=1,row=1)
    
        button= tk.Label(buttons_frame,text="Nombres",font=Helvfont,relief="ridge",width=18)
        button.grid(column=2,row=1)
        button= tk.Label(buttons_frame,text="Apellidos", font=Helvfont,relief="ridge",width=18)
        button.grid(column=3,row=1)
        button= tk.Label(buttons_frame,text="Telefono", font=Helvfont,relief="ridge",width=10)
        button.grid(column=4,row=1)
        button= tk.Label(buttons_frame,text="Direccion", font=Helvfont,relief="ridge",width=60)
        button.grid(column=5,row=1)
    

        conn = pymysql.connect("localhost","root","root","proy_drone_hacienda",port=3306)
        cursor = conn.cursor()
        sql = "SELECT * FROM empleados"
        cursor.execute(sql)
        print("conect_exito..")
        #resul = cursor.fetchone()   o   resul = cursor.fetchall()
        rows1 = cursor.fetchall()
        i=1
        for row1 in rows1:
            i=i+1
            nombre = str(row1[1])
            apellido = str(row1[2])
            cedula = str(row1[3])
            direccion = str(row1[4])
            telefono = str(row1[5])

            button= tk.Label(buttons_frame,text=cedula, font=("Helvetica",10),relief="ridge",width=10)
            button.grid(column=1,row=i)
            button= tk.Label(buttons_frame,text=nombre, font=("Helvetica",10),relief="ridge",width=18)
            button.grid(column=2,row=i)
            button= tk.Label(buttons_frame,text=apellido, font=("Helvetica",10),relief="ridge",width=18)
            button.grid(column=3,row=i)
            button= tk.Label(buttons_frame,text=telefono, font=("Helvetica",10),relief="ridge",width=10)
            button.grid(column=4,row=i)
            button= tk.Label(buttons_frame,text=direccion, font=("Helvetica",10),relief="ridge",width=60)
            button.grid(column=5,row=i)



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
    app = MyApp("EMPLEADOS")
    app.mainloop()
