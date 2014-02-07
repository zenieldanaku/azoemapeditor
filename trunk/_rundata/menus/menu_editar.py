from .basemenu import BaseMenu

class Menu_Editar(BaseMenu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu Editar'
        self.barra = barra
        opciones = [{'nom':'Preferencias...','cmd':self.Preferencias}]
        super().__init__('Editar',opciones,x,y)

    def Preferencias(self):
        print('preferencias')