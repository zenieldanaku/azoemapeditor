from globales import GLOBALES as G, SharedFuntions as shared
from pygame import quit as pyquit
from sys import exit as sysexit
from widgets import Menu, FileDiag

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Archivo'
        self.barra = barra
        opciones = [
            {'nom':'Nuevo{}','cmd':lambda:shared.nuevo_mapa()},
            {"nom":'Abrir...{}',"cmd":lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.abrirMapa})},
            {'nom':'Guardar{}','cmd':self.Guardar},
            {'nom':'Guardar como...{}','cmd':lambda:FileDiag({'scr':'G','tipo':'G','cmd':shared.guardarMapa})},
            {'nom':'Cerrar{}','cmd':self.Cerrar},
            {'nom':'Salir{}','cmd':self.Salir}]
        super().__init__('Archivo',opciones,x,y)
        
    def Guardar(self):
        # acá habria que ver si hay cambios.
        FileDiag({'scr':'G','tipo':'G','cmd':shared.guardarMapa})
        
    def Cerrar(self):
        print('cierra el archivo abierto')
    
    def Salir(self):
        pyquit()
        sysexit()
        
