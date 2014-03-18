from widgets import Menu

class Menu_Simbolo (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Simbolo'
        self.barra = barra
        opciones = [{'nom':'Mobs...','cmd':lambda:print('mobs')},
                   {'nom':'Props...','cmd':lambda:print('props')}]
        super().__init__('Simbolo',opciones,x,y)