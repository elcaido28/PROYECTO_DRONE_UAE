from Tkinter import *
v0=Tk()
v0.title("Gato")
v0.resizable(0,0)

color,nl,matriz,ganador=["red"],[],[0,0,0,0,0,0,0,0,0],[0]

def imprimir(t): print t
def doit(f): v0.after(100,f) # Evento por tiempo

# Crea un gato
def gato():
    ind=0
    c1,c2=0,0
    while ind < 9:
        nl.append(Button(v0,text="",width=10,height=5,bg="white"))
        nl[ind].grid(row=c2,column=c1)
        ind+=1
        if c1==2: c1,c2=0,c2+1
        else: c1+=1
    nl[0].config(command=lambda: jugar(0)), nl[1].config(command=lambda: jugar(1))
    nl[2].config(command=lambda: jugar(2)), nl[3].config(command=lambda: jugar(3))
    nl[4].config(command=lambda: jugar(4)), nl[5].config(command=lambda: jugar(5))
    nl[6].config(command=lambda: jugar(6)), nl[7].config(command=lambda: jugar(7))
    nl[8].config(command=lambda: jugar(8))

def juego_finalizado(): # Revisa si el gato está lleno. Si lo está devuelve True
    ind,largo=0,len(matriz)
    while ind < largo:
        if matriz[ind] == 0:
            return False
            break
        ind+=1
    return True

def tres_linea(lista):
    if matriz[lista[0]] != 0 and matriz[lista[1]] != 0 and matriz[lista[2]] != 0:
        if matriz[lista[0]] == matriz[lista[1]] == matriz[lista[2]]:
            ganador[0]=matriz[lista[0]]
            return True
    return False

def gana():
    if tres_linea([0,1,2]) or tres_linea([3,4,5]) or tres_linea([6,7,8]) or tres_linea([0,3,6]) or tres_linea([1,4,7]) or tres_linea([2,5,8]) or tres_linea([0,4,8]) or tres_linea([2,4,6]):
        return True

def limpiar_botones():
    color="white"
    ind,largo=0,len(nl)
    while ind < largo:
        nl[ind].config(bg=color)
        ind+=1
    matriz[0],matriz[1],matriz[2],matriz[3],matriz[4],matriz[5],matriz[6],matriz[7],matriz[8]=0,0,0,0,0,0,0,0,0

def declarar_ganador():
    v0.after(200,declarar_ganador)
    if gana():
        limpiar_botones()
        v0.withdraw()
        v1=Toplevel(v0)
        if ganador[0] == 1:
            l1=Label(v1,text="Ganador: Jugador 1 (Azul)",font=(16))
            color[0]="red"
        if ganador[0] == 2:
            l1=Label(v1,text="Ganador: Jugador 2 (Rojo)",font=(16))
            color[0]="blue"
        l1.pack()
        b1=Button(v1,text="OK",command=lambda: v1.withdraw() or v0.deiconify(),font=(16))
        b1.pack()
        v1.focus_force()

def reiniciar_juego():
    v0.after(200,reiniciar_juego)
    if juego_finalizado():
        v0.withdraw()
        v1=Toplevel(v0)
        v1.title("Finalizado")
        v1.resizable(0,0)
        l1=Label(v1,text="Nadie Ganó.",font=(16))
        l1.pack()
        b1=Button(v1,text="OK",command=lambda: v1.withdraw() or v0.deiconify(),font=(16))
        b1.pack()
        doit(limpiar_botones())

def jugar(posicion):
    if matriz[posicion] != 0:
        print "Ya se jugó en esta posición"
    else:
        if color[0]=="red":
            matriz[posicion]=1
            color[0]="blue"
            nl[posicion].config(bg=color)
        elif color[0]=="blue":
            matriz[posicion]=2
            color[0]="red"
            nl[posicion].config(bg=color)
        print "ESTADO DE LA MATRIZ:",matriz

gato()
declarar_ganador()
reiniciar_juego()
v0.mainloop()
