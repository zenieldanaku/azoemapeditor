from globales import GLOBALES as G, Resources as r
from widgets import Menu, FileDiag

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Mapa'
        self.barra = barra
        cascadas = {
            'imagen':[
                {'nom':'Fondo','cmd':self.Fondo},
                {'nom':'Colisiones','cmd':self.Colisiones}]
        }
        opciones = [{'nom':'Grilla...','cmd':self.Grilla},
                   {'nom':'Capas...','cmd':self.Capas},
                   {'nom':'Imagen >','csc':cascadas['imagen']}]
        super().__init__('Mapa',opciones,x,y)

    def Grilla(self):
        print('grilla')
    
    def Capas(self):
        print('capas')
       
    def Fondo(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.setRutaFondo})
        
    def Colisiones(self):
        FileDiag({'scr':'A','tipo':'A','cmd':self.setRutaColis})
    
    @staticmethod
    def setRutaFondo(ruta):
        G.ruta = ruta
        G.cargar_imagen('Fondo')
    
    @staticmethod
    def setRutaColis(ruta):
        G.ruta = ruta
        G.cargar_imagen('Colisiones')