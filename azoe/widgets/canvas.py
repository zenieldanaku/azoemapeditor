from pygame import Surface, mouse, mask,Rect,draw
from . import BaseWidget

class Canvas(BaseWidget):
    
    clip = None
    FONDO = None
    doc_w = None
    doc_h = None
    pressed = False
    shift = False
    eleccion = Rect(0,0,0,0)
    SeleccionMultiple = False
    def __init__(self,parent,x,y,w,h,clip,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = (255,255,245)
        if 'colorCuadro' not in opciones:
            opciones['colorCuadro'] = (191,191,191)
        super().__init__(parent,**opciones)
        self.nombre = self.parent.nombre+'.Canvas'
        self.x,self.y = x,y
        self.w,self.h = clip
        self.elX,self.elY = 0,0
        self.Tw,self.Th = w,h
        self.FONDO = Surface((w,h))
        self.doc_w,self.doc_h = w,h
        self.pintarFondoCuadriculado()
        self.image = self.FONDO.subsurface(0,0,self.w,self.h)
        self.image.set_clip((0,0,self.w,self.h))
        self.clip = self.image.get_clip()
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
    
    def pintarFondoCuadriculado(self,C=32):
        self.FONDO.fill(self.opciones['colorFondo'])
        for y in range(self.FONDO.get_height()//C):
            for x in range(self.FONDO.get_width()//C):
                if y%2 == 0:
                    if x%2 ==0:
                        self.FONDO.fill(self.opciones['colorCuadro'],(x*C,y*C,C,C))
                else:
                    if x%2 != 0:
                        self.FONDO.fill(self.opciones['colorCuadro'],(x*C,y*C,C,C))
    
    def onMouseDown(self,button):
        x,y = self.getRelMousePos()
        tiles = []
        if button == 1 or button == 3:
            if hasattr(self,'tiles'):
                selected = 0
                for tile in self.tiles:
                    if tile.selected:
                        selected += 1
                        if selected > 1:
                            break
            
            if not self.shift:
                if not self.SeleccionMultiple:
                    for tile in self.tiles:
                        tile.serDeselegido()
            tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                item = tiles[-1]
                mascara = mask.from_surface(item.image)
                if mascara.get_at((x-item.x,y-item.y)):
                    item.onMouseDown(button)
                    if selected > 1:
                        self.SeleccionMultiple = True                    
            else:
                for tile in self.tiles:
                    tile.serDeselegido()
                if button == 1:
                    self.pressed = True
                    self.elX,self.elY = x,y
                    if self.eleccion.size != (0,0):
                        self.eleccion.size=(0,0)
                elif button == 3:
                    if hasattr(self,'context'):
                        self.context.show()
                    
    def onMouseUp(self,button):
        x,y = self.getRelMousePos()
        tiles = []
        if button == 1:
            if hasattr(self,'tiles'):
                tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                for tile in tiles:
                    tile.onMouseUp(button)
            else:
                self.pressed = False
                self.SeleccionMultiple = False
                
            selected = 0
            for tile in self.tiles:
                if self.eleccion.contains(tile.rect):
                    tile.serElegido()
                    selected += 1
            if selected > 1:
                self.SeleccionMultiple = True
                    
            self.eleccion.size = 0,0
        
    def getRelMousePos(self,absx=None,absy=None):
        if absx is None and absy is None:
            abs_x,abs_y = mouse.get_pos()
        else:
            abs_x = absx
            abs_y = absy
        off_x,off_y = self.image.get_offset()
        dx = abs_x+off_x-self.x
        dy = abs_y+off_y-self.y
        
        if dx < 0: dx = 0
        if dy < 0: dy = 0
        
        if dx >= self.Tw: dx = self.Tw
        if dy >= self.Th: dy = self.Th
        
        return dx,dy

    def cambiar_layer(self,spr,mod):
        layer = spr.layer+mod
        self.tiles.change_layer(spr,layer)
    
    def update(self):
        x,y = self.elX,self.elY
        if self.pressed:
            nx,ny = self.getRelMousePos()
            dx = nx-x
            dy = ny-y
            if dx > 0:
                self.eleccion.x = x
            elif dx < 0:
                self.eleccion.left = x
            else:
                self.eleccion.w = 0
            self.eleccion.w = dx
                
            if dy > 0:
                self.eleccion.y = y
            elif dy < 0:
                self.eleccion.top = y
            else:
                self.eleccion.h = 0
            self.eleccion.h = dy
            self.eleccion.normalize()
            
