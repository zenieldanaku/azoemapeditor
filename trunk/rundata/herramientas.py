from widgets import Marco
from constantes import *

class PanelHerramientas(Marco):
    x,y,w,h = 0,0,0,0
    
    def __init__(self,**opciones):
        super().__init__(0,2*C,2*C,16*C,**opciones)
        self.nombre = 'herramientas'        