from PIL import Image


imagen1 = Image.open("img_union/IMG123.jpg")
imagen2 = Image.open("img_union/IMG124.jpg")
imagen3 = Image.open("img_union/img-unidas.jpg")
imagen4 = Image.open("img_union/img-unidas1.jpg")

img_acum=int(imagen1.size[0])+int(imagen2.size[0])+int(imagen3.size[0])
img_acum2=int(imagen1.size[1])
final = Image.new("RGB",(img_acum,img_acum2+img_acum2),"black")

final.paste(imagen1, (0,0))
final.paste(imagen2, (int(imagen1.size[0]),0))
final.paste(imagen3, (img_acum-int(imagen3.size[0]),0))
final.paste(imagen4, (0,img_acum2))
final.show()
final.save("img_union/img-unidas2.jpg")
