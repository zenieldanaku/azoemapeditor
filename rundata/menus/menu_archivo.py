from globales import Sistema as Sys
from widgets import Menu, FileDiag

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Archivo'
        self.barra = barra
        opciones = [
            {'nom':'Nuevo','cmd':lambda:Sys.nuevoMapa()},
            {'nom':'Abrir',"win":lambda:FileDiag({'scr':'A','tipo':'A','cmd':Sys.abrirMapa})},
            {'nom':'Guardar','cmd':self.Guardar},
            {'nom':'Guardar como','win':lambda:FileDiag({'scr':'G','tipo':'G','cmd':Sys.guardarMapa})},
            {'nom':'Cerrar','cmd':Sys.cerrarMapa},
            {'nom':'Salir','cmd':Sys.salir}]
        super().__init__('Archivo',opciones,x,y)
    
    def Guardar(self):
        # acá habria que ver si hay cambios.
        FileDiag({'scr':'G','tipo':'G','cmd':Sys.guardarMapa})