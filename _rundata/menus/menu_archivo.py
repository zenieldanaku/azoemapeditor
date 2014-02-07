from .basemenu import BaseMenu
from widgets import BotonMenu
from pygame import quit as pyquit
from sys import exit as sysexit


class Menu_Archivo(BaseMenu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu Archivo'
        self.barra = barra
        opciones = [
            {'nom':'Nuevo','cmd':self.Nuevo},
            {'nom':'Abrir...','cmd':self.Abrir},
            {'nom':'Guardar','cmd':self.Guardar},
            {'nom':'Guardar como...','cmd':self.Guardar_como},
            {'nom':'Cerrar','cmd':self.Cerrar}]
        super().__init__('Archivo',opciones,x,y)
        
    
    def Nuevo(self):
        print('nuevo arhivo')
    def Abrir(self):
        print('abrir achivo')
    def Guardar(self):
        print('guardar archivo')
    def Guardar_como(self):
        print('guardar archivo con otro nombre')
    
    def Cerrar(self):
        pyquit()
        sysexit()