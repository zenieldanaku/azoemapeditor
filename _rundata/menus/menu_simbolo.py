from .basemenu import BaseMenu

class Menu_Simbolo (BaseMenu):
    def  __init__(self,x,y,barra):
        self.barra = barra
        self.nombre = 'Menu Simbolo'
        opciones = [{'nom':'Mobs...','cmd':self.Mobs},
                   {'nom':'Props...','cmd':self.Props}]
        super().__init__('Simbolo',opciones,x,y)
        
    def Mobs(self):
        print('mobs')
    def Props(self):
        print('props')