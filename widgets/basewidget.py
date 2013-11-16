from pygame.sprite import DirtySprite
from pygame import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP

class BaseWidget(DirtySprite):
    '''clase base para todos los widgets'''
    focusable = True
    # si no es focusable, no se le llaman focusin y focusout
    #(por ejemplo, un contenedor, una etiqueta de texto)
    hasFocus = False
    # indica si el widget está en foco o no.
    enabled = True
    #un widget con enabled==False no recibe ningun evento
    nombre = ''
    #identifica al widget en el renderer
    
    def __init__(self):
        super().__init__()
    
    def onFocusIn(self):
        self.hasFocus = True
    
    def onFocusOut(self):
        self.hasFocus = False
    
    def onMouseDown(self,mousedata):
        pass
    
    def onMouseUp(self, mousedata):
        pass
    
    def onKeyDown(self, keydata):
        pass
    
    def onKeyUp(self, keydata):
        pass
    
    def update(self,events):
        for event in events:
            if event.type == KEYDOWN:
                return self.onKeyDown(event)
            elif event.type == KEYUP:
                return self.onKeyUp(event)
            elif event.type == MOUSEBUTTONDOWN:
                return self.onMouseDown(event)
            elif event.type == MOUSEBUTTONUP:
                return self.onMouseUp(event)
            
    