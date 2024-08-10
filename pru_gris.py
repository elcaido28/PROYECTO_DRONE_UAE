from PIL import Image,ImageTk,ImageDraw
import tkinter
import numpy as np
import matplotlib.pyplot as plt

import time
import sys
import os, glob
import pygame
from pygame.locals import Color
######### transponer - poner opacidad ##########
def opacidad():
    img=plt.imread('imagen/atardecer.jpg')
    plt.imshow(img)
    plt.show()
    cropped_img=img[0:1000,0:1000]
    img=plt.imsave('imagen/atardecer.png',cropped_img)  

    img2=plt.imread('imagen/atardecer.png')
    opr=img2 * 0.864

    print(opr)
    plt.imshow(opr)
    plt.show()
    img2=plt.imsave('imagen/atardecer.png',opr)

  # union de 2 imagenes

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
  image3 = changeImageSize(800, 500, image1)
  image4 = changeImageSize(800, 500, image2)
  # Make sure the images have alpha channels

  image3.putalpha(1)
  image4.putalpha(1)
  # Display the images
  #image3.show()
  #image4.show()
  # Do an alpha composite of image4 over image3
  alphaComposited = Image.alpha_composite(image3, image4)
  #alphaBlended = Image.blend(image4, image3,.1)
  #alphaBlended.show()
  # Display the alpha composited image

  alphaComposited.show()


######### estcala de gris ##########
def escala_gris():
    ruta=('imagen/atardecer.jpg')
    img=Image.open(ruta)
    img.show()
    img2=img
    i=0
    mm=3
    a2=0
    while i<img2.size[0]:
        j=0
        while j<img2.size[1]:
            r,b,g=img2.getpixel((i,j))        
            g=(b+g+r)/4
            gris=int(g)
            pixel=tuple([gris,gris,gris])
            #print(pixel)
            img2.putpixel((i,j),(gris,gris,gris,20))
 
            j+=1
        i+=1
    img2.show()

######### porcentaje maximo ##########



def escala_max():
    ruta=('imagen/atardecer.jpg')
    img=Image.open(ruta)
    img.show()
    img2=img
    i=0
    r2=0
    b2=0
    g2=0
    a2=0
    while i<img2.size[0]:
        j=0
        while j<img2.size[1]:
            #r,g,b,a=img2.getpixel((i,j))   #para  .png
            r,g,b=img2.getpixel((i,j))  
            #print(r,b,r,a)  #para  .png
            r2+=+r
            g2+=+g
            b2+=+b
            a=1
            #a2+=+a  #para  .png
            #g=(r+g+b+a)/6    #para  .png
            g=(r+g+b+a)/3
            gris=int(g)
            #pixel=tuple([gris,gris,gris,gris])   #para  .png
            pixel=tuple([gris,gris,gris,gris])    
            img2.putpixel((i,j),pixel)
            j+=1
        i+=1
    ran=j*i
    r2=r2/ran
    g2=g2/ran
    b2=b2/ran    
    #a2=a2/ran     #para  .png
    #print(int(r2),b2,r2,a2)     #para  .png
    print(int(r2),int(g2),int(b2))
    rojo=(int(r2)*100)/255
    amarillo=(int(r2)+int(g2))/2
    amarillo=(int(amarillo)*100)/255
    blanco=3
    if amarillo > 10 :
        blanco=(int(b2)*100)/255

    print("% rojo="+str(int(rojo)),"% amarillo="+str(int(amarillo)),"% blanco="+str(int(blanco)))
    img2.save('Foto123.png')
    img2.show()

######### convertir imagen ##########
        
def processImage(numero): 
    i = Image.new("RGB", (16,16))
    d = ImageDraw.Draw(i)
    d.text((2,2), "55", "#ff0000")
    name_file = 'imagen/atardecer.jpg'
    filename = os.path.join(linux_settings.MEDIA_ROOT, name_file)
    i.save(open(filename, "wb"), "PNG")
    filename_url = linux_settings.MEDIA_URL + name_file
    return filename_url

def array_ss():
    ar=[]
    dato="43sdsv"
    k=0
    for i in range(4):
        ar.append(dato)
        print(ar)

    for j in ar:
        print(j)

        
array_ss() 


