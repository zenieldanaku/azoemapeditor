from globales import Sistema as Sys, C
from widgets import Menu, subVentana, Marco

class Menu_Editar(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Editar'
        self.barra = barra
        opciones = [
            {"nom":'Cortar',"cmd":self.Cortar},
            {"nom":'Copiar',"cmd":self.Copiar},
            {"nom":'Pegar',"cmd":self.Pegar},
            {"nom":'barra'},
            {"nom":'Entradas',"cmd":self.Entrada},
            {"nom":'Simbolo','win':lambda:EditarSimbolo()}
            #{'nom':'Preferencias','win':lambda:cuadroPreferencias()}
            ]
        super().__init__('Editar',opciones,x,y)

    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    
    def Entrada(self):
        print('config entrada')

class EditarSimbolo(subVentana):
    def __init__(self):
        self.nombre = 'Editar Simbolo'
        super().__init__(4*C,3*C,12*C,10*C,self.nombre)
        x,y,w,h = self.x,self.y,self.w,self.h
        area = Marco(x+C,y+C,C*4,C*4)
        self.agregar(area)