from .baseSubVentana import subVentana
from globales.constantes import C

class PopUp(subVentana):
    def __init__(self,**opciones):
        super().__init__(C,C,4*C,3*C,"popUp",**opciones)