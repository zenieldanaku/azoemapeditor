from globales import GLOBALES as G, Resources as r
from globales import SharedFunctions as shared
from widgets import Menu, FileDiag

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Mapa'
        self.barra = barra
        cascadas = {'imagen':[
                {'nom':'Fondo','win':lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.setRutaFondo})},
                {'nom':'Colisiones','win':lambda:FileDiag({'scr':'A','tipo':'A','cmd':shared.setRutaColis})}]}
        opciones = [{'nom':'Grilla','cmd':lambda:print('grilla')},
                   {'nom':'Capas','cmd':lambda:print('capas')},
                   {'nom':'Imagen','csc':cascadas['imagen']}]
        super().__init__('Mapa',opciones,x,y)