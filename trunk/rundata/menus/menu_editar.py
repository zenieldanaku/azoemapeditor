from widgets import Menu
from ._cuadroPreferencias import cuadroPreferencias

class Menu_Editar(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Editar'
        self.barra = barra
        opciones = [
            {"nom":'Cortar',"cmd":self.Cortar},
            {"nom":'Copiar',"cmd":self.Copiar},
            {"nom":'Pegar',"cmd":self.Pegar},
            {"nom":'Entradas',"cmd":self.Entrada},
            {'nom':'Preferencias','win':lambda:cuadroPreferencias()}]
        super().__init__('Editar',opciones,x,y)

    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    
    def Entrada(self):
        print('config entrada')


