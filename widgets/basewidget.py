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
    nombre = ''
    #identifica al widget en el renderer
    hasMouseOver = False
    #indica si el widget tuvo el mouse encima o no, por el onMouseOut
    
    ##las opciones con las que se inicializo
    opciones = None
    
    def __init__(self, **opciones):
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
    
    def _dibujarBorde(self):
        from colores import color
        from pygame import draw
        draw.line(self.image, color(self.opciones.get('colorBordeSombra', 'sysElmShadow')), (0,self.rect.h-2),(self.rect.w-1,self.rect.h-2), 2)
        draw.line(self.image, color(self.opciones.get('colorBordeSombra', 'sysElmShadow')), (self.rect.w-2,self.rect.h-2),(self.rect.w-2,0), 2)
        draw.lines(self.image, color(self.opciones.get('colorBordeLuz', 'sysElmLight')), False, [(self.rect.w-1,0),(0,0),(0,self.rect.h-3)], 2)
    
    def update(self):
        self.dirty = 1
    
    def __repr__(self):
        return self.nombre