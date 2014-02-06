from renderer import Renderer
from widgets import *
from constantes import *
from .BarraMenus import barraMenus
from .BarraHerramientas import barraHerramientas
from .Barra3 import barra3
from .BarraEstado import barraEstado

from pygame import font
font.init()
# no quiero hacer esto, pero no me sale resolverlos como clases estáticas
BarraMenus = barraMenus()
BarraHerramientas = barraHerramientas()
Barra3 = barra3()
BarraEstado = barraEstado()
#
#Renderer.addWidget(Scroll((17*C)+8, 2*C, 1/2*C, grilla.h))
#grilla = Grilla((2*C)+2,2*C,15*C,15*C)
#Renderer.addWidget(grilla)
#Renderer.addWidget(Scroll((2*C)+2, (17*C)+8, grilla.w, 1/2*C))
#Renderer.addWidget(Herramientas(0,2*C,2*C,16*C))
#Renderer.addWidget(PanelSimbolos(18*C-1,2*C,6*C,16*C-1))