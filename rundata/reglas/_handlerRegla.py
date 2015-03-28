from widgets import BaseWidget, ToolTip
from pygame import Surface, draw, mouse
from ._guias import LineaGuiaX, LineaGuiaY
from globales import EventHandler

class HandlerRegla(BaseWidget):
    selected = False
    pressed = False
    lineas = []
    tip = 'Haga clic y arrastre para generar dos guías'
    def __init__(self,parent,x,y,**opciones):
        super().__init__(**opciones)        
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.HandlerRegla'
        self.image = self._crear()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.w,self.h = self.image.get_size()
        self.tooltip = ToolTip(self,self.tip,self.x,self.y)
    
    @staticmethod
    def _crear():
        imagen =  Surface((16,16))
        imagen.fill((255,255,255),(1,1,14,14))
        draw.line(imagen,(0,0,0),(0,10),(14,10))
        draw.line(imagen,(0,0,0),(10,0),(10,14))
        return imagen
        
    def onMouseDown(self,button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.lineaX = LineaGuiaX(self.parent,len(self.lineas))
            self.lineaY = LineaGuiaY(self.parent,len(self.lineas))
            self.newLine = True
    
    def onMouseUp(self,button):
        if button == 1 and self.enabled:
            self.pressed = False
            self.lineas.append(self.lineaX)
            self.lineas.append(self.lineaY)
            self.lineaX = None
            self.lineaY = None
    
    def onMouseIn(self):
        super().onMouseIn()
        self.ToggleSel(True)
    
    def onMouseOut(self):
        self.ToggleSel(False)
        if not self.pressed:
            super().onMouseOut()
            self.tooltip.hide()
    
    def onMouseOver(self):
        x,y = mouse.get_pos()
        if self.pressed:
            if not self.rect.collidepoint((x,y)) and self.newLine:
                EventHandler.addWidget(self.lineaX)
                EventHandler.addWidget(self.lineaY)
                self.newLine = False
                
            self.moverLineas()
        if self.hasFocus:
            self.tooltip.show()
    
    def ToggleSel(self,select):
        if select and self.enabled:
            draw.line(self.image,(125,255,255),(1,10),(14,10))
            draw.line(self.image,(125,255,255),(10,1),(10,14))
        else:
            draw.line(self.image,(0,0,0),(0,10),(14,10))
            draw.line(self.image,(0,0,0),(10,0),(10,14))
    
    def scroll(self,dx,dy):
        for linea in self.lineas:
            if isinstance(linea, LineaGuiaX):    
                linea.rect.y -= dy
            elif isinstance(linea, LineaGuiaY):
                linea.rect.x -= dx
    
    def moverLineas(self):
        x,y = self.parent.getRelMousePos()
        abs_x,abs_y = mouse.get_pos()
        
        self.lineaX.rect.y = abs_y
        self.lineaY.rect.x = abs_x
        self.lineaX.x = y
        self.lineaY.y = x
    
    def update(self):
        if not self.enabled:
            for linea in self.lineas:
                EventHandler.delWidget(linea)
            self.lineas.clear()
