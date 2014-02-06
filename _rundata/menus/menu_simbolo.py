from .basemenu import BaseMenu

class Menu_Simbolo (BaseMenu):
    def  __init__(self,x,y):
        self.nombre = 'Menu Simbolo'
        nombres = ['Mobs...','Props...']
        super().__init__(nombres,x,y)
        
    def Mobs(self):
        pass
    def Props(self):
        pass