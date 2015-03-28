from widgets import BaseWidget, ToolTip
from pygame import Surface, Rect, font, draw, mouse
from globales import C, EventHandler
from ._guias import LineaGuiaX, LineaGuiaY

class BaseRegla(BaseWidget):
    pressed = False
    lineas = [] #list
    linea = None #object
    tip = 'Haga clic y arrastre para generar una guía'+' '#el espacio es intencional
    
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)
        self.lineas = []
        self.x,self.y = x,y
        self.parent = parent
    
    def actualizar_tamanio(self,nuevotamanio):
        self.FONDO = self.crear(nuevotamanio)
        self.clip.topleft = 0,0
        self.image = self.FONDO.subsurface(self.clip)
        
    def onMouseUp(self,button):
        if button == 1 and self.enabled:
            self.pressed = False
            self.lineas.append(self.linea)
            self.linea = None
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
        self.tooltip.hide()

    def onMouseOver(self):
        x,y = mouse.get_pos()
        if self.pressed:
            if not self.rect.collidepoint((x,y)) and self.newLine:
                EventHandler.addWidget(self.linea)
                self.newLine = False
                
            self.moverLinea()
        if self.hasFocus:
            self.tooltip.show()
    
    def update(self):
        if not self.enabled:
            for linea in self.lineas:
                EventHandler.delWidget(linea)
            self.lineas.clear()

class ReglaH(BaseRegla):
    def __init__(self,parent,x,y,w,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaH'
        self.FONDO = self.crear(w)
        self.w,self.h = w,self.FONDO.get_height()
        self.lin = 'w'
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
        abs_x,abs_y = mouse.get_pos()
        x,y = self.parent.getRelMousePos()
        
        self.linea.rect.y = abs_y
        self.linea.y = y
    
    def scroll(self,dx,dy):
        self.clip.x += dx
        self.image.set_clip(self.clip)
        self.image = self.FONDO.subsurface(self.clip)
        for i in range(len(self.lineas)):
            self.lineas[i].rect.y -= dy
    
    def onMouseDown(self,button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.linea = LineaGuiaX(self.parent,len(self.lineas))
            self.newLine = True

class ReglaV(BaseRegla):
    def __init__(self,parent,x,y,h,**opciones):
        super().__init__(parent,x,y,**opciones)
        self.nombre = self.parent.nombre+'.ReglaV'
        self.FONDO = self.crear(h)
        self.w,self.h = self.FONDO.get_width(),h
        self.lin = 'h'
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
        abs_x,abs_y = mouse.get_pos()
        x,y = self.parent.getRelMousePos()

        self.linea.rect.x = abs_x
        self.linea.x = x
    
    def scroll(self,dx,dy):
        self.clip.y += dy
        self.image.set_clip(self.clip)
        self.image = self.FONDO.subsurface(self.clip)
        for i in range(len(self.lineas)):
            self.lineas[i].rect.x -= dx
        
    def onMouseDown(self,button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.linea = LineaGuiaY(self.parent,len(self.lineas))
            self.newLine = True