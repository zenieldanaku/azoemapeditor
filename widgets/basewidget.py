from pygame.sprite import DirtySprite
from globales import color
from pygame import draw

class BaseWidget(DirtySprite):
    '''clase base para todos los widgets'''
    focusable = True
    # si no es focusable, no se le llaman focusin y focusout
    # (por ejemplo, un contenedor, una etiqueta de texto)
    hasFocus = False
    # indica si el widget está en foco o no.
    enabled = True
    # un widget con enabled==False no recibe ningun evento
    nombre = ''
    # identifica al widget en el renderer
    hasMouseOver = False
    # indica si el widget tuvo el mouse encima o no, por el onMouseOut
    opciones = None
    # las opciones con las que se inicializo
    setFocus_onIn = False
    # if True: Renderer.setFocus se dispara onMouseIn también.
    KeyCombination = ''
    
    layer = 0
    def __init__(self,parent=None,**opciones):
        if parent is not None:
            self.parent = parent
            self.layer = self.parent.layer+1
        self.opciones = opciones
        super().__init__()
        
    def onFocusIn(self):
        self.hasFocus = True
    
    def onFocusOut(self):
        self.hasFocus = False
    
    def onMouseDown(self,mousedata):
        pass
    
    def onMouseUp(self, mousedata):
        pass
    
    def onMouseOver(self):
        pass
    
    def onMouseIn(self):
        self.hasMouseOver = True
    
    def onMouseOut(self):
        self.hasMouseOver = False
    
    def onKeyDown(self, keydata):
        pass
    
    def onKeyUp(self, keydata):
        pass
    
    def onDestruction(self):
        #esta funcion se llama cuando el widget es quitado del renderer.
        pass
    
    @staticmethod
    def _biselar(imagen,colorLuz,colorSombra):
        w,h = imagen.get_size()
        draw.line(imagen, colorSombra, (0,h-2),(w-1,h-2), 2)
        draw.line(imagen, colorSombra, (w-2,h-2),(w-2,0), 2)
        draw.lines(imagen, colorLuz, 0, [(w-2,0),(0,0),(0,h-4)],2)
        return imagen
    
    def reubicar_en_ventana(self,dx=0,dy=0):
        self.rect.move_ip(dx,dy)
        self.x += dx
        self.y += dy
        self.dirty = 1
            
    def __repr__(self):
        return self.nombre