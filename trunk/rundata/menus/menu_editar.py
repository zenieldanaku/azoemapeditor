from widgets import Menu
from globales import SharedFuntions as shared

class Menu_Editar(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Editar'
        self.barra = barra
        opciones = [
            {"nom":'Cortar',"cmd":self.Cortar},
            {"nom":'Copiar',"cmd":self.Copiar},
            {"nom":'Pegar',"cmd":self.Pegar},
            {'nom':'Preferencias...','cmd':lambda:print('preferencias')}]
        super().__init__('Editar',opciones,x,y)

    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')