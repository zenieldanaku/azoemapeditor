from widgets import BaseWidget
from pygame import mouse, PixelArray

class SimboloBase (BaseWidget):
    img_pos = None #imagen normal
    img_neg = None #imagen semitransparente
    img_sel = None #imagen seleccionada
    img_cls = None #imagen de colisiones
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
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            x,y = mouse.get_pos()
            self.px = x-self.x
            self.py = y-self.y
        elif button == 3:
            self.context.show()
    
    def onMouseOut(self):
        super().onMouseOut()
        self.pressed = False
    
    def hideMenu(self):
        print('dummy')
    
    @staticmethod
    def _crear_transparencia(imagen):
        pxArray = PixelArray(imagen)
        for y in range(imagen.get_height()):
            for x in range(imagen.get_width()):
                _color = imagen.unmap_rgb(pxArray[x,y])
                if _color.a == 255: _color.a = 200
                pxArray[x,y] = _color
        return pxArray.surface