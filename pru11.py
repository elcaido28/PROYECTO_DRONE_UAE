##import tkinter as tk # Python 3 
##root = tk.Tk() 
### The image must be stored to Tk or it will be garbage collected. 
##root.image = tk.PhotoImage(file="histogramas/paisa.png") 
##label = tk.Label(root, image=root.image, bg='white') 
##root.overrideredirect(True) 
##root.geometry("+250+250") 
##root.lift() 
##root.wm_attributes("-topmost", True) 
##root.wm_attributes("-disabled", True) 
##root.wm_attributes("-transparentcolor", "white") 
##label.pack() 
##label.mainloop() 
##




from PIL import Image, ImageOps

imagen = Image.open("histogramas/paisa.png")
imagen.mode #-> RGB
imagenbn = imagen.convert("L")
imagenbn.show()
imagenbn.save("histogramas/amapolasbn.jpg")






##
##
##############################
######### UNIR 2 IMAGNES #####
##############################
##import pygame
##import sys
### Importamos constantes locales de pygame
##from pygame.locals import *
### Iniciamos Pygame
##pygame.init()
### Creamos una surface (la ventana de juego), asignándole un alto y un ancho
##Ventana = pygame.display.set_mode((1000, 600))
### Le ponemos un título a la ventana
##pygame.display.set_caption("Poniendo Imágenes")
### Cargamos las imágenes
##Fondo = pygame.image.load("histogramas/paisa.png")
##Imagen = pygame.image.load("histogramas/ciudad.png")
### posiciona las imágenes en Ventana
##Ventana.blit(Fondo, (0, 0))
##Ventana.blit(Imagen, (150, 50))
### refresca los gráficos
##pygame.display.flip()
### Bucle infinito para mantener el programa en ejecución
##while True:    
##    # Manejador de eventos
##    for evento in pygame.event.get():
##        # Pulsación de la tecla escape
##        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
##                sys.exit()
