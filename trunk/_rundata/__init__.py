from renderer import Renderer
from widgets import *
from constantes import *
from .BarraMenus import barraMenus
from .BarraHerramientas import barraHerramientas
from .Barra3 import barra3
from .BarraEstado import barraEstado

from pygame import font
font.init()
## no quiero hacer esto, pero no me sale resolverlos como clases estáticas
BarraMenus = barraMenus()
BarraHerramientas = barraHerramientas()
Barra3 = barra3()
BarraEstado = barraEstado()