from PIL import Image ,ImageOps

#modulo para generar la grafica
import matplotlib.pyplot as plt

nombre_del_archivo="histogramas/Tulips.jpg"
foto=Image.open(nombre_del_archivo) #si la imagen es a color la convertimos a escala de grises
##if foto.mode != 'L':
##    foto=foto.convert('L')

histograma=ImageOps.equalize(foto)
histograma.save("histogramas/corte2.jpg")
##
##plt.figure(1)
##x=range(len(histograma))
##plt.xticks([0, 50, 100, 150, 200, 255])
##plt.bar(x, histograma, align='center')
##plt.title('Histograma')
##plt.xlabel('Valores de intensidad')
##plt.ylabel('Numero de pixeles')
##    
##plt.savefig("histogramas/corte2.jpg", bbox_inches='tight')
##plt.show()





##
##
##from PIL import Image
##
##import matplotlib.pyplot as plt
##
## 
##
##def getRed(redVal):
##    return '#%02x%02x%02x' % (redVal, 0, 0)
##def getGreen(greenVal):
##    return '#%02x%02x%02x' % (0, greenVal, 0)
##def getBlue(blueVal):
##    return '#%02x%02x%02x' % (0, 0, blueVal)
### Create an Image with specific RGB value
##image = Image.open("img_campo/img003_3.jpg") 
##
### Modify the color of two pixels
##image.putpixel((0,1), (1,1,5))
##image.putpixel((0,2), (2,1,5))
### Display the image
##image.show()
### Get the color histogram of the image
##histogram = image.histogram()
### Take only the Red counts
##l1 = histogram[0:256]
### Take only the Blue counts
##l2 = histogram[256:512]
### Take only the Green counts
##l3 = histogram[512:768]
##plt.figure(0)
### R histogram
##for i in range(0, 256):
##    plt.bar(i, l1[i], color = getRed(i), edgecolor=getRed(i), alpha=0.3)
### G histogram
##plt.figure(1)
##for i in range(0, 256):
##    plt.bar(i, l2[i], color = getGreen(i), edgecolor=getGreen(i),alpha=0.3)
### B histogram
##plt.figure(2)
##for i in range(0, 256):
##    plt.bar(i, l3[i], color = getBlue(i), edgecolor=getBlue(i),alpha=0.3)
##plt.show()
##
##






##
##import cv2
##import numpy as np
##from matplotlib import pyplot as plt
##
##img = cv2.imread('images/GoldenGateSunset.png', -1)
##cv2.imshow('GoldenGate',img)
##
##color = ('b','g','r')
##for channel,col in enumerate(color):
##    histr = cv2.calcHist([img],[channel],None,[256],[0,256])
##    plt.plot(histr,color = col)
##    plt.xlim([0,256])
##plt.title('Histogram for color scale picture')
##plt.show()
##
##while True:
##    k = cv2.waitKey(0) & 0xFF     
##    if k == 27: break             # ESC key to exit 
##cv2.destroyAllWindows()
##
##
