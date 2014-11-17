from widgets import Menu
from globales import Sistema as Sys
from ._cuadroEditarSimbolo import EditarSimbolo

class Menu_Editar(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Editar'
        self.barra = barra
        opciones = [
            {"nom":'Deshacer','cmd':lambda:print('deshacer'),'key':'Ctrl+Z'},
            {"nom":'Rehacer','cmd':lambda:print('rehacer'),'key':'Ctrl+Alt+Z'},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":self.Cortar,"icon":Sys.iconos['cortar'],'key':'Ctrl+X'},
            {"nom":'Copiar',"cmd":self.Copiar,"icon":Sys.iconos['copiar'],'key':'Ctrl+C'},
            {"nom":'Pegar',"cmd":self.Pegar,"icon":Sys.iconos['pegar'],'key':'Ctrl+V'},
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