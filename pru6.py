import Tkinter as tk
import tkFileDialog
from PIL import ImageTk, Image


root = tk.Tk()

pic = tkFileDialog.askopenfilename()

img = Image.open(pic)

o_size = img.size   #Tama�o original de la imagen
f_size = (400, 400) #Tama�o del canvas donde se mostrar� la imagen


factor = min(float(f_size[1])/o_size[1], float(f_size[0])/o_size[0])
width = int(o_size[0] * factor)
height = int(o_size[1] * factor)

rImg= img.resize((width, height), Image.ANTIALIAS)
rImg = ImageTk.PhotoImage(rImg)

canvas = tk.Canvas(root, width=f_size[0], height= f_size[1])
canvas.create_image(f_size[0]/2, f_size[1]/2, anchor=tk.CENTER, image=rImg, tags="img")
canvas.pack(fill=None, expand=False)

root.mainloop()
