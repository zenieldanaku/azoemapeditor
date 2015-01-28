from widgets import subVentana, Boton
from globales import C, color, Sistema, EventHandler
from libs.textrect import render_textrect
from pygame import font, Rect
__all__ = ['Alerta','Pregunta','Error','Info']

class _DiagBox(subVentana):
    def __init__(self,**opciones):
        super().__init__(C*8-2,C*5-3,"popUp",**opciones)
        
class Alerta (_DiagBox):
    layer = 40000
    status = False
    def __init__(self,texto):
        super().__init__()
        self.area = Rect(3,24,self.w-6,self.h-27)
        fuente = font.SysFont('Verdana',13)
        render = render_textrect(texto,fuente,self.area,(0,0,0),color('sysElmFace'))
        
        self.btnTrue = Boton(self,self.x+3,self.y+self.area.h,'verdad',self.aceptar,'Aceptar',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.image.blit(render,(3,24))
        self.agregar(self.btnTrue)
    
    def aceptar(self):
        self.status = True
        
    def update(self):
        if self.status:
            EventHandler.delWidget(self)
            return True
        else:
            return False
        

class Pregunta (_DiagBox):
    pass

class Error (_DiagBox):
    pass

class Info (_DiagBox):
    pass

#254 x 157
#C*8-2,C*5-3