from globales import Sistema as Sys, EventHandler, color, C, LAYER_COLISIONES,LAYER_FONDO
from widgets import BaseWidget, ScrollH, ScrollV, Boton, BotonToggle, Marco, ToolTip, BotonCerrar
from pygame.sprite import LayeredDirty
from pygame import Surface,Rect,draw,font,K_SPACE,mouse
from .SpecialCanvas import SpecialCanvas
import os

class Grilla(Marco):
    canvas = None
    ScrollX = None
    ScrollY = None
    BtnVerGr = None
    BtnVerCapa = None
    verGrilla = False
    verRegla = False
    def __init__(self):
        self.nombre = 'Grilla'
        super().__init__(0,19,15*C+15,15*C+16,False)
        
        self.canvas = SpecialCanvas(self,self.x+16,self.y+16,15*C,15*C,(15*C,15*C))
        self.canvas.ScrollX = ScrollH(self.canvas,self.x+16,self.y+self.h)
        self.canvas.ScrollY = ScrollV(self.canvas,self.x+self.w,self.y+16)
        self.canvas.Grilla = _grilla(self,self.x+16,self.y+16,15*C,15*C)
        
        i = Sys.iconos #alias
        
        self.BtnVerCapa = BotonToggle(self,19*C+6,23,'BtnVerCapa',self.cmdVerCapa,[i['ver_fondo'],i['ver_cls'],i['ver_dis']],"Alterna entre el mapa de colisiones y la imagen de fondo")
        self.BtnVerGr = BotonToggle(self,19*C+6,C+23,'BtnVerGr',self.cmdVerGr,[i['grilla'],i['grilla_tog'],i['grilla_dis']],"Muestra u oculta la grilla")
        self.BtnCerrarMapa = BotonCerrar(self,self.w+1,self.y,15,15,'BtnCerrarMapa',Sys.cerrarProyecto)
        self.canvas.ReglaX = ReglaH(self.canvas,self.x+15,self.y,15*C+1)
        self.canvas.ReglaY = ReglaV(self.canvas,self.x,self.y+15,15*C+1)
        self.ReglaHandler = HandlerRegla(self.canvas,self.x,self.y)
        
        self.agregar(self.canvas)
        self.agregar(self.canvas.ScrollX)
        self.agregar(self.canvas.ScrollY)
        self.agregar(self.BtnCerrarMapa)
        self.agregar(self.BtnVerGr)
        self.agregar(self.BtnVerCapa)
        self.agregar(self.canvas.ReglaX)
        self.agregar(self.canvas.ReglaY)
        self.agregar(self.ReglaHandler)
        
        self.habilitar(False)
    #Funciones de comando para los botones
    def cmdVerGr(self):
        if self.verGrilla:
            self.quitar(self.canvas.Grilla)
            self.verGrilla = False
        else:
            self.agregar(self.canvas.Grilla)
            self.verGrilla = True
        
    def cmdVerCapa(self):
        capas = self.canvas.capas
        capas.switch_layer(LAYER_COLISIONES,LAYER_FONDO)
        
        if Sys.capa_actual == LAYER_FONDO:
            Sys.capa_actual = LAYER_COLISIONES
        elif Sys.capa_actual == LAYER_COLISIONES:
            Sys.capa_actual = LAYER_FONDO
    
    def habilitar(self,control):
        if control:
            self.canvas.ScrollX.enabled = True
            self.canvas.ScrollY.enabled = True
            self.BtnVerCapa.serHabilitado()
            self.BtnVerGr.serHabilitado()
            self.canvas.ReglaX.enabled = True
            self.canvas.ReglaY.enabled = True
            self.ReglaHandler.enabled = True
            self.canvas.enabled = True
        else:
            self.canvas.ScrollX.enabled = False
            self.canvas.ScrollY.enabled = False
            self.BtnVerCapa.serDeshabilitado()
            self.BtnVerGr.serDeshabilitado()
            self.canvas.ReglaX.enabled = False
            self.canvas.ReglaY.enabled = False
            self.ReglaHandler.enabled = False
            self.canvas.enabled = False
        
    def update(self):
        if Sys.PROYECTO is None:
            self.BtnCerrarMapa.serDeshabilitado()
        else:
            if not self.BtnCerrarMapa.enabled:
                self.BtnCerrarMapa.serHabilitado()
                
        self.dirty = 1
        
class _grilla(BaseWidget):
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.focusable = False
        self.nombre = self.parent.nombre+'._grilla'
        self.FONDO = self._crear(w,h,C)
        self.clip = Rect(0,0,15*C,15*C)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h,cuadro):
        marco = Rect(0,0,w,h)
        base = Surface(marco.size)
        _color = (100,200,100)
        for x in range(cuadro,(h//cuadro)*cuadro,cuadro):
            draw.line(base, _color, (x,marco.top), (x,marco.bottom),1)
        for y in range(cuadro,(w//cuadro)*cuadro,cuadro):
            draw.line(base, _color, (marco.left,y-1), (marco.right,y-1),1)
            
        base.set_colorkey((0,0,0))
        
        return base
    
    def actualizar_tamanio(self,w,h):
        self.FONDO = self._crear(w,h,C)
        self.clip.topleft = 0,0
        self.image = self.FONDO.subsurface(self.clip)
        
    def scroll(self,dx,dy):
        self.clip.y += dy
        self.clip.x += dx
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.y -= dy
            self.clip.x -= dx
        
class BaseRegla(BaseWidget):
    pressed = False
    tip = 'Haga clic y arrastre para generar una guía '
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent
    
    def actualizar_tamanio(self,nuevotamanio):
        self.FONDO = self.crear(nuevotamanio)
        self.clip.topleft = 0,0
        self.image = self.FONDO.subsurface(self.clip)
        
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            self.linea = LineaGuia(self,*self.lin)
            EventHandler.addWidget(self.linea,layer = self.parent.layer+1)
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            self.linea = None
            
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
        self.tooltip.hide()

    def onMouseOver(self):
        if self.pressed:
            self.moverLinea()
        if self.hasFocus:
            self.tooltip.show()

class ReglaH(BaseRegla):
    def __init__(self,parent,x,y,w,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaH'
        self.FONDO = self.crear(w)
        self.w,self.h = w,self.FONDO.get_height()
        self.lin = self.x+1,self.y+self.h,self.parent.Tw,1
        self.clip = Rect(0,0,15*C,self.h)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.image.get_rect(topleft =(self.x,self.y))
        self.tooltip = ToolTip(self,self.tip+'horizontal',self.x,self.y)
        
    @staticmethod
    def crear(w):
        fuente = font.SysFont('verdana',8)
        regla = Surface((w,C//2))
        regla.fill((255,255,255),(1,1,w-2,14))
        j = -1
        for i in range(1,33):
            j+=1
            draw.line(regla,(0,0,0),(i*C,0),(i*C,16))
            digitos = [i for i in str(j*C)]
            gx = 0
            for d in range(len(digitos)):
                render = fuente.render(digitos[d],True,(0,0,0),(255,255,255))
                dx = (i-1)*C+gx+4
                regla.blit(render,(dx,4))
                gx += 4
                
        return regla

    def moverLinea(self):
        x,y = self.parent.getRelMousePos()
        y += self.y+self.h
        self.linea.rect.y = y
    
    def scroll(self,dx):
        self.clip.x += dx
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.x -= dx

class ReglaV(BaseRegla):
    def __init__(self,parent,x,y,h,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaV'
        self.FONDO = self.crear(h)
        self.w,self.h = self.FONDO.get_width(),h
        self.lin = self.x+self.w,self.y+1,1,self.parent.Th
        self.clip = Rect(0,0,self.w,15*C)
        self.image = self.FONDO.subsurface(self.clip)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.tooltip = ToolTip(self,self.tip+'vertical',self.x,self.y)
    
    @staticmethod
    def crear(h):
        fuente = font.SysFont('verdana',8)
        regla = Surface((C//2,h))
        regla.fill((255,255,255),(1,1,14,h-2))
        
        j = -1
        for i in range(1,33):
            j+=1
            draw.line(regla,(0,0,0),(0,i*C),(C//2,i*C))
            digitos = [i for i in str(j*C)]
            gy = 0
            for d in range(len(digitos)):
                render = fuente.render(digitos[d],True,(0,0,0),(255,255,255))
                dy = (i-1)*C+gy+1
                regla.blit(render,(4,dy))
                gy += 9
    
        return regla
        
    def moverLinea(self):
        x,y = self.parent.getRelMousePos()
        x += self.x+self.w
        self.linea.rect.x = x
    
    def scroll(self,dy):
        self.clip.y += dy
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.y -= dy
    
class HandlerRegla(BaseWidget):
    selected = False
    pressed = False
    tip = 'Haga clic y arrastre para generar dos guías'
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.HandlerRegla'
        self.image = self._crear()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.w,self.h = self.image.get_size()
        self.linX = -1,0,1,self.parent.Th
        self.linY = self.x,self.y+self.h,self.parent.Tw,1
        self.tooltip = ToolTip(self,self.tip,self.x,self.y)
    
    @staticmethod
    def _crear():
        imagen =  Surface((16,16))
        imagen.fill((255,255,255),(1,1,14,14))
        draw.line(imagen,(0,0,0),(0,10),(14,10))
        draw.line(imagen,(0,0,0),(10,0),(10,14))
        return imagen
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            self.lineaX = LineaGuia(self,*self.linX)
            self.lineaY = LineaGuia(self,*self.linY)
            EventHandler.addWidget(self.lineaX,layer = self.parent.layer+1500)
            EventHandler.addWidget(self.lineaY,layer = self.parent.layer+1500)
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
    
    def onMouseIn(self):
        super().onMouseIn()
        self.ToggleSel(True)
    
    def onMouseOut(self):
        self.ToggleSel(False)
        if not self.pressed:
            super().onMouseOut()
            self.tooltip.hide()
    
    def onMouseOver(self):
        if self.pressed:
            self.moverLineas()
        self.tooltip.show()
    
    def ToggleSel(self,select):
        if select and self.enabled:
            draw.line(self.image,(125,255,255),(1,10),(14,10))
            draw.line(self.image,(125,255,255),(10,1),(10,14))
        else:
            draw.line(self.image,(0,0,0),(0,10),(14,10))
            draw.line(self.image,(0,0,0),(10,0),(10,14))
    
    def moverLineas(self):
        x,y = self.parent.getRelMousePos()
        
        x += self.x+self.w
        y += self.y+self.h
        
        self.lineaX.rect.x = x
        self.lineaY.rect.y = y

class LineaGuia (BaseWidget):
    pressed = False
    locked = False
    def __init__(self,parent,x,y,w,h,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.LineaGuia'
        self.base_x,self.base_y = x,y
        #self.max_x,self.max_y = self.parent.Tw,self.parent.Th
        self.x,self.y,self.w,self.h = x,y,w,h
        self.image = Surface((self.w,self.h))
        self.image.fill((120,255,255))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
         
        if self.w > self.h:
            self.nombre += '.W'
        else:
            self.nombre += '.H'
    
    def onMouseDown(self,button):
        self.pressed = True
    
    def onMouseUp(self,button):
        self.pressed = False
        
    def onMouseIn(self):
        super().onMouseIn()
            
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
        
    def desplazar(self):
        x,y = mouse.get_pos()
        if self.w > self.h:
            if y > self.base_y:
                self.rect.y = y
        else:
            if x > self.base_x:
                self.rect.x = x

    def update(self):
        if self.pressed and not self.locked:
            self.desplazar()
            
        self.x,self.y,self.w,self.h = self.rect
        self.dirty = 1