from .basewidget import BaseWidget
from pygame import mouse

class SimboloBase (BaseWidget):
    pressed = False
    dx,dy = 0,0
    def __init__(self,parent,data,**opciones):
        super().__init__(**opciones)
        self.data = data
        self.parent = parent
        self.x,self.y = self.data['pos']
        self._nombre = self.data['nombre']
        self.nombre = self.parent.nombre+'.Simbolo.'+self._nombre
        self._imagen = self.data['image']
        self.w,self.h = self._imagen.get_size()
        self.rect = self._imagen.get_rect(topleft=(self.x,self.y))
        self.px,self.py = self.rect.topleft
        
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
    
    def _arrastrar(self):
        abs_x,abs_y = mouse.get_pos()
        new_x,new_y = abs_x-self.x,abs_y-self.y
        
        dx = new_x-self.px
        dy = new_y-self.py
        
        return dx,dy
    
    def mover(self,dx=0,dy=0):
        self.rect.move_ip(dx,dy)
        self.x += dx
        self.y += dy