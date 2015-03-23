from .basewidget import BaseWidget
from pygame import Rect, Surface, draw

class Checkbox(BaseWidget):
    state = False
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.x,self.y = x,y
        
        self.nombre = self.parent.nombre+".checkbox"
        self.img_true = self._crear(True)
        self.img_false = self._crear(False)
        
        self.image = self.img_false
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(checked):
        lado = 12
        img = Surface((lado,lado))
        img.fill((255,255,255),(1,1,lado-2,lado-2))
        
        if checked:
            draw.aaline(img,(0,0,0),[2,2],[9,10]) # \
            draw.aaline(img,(0,0,0),[2,10],[9,2]) # /
        
        return img
    
    def check(self):
        self.state = not self.state
    
    def onMouseDown(self,dummy):
        self.check()
    
    def update(self):
        if self.state:
            self.image = self.img_true
        else:
            self.image = self.img_false
        
        self.dirty = 1