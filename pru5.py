import Tkinter as tk 
from PIL import ImageTk, Image 

path = 'img_campo/img001.jpg' 

root = tk.Tk() 
img = ImageTk.PhotoImage(Image.open(path)) 
panel = tk.Label(root, image = img) 
panel.pack(side = "bottom", fill = "both", expand = "yes") 
root.mainloop() 
