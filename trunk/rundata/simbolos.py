from pygame import Rect,Surface,draw,mouse
from pygame.sprite import LayeredDirty
from widgets import Marco, BaseWidget
from widgets import Boton, DropDownList, Entry
from renderer import Renderer
from colores import color
from constantes import *
from globales import SharedFunctions as shared, GLOBALES as G

class PanelSimbolos(Marco):
    simbolos = None
    def __init__(self,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = color('sysElmFace')

        super().__init__(18*C-1,2*C,6*C,16*C-1,**opciones)
        self.nombre = 'PanelSimbolos'
        self.simbolos = LayeredDirty()
        self.PrevArea = area_prev(self,self.x+3,self.y+10*C-2,self.w-6,6*C)
        ejemplo = Simbolo(self.PrevArea,16,16)
        self.PrevArea.agregarSimbolo(ejemplo)
        
        self.BtnMob = Boton(self,18*C+1,self.y+1,'Mobs',self.VerPanelMobs,'Mob',**{'w':3*C-1})
        self.BtnProp = Boton(self,21*C,self.y+1,'Props',self.VerPanelProps,'Prop',**{'w':3*C-1})
        self.PanelMobs = SubPanelMobs(self,self.x+2,self.y+C-5,self.w-4,9*C)
        self.PanelProps = SubPanelProps(self,self.x+2,self.y+C-5,self.w-4,9*C)
        self.agregar(self.BtnMob)
        self.agregar(self.BtnProp)
        self.agregar(self.PanelMobs,50)
    
    def VerPanelMobs(self):
        self.PanelProps.visible = False
        self.PanelMobs.visible = True
        
    def VerPanelProps(self):
        self.PanelMobs.visible = False
        self.PanelProps.visible = True
    
    def update(self):
        if G.HabilitarTodo:
            if not self.BtnMob.enabled: self.BtnMob.serHabilitado()
            if not self.BtnProp.enabled: self.BtnProp.serHabilitado()
        else:
            if self.BtnMob.enabled: self.BtnMob.serDeshabilitado()
            if self.BtnProp.enabled: self.BtnProp.serDeshabilitado()
            

class _SubPanel(Marco):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(x,y,w,h,False,**opciones)
        self.parent = parent
        self.visible = False
    
    def update(self):
        for item in self.contenido:
            item.visible = self.visible
            item.enabled = item.visible
        self.dirty = 1

class SubPanelMobs(_SubPanel):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(parent,x,y,w,h,**opciones)
        self.nombre = self.parent.nombre+'.SubPanelMobs'
        self.BtnNuevo = Boton(self,self.x+self.w-29,self.y+1,'Nuevo',self.cmdNuevo,'+')
        self.EntryNom = Entry(self,'Nombre',self.x+1,self.y+3,5*C-3)
        self.EntryNom.enabled = False
        self.dropTipo = DropDownList(self,'Tipo',self.x+1,self.y+C,6*C-6,['¿Tipo?','Monstruo','Victima'])
        self.agregar(self.BtnNuevo)
        self.agregar(self.EntryNom)
        self.agregar(self.dropTipo)
    
    def cmdNuevo(self):
        self.EntryNom.enabled = True
        self.EntryNom.setText('¿Nombre?')


class SubPanelProps(_SubPanel):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(parent,x,y,w,h,**opciones)
        self.nombre = self.parent.nombre+'.SubPanelProps'

class area_prev(Marco):
    simbolos = None
    def __init__(self,parent,x,y,w,h,**opciones):
        if 'colorGrilla' not in opciones:
            opciones['colorGrilla'] = (150,200,200)
        super().__init__(x,y,w,h,False,**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.AreaPrev'
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        grilla = self.opciones['colorGrilla']
        self.image = self._dibujar_grilla(self._biselar(self.image,sombra,luz),grilla)
        self.area = Rect(self.x+2,self.y+2,self.w-4,self.h-18)
        self.simbolos = LayeredDirty()
        
    @staticmethod
    def _dibujar_grilla(imagen,color):
        w,h = imagen.get_size()
        marco = Rect(0,0,w-2,h-2)
        for i in range(1*C,6*C,C):
            draw.line(imagen, color, (i,marco.top), (i,marco.bottom))
            draw.line(imagen, color, (marco.left,i), (marco.right,i))
        return imagen
    
    def agregarSimbolo(self,simbolo):
        simbolo.rect.x += self.area.x
        simbolo.rect.y += self.area.y

        if simbolo not in self.simbolos:
            self.simbolos.add(simbolo)
        self.agregar(simbolo)

class Simbolo (BaseWidget):
    pressed = False
    enArea = True
    copiar = False
    def __init__(self,parent,w,h,**opciones):
        super().__init__(**opciones)
        self.x,self.y = 0,0
        self.w,self.h = w,h
        self.parent = parent
        self.nombre = self.parent.nombre+'.Simbolo.'+'ejemplo'
        self.image = Surface((self.w,self.h))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            if self.copiar:
                shared.copiar(self)
                shared.pegar('Grilla.Canvas')
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        x,y = mouse.get_pos()
        dx = x-self.w//2
        dy = y-self.h//2
        self.enArea = self.parent.area.collidepoint(dx,dy)
        if self.pressed:
            if self.enArea:
                self.mover(dx,dy)
            elif x-self.rect.x < 0:
                self.copiar = True
        
    def mover(self,dx=0,dy=0):
        self.rect.x = dx
        self.rect.y = dy
        self.x,self.y = dx,dy
    
    def copy(self):
        return Simbolo(self.parent,self.w,self.h)
