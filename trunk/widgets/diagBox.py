from widgets import subVentana, BotonAceptarCancelar
from globales import C, color, Sistema, EventHandler
from libs.textrect import render_textrect
from pygame import font, Rect
__all__ = ['Alerta','Pregunta','Error','Info']

class _DiagBox(subVentana):
    def __init__(self,nombre,**opciones):
        super().__init__(C*8-2,C*4-16,nombre,**opciones)
        
class Alerta (_DiagBox):
    layer = 40000
    cerrar = False
    accion_true = None
    accion_false = None
    def __init__(self,texto,accion_si,accion_no,**opciones):
        super().__init__('Alerta',**opciones)
        self.accion_true = accion_si
        self.accion_false = accion_no
        
        self.area = Rect(3,24,self.w-6,self.h-27)
        x,y,w,h=self.x,self.y,self.area.w,self.area.h
        
        fuente = font.SysFont('Verdana',13)
        render = render_textrect(texto,fuente,self.area,(0,0,0),color('sysElmFace'))
        self.image.blit(render,(3,24))
        
        self.btnTrue = BotonAceptarCancelar(self,x+w-(62*2)-12,y+h+1,True,self.aceptar)
        self.btnFalse = BotonAceptarCancelar(self,x+w-62-4,y+h+1,False,self.cancelar)
        self.agregar(self.btnTrue)
        self.agregar(self.btnFalse)
    
    def aceptar(self):
        self.accion_true()
        self.cerrar = True
    
    def cancelar(self):
        self.accion_false()
        self.cerrar = True
        
    def update(self):
        if self.cerrar:
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