from widgets import BarraMenu, Entry
from renderer import Renderer
from constantes import *

class barra3 (BarraMenu):
    def __init__(self):
        nombre = 'Menu_3'
        x,y = 0,18*C
        w,h = 24*C,1*C
        
        super().__init__(nombre,x,y,w,h)
        self.focusable = False
        self.entry = Entry(5,y+5,int(self.rect.w/3)*2)
        Renderer.addWidget(self)
        Renderer.addWidget(self.entry,1)
