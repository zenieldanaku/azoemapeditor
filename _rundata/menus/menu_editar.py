from .basemenu import BaseMenu

class Menu_Editar(BaseMenu):
    def  __init__(self,x,y):
        self.nombre = 'Menu Editar'
        nombres = ['Preferencias...']
        super().__init__(nombres,x,y)

    def Preferencias(self):
        pass