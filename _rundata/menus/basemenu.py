from widgets import BaseWidget, BotonMenu, CascadaMenu
from renderer import Renderer

class BaseMenu (BaseWidget):
    cascada = None
    _visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        super().__init__()
        self.boton = BotonMenu(self,nombre,x,y)
        Renderer.addWidget(self.boton,4)
        h = self.boton.rect.h
        self.cascada = CascadaMenu(ops,x,h,h)
    
    def showMenu(self):
        self.cascada.showMenu()

    def hideMenu(self):
        self.cascada.hideMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        self.hideMenu()