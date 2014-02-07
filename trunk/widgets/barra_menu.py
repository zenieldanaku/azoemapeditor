from .basewidget import BaseWidget
from constantes import *
from pygame import Surface,draw
from pygame.sprite import LayeredDirty
from renderer import Renderer
from .boton_menu import BotonMenu


class BarraMenu(BaseWidget):
    def __init__(self,nom_menu,x,y,w,h):
        super().__init__()

        self.nombre = nom_menu
        self.image = Surface((w,h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,w-2,h-2),2)
