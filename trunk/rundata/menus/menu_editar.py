from widgets import Menu

class Menu_Editar(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Editar'
        self.barra = barra
        opciones = [{'nom':'Preferencias...','cmd':self.Preferencias}]
        super().__init__('Editar',opciones,x,y)

    def Preferencias(self):
        print('preferencias')