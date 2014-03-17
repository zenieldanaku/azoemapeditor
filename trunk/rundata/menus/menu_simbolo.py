from widgets import Menu

class Menu_Simbolo (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Simbolo'
        self.barra = barra
        opciones = [{'nom':'Mobs...','cmd':self.Mobs},
                   {'nom':'Props...','cmd':self.Props}]
        super().__init__('Simbolo',opciones,x,y)
        
    def Mobs(self):
        print('mobs')
    def Props(self):
        print('props')