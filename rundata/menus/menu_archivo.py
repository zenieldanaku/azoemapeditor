from globales import GLOBALES as G
from pygame import quit as pyquit
from sys import exit as sysexit
from widgets import Menu, FileDiag

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Archivo'
        self.barra = barra
        opciones = [
            {'nom':'Nuevo{}','cmd':self.Nuevo},
            {'nom':'Abrir...{}','cmd':self.Abrir},
            {'nom':'Guardar{}','cmd':self.Guardar},
            {'nom':'Guardar como...{}','cmd':self.Guardar_como},
            {'nom':'Cerrar{}','cmd':self.Cerrar},
            {'nom':'Salir{}','cmd':self.Salir}]
        super().__init__('Archivo',opciones,x,y)
        
    def Nuevo(self): G.nuevo_mapa()
    def Abrir(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.abrirMapa})
    
    def Guardar(self):
        # acá habria que ver si hay cambios.
        FileDiag({'scr':'G','tipo':'G','cmd':self.guardarMapa})
    
    def Guardar_como(self):
        FileDiag({'scr':'G','tipo':'G','cmd':self.guardarMapa})
        
    def Cerrar(self):
        print('cierra el archivo abierto')
    
    def Salir(self):
        pyquit()
        sysexit()
    
    @staticmethod
    def abrirMapa(ruta):
        try:
            G.cargar_mapa(ruta)
        except:
            G.estado = 'Error: El archivo no existe.'
    
    @staticmethod
    def guardarMapa(ruta):
        try:
            G.guardar_mapa(ruta)
            G.estado = "Mapa '"+ruta+"' guardado."
        except: 
            G.estado ='Error: Es necesario cargar un mapa.'