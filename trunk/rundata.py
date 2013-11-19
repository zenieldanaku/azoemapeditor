from renderer import Renderer
from widgets import *
from constantes import *



def crear_widgets(fondo):
    add = Renderer.addWidget # function alias
    
    ventana = add(Ventana(fondo.get_size()),0)
    grilla = add(Grilla((2*C)+2,2*C,15*C,15*C))
    add(Barra((17*C)+8, 2*C, 1/2*C, grilla.h))
    add(Barra((2*C)+2, (17*C)+8, grilla.w, 1/2*C))
    add(Herramientas(0,2*C,2*C,16*C))
    add(PanelSimbolos(18*C-1,2*C,6*C,16*C-1))
    
    botones_1 = ['Archivo','Editar','Mapa','Símbolo']
    add(Menu_barra('Menu_1',0,0,24*C,1*C,botones_1))
    add(Menu_barra('Menu_2',0,C,24*C,1*C,[]))
    add(Menu_barra('Menu_3',0,18*C,24*C,1*C,[]))
    add(Menu_barra('estado',0,(19*C),24*C,1*C,[]))
    
    return ventana