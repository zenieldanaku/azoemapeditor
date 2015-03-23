from widgets import Menu
from globales import Sistema as Sys
from ._cuadroEditarSimbolo import EditarSimbolo
from ._cuadrosEntradas import CuadroEntrada

class Menu_Editar(Menu):
    def  __init__(self,parent,x,y):
        opciones = [
            {"nom":'Deshacer','cmd':lambda:print('deshacer'),'key':'Ctrl+Z'},
            {"nom":'Rehacer','cmd':lambda:print('rehacer'),'key':'Ctrl+Alt+Z'},
            {"nom":'barra'},
            {"nom":'Cortar',"cmd":Sys.cortar,"icon":Sys.iconos['cortar'],'key':'Ctrl+X'},
            {"nom":'Copiar',"cmd":Sys.copiar,"icon":Sys.iconos['copiar'],'key':'Ctrl+C'},
            {"nom":'Pegar',"cmd":Sys.pegar,"icon":Sys.iconos['pegar'],'key':'Ctrl+V'},
            {"nom":'barra'},
            {"nom":'Entradas',"win":CuadroEntrada},
            {"nom":'Simbolo','win':EditarSimbolo},
            {'nom':'Preferencias','win':lambda:print('preferencias'),'key':'Ctrl+P'}
            ]
        super().__init__(parent,'Editar',opciones,x,y)
        
        self.referencias['Rehacer'].serDeshabilitado()
    
    def update(self):
        objeto = self.referencias['Entradas']
        if Sys.PROYECTO == None:
            objeto.serDeshabilitado()
        elif not objeto.enabled:
            objeto.serHabilitado()