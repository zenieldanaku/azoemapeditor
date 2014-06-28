from globales import Sistema as Sys
from widgets import Menu, FileDiag

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Mapa'
        self.barra = barra
        cascadas = {'imagen':[
                {'nom':'Fondo','win':lambda:FileDiag({'scr':'A','tipo':'A','cmd':Sys.setRutaFondo})},
                {'nom':'Colisiones','win':lambda:FileDiag({'scr':'A','tipo':'A','cmd':Sys.setRutaColis})}]}
        opciones = [{'nom':'Grilla','cmd':lambda:print('grilla')},
                   {'nom':'Capas','cmd':lambda:print('capas')},
                   {'nom':'Imagen','csc':cascadas['imagen']}]
        super().__init__('Mapa',opciones,x,y)