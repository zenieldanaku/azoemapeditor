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
            {"nom":'Cortar',"cmd":Sys.cortar,"icon":Sys.iconos['cortar'],'key':'Ctrl+X'},
            {"nom":'Copiar',"cmd":Sys.copiar,"icon":Sys.iconos['copiar'],'key':'Ctrl+C'},
            {"nom":'Pegar',"cmd":Sys.pegar,"icon":Sys.iconos['pegar'],'key':'Ctrl+V'},
            {"nom":'barra'},
            {"nom":'Entradas',"cmd":self.Entrada},
            {"nom":'Simbolo','win':EditarSimbolo},
            {'nom':'Preferencias','win':lambda:print('preferencias'),'key':'Ctrl+P'}
            ]
        super().__init__('Editar',opciones,x,y)
        
        self.referencias['Rehacer'].serDeshabilitado()

    def Entrada(self):
        print('config entrada')