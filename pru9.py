from Tkinter import *

# Configuración de la raíz
root = Tk()

label = Label(root, text="Nombre muy largo")
label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

entry = Entry(root)
entry.grid(row=0, column=1, padx=5, pady=5)
entry.config(justify="right", state="normal")

label2 = Label(root, text="Contraseña")
label2.grid(row=1, column=0, sticky="w", padx=5, pady=5)

entry2 = Entry(root)
entry2.grid(row=1, column=1, padx=5, pady=5)
entry2.config(justify="center", show="?")



gata=("img_campo/icono_menu1.jpg")
img = PhotoImage(open=gata)
            
image= Label(root,image=img)
image.grid (fila = 0, columna = 2, columnas = 2, rowspan = 2,pegajoso = W + E + N + S, padx = 5, pady = 5)

button1.grid (fila = 2, columna = 2)
button2.grid (fila = 2, columna = 3)

# Finalmente bucle de la aplicación
root.mainloop()
