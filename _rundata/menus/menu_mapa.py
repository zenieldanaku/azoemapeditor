from .basemenu import BaseMenu

class Menu_Mapa (BaseMenu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu Mapa'
        self.barra = barra
        opciones = [{'nom':'Grilla...','cmd':self.Grilla},
                   {'nom':'Capas...','cmd':self.Capas}]
        super().__init__('Mapa',opciones,x,y)

    def Grilla(self):
        print('grilla')
    def Capas(self):
        print('capas')