from .BarraEstado import barraEstado
from .simbolos import PanelSimbolos
from .BarraMenus import barraMenus
from .Grilla import Grilla
from constantes import *
from pygame import font
from widgets import *

font.init()
## no quiero hacer esto, pero no me sale resolverlos como clases estáticas
BarraMenus = barraMenus()
BarraEstado = barraEstado()
Grilla = Grilla()
Simbolos = PanelSimbolos()

