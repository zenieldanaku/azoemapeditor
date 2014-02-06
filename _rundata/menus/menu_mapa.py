from .basemenu import BaseMenu

class Menu_Mapa (BaseMenu):
    def  __init__(self,x,y):
        self.nombre = 'Menu Mapa'
        nombres = ['Grilla...','Capas...']
        super().__init__(nombres,x,y)

    def Grilla(self):
        pass
    def Capas(self):
        pass