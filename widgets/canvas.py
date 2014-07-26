from pygame import Surface, mouse, mask
from . import BaseWidget
from globales import C

class Canvas(BaseWidget):
    
    clip = None
    FONDO = None
    doc_w = None
    doc_h = None
    pressed = False
    shift = False
    def __init__(self,parent,x,y,w,h,clip,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = (255,255,245)
        if 'colorCuadro' not in opciones:
            opciones['colorCuadro'] = (191,191,191)
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.Canvas'
        self.layer = self.parent.layer+1
        self.x,self.y = x,y
        self.w,self.h = clip
        self.Tw,self.Th = w,h
        self.FONDO = Surface((w,h))
        self.doc_w,self.doc_h = w,h
        self.pintarFondoCuadriculado()
        self.image = self.FONDO.subsurface(0,0,self.w,self.h)
        self.image.set_clip((0,0,self.w,self.h))
        self.clip = self.image.get_clip()
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
    
    def pintarFondoCuadriculado(self):
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
        if button == 1 or button == 3:
            if not self.shift:
                for tile in self.tiles:
                    tile.selected = False
            tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                item = tiles[-1]
                mascara = mask.from_surface(item.image)
                if mascara.get_at((x-item.x,y-item.y)):
                    item.onMouseDown(button)
            else:
                self.pressed = True
    
    def onMouseUp(self,button):
        x,y = self.getRelMousePos()
        if button == 1:
            tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                for tile in tiles:
                    tile.onMouseUp(1)
            else:
                self.pressed = False
    
    def getRelMousePos(self):
        abs_x,abs_y = mouse.get_pos()
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