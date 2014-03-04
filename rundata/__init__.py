from widgets import *
from constantes import *
from .BarraMenus import barraMenus
from .BarraHerramientas import barraHerramientas
from .BarraEntry import barraEntry
from .BarraEstado import barraEstado
from .grilla import grilla
from .simbolos import PanelSimbolos
from .herramientas import PanelHerramientas
from pygame import font

font.init()
## no quiero hacer esto, pero no me sale resolverlos como clases estáticas
BarraMenus = barraMenus()
BarraHerramientas = barraHerramientas()
BarraEntry = barraEntry()
BarraEstado = barraEstado()
Grilla = grilla()
Herramientas = PanelHerramientas()
Simbolos = PanelSimbolos()