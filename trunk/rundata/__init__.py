from .BarraHerramientas import barraHerramientas
from .herramientas import PanelHerramientas
from .BarraEstado import barraEstado
from .simbolos import PanelSimbolos
from .BarraMenus import barraMenus
from .grilla import grilla
from constantes import *
from pygame import font
from widgets import *

font.init()
## no quiero hacer esto, pero no me sale resolverlos como clases estáticas
BarraMenus = barraMenus()
BarraHerramientas = barraHerramientas()
BarraEstado = barraEstado()
Grilla = grilla()
Herramientas = PanelHerramientas()
Simbolos = PanelSimbolos()