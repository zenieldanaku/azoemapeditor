from pygame.sprite import DirtySprite

class BaseWidget(DirtySprite):
    '''clase base para todos los widgets'''
    focusable = True
    # si no es focusable, no se le llaman focusin y focusout
    #(por ejemplo, un contenedor, una etiqueta de texto)
    hasFocus = False
    # indica si el widget está en foco o no.
    enabled = True
    #un widget con enabled==False no recibe ningun evento
    
    def __init__(self):
        super().__init__()
    
    def onFocusIn(self):
        pass
    
    def onFocusOut(self):
        pass
    
    def onClick(self, mousedata):
        pass
    
    def onMouseDown(self,mousedata):
        pass
    
    def onMouseUp(self, mousedata):
        pass
    
    def onKeyDown(self, keydata):
        pass
    
    def onKeyPress(self, keydata):
        pass
    
    def onKeyUp(self, keydata):
        pass