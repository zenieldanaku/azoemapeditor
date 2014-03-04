from widgets import Menu
from pygame import quit as pyquit
from sys import exit as sysexit
from globales import GLOBALES as G

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu Archivo'
        self.barra = barra
        cascadas = {
            'Nuevo':[
                
            ]
        }
        opciones = [
            {'nom':'Nuevo','cmd':self.Nuevo},
            {'nom':'Abrir...','cmd':self.Abrir},
            {'nom':'Guardar','cmd':self.Guardar},
            {'nom':'Guardar como...','cmd':self.Guardar_como},
            {'nom':'Cerrar','cmd':self.Cerrar},
            {'nom':'Salir','cmd':self.Salir}]
        super().__init__('Archivo',opciones,x,y)
        
    
    def Nuevo(self): G.nuevo_mapa()
    def Abrir(self):
        print('abrir achivo')
    def Guardar(self): G.guardar_mapa()
    def Guardar_como(self):
        print('guardar archivo con otro nombre')
    def Cerrar(self):
        print('cierra el archivo abierto')
    
    def Salir(self):
        pyquit()
        sysexit()