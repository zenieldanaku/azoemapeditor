from pygame.sprite import LayeredDirty, DirtySprite
from globales import GLOBALES as G
from pygame import Surface, mouse
from . import BaseWidget
from constantes import * 

class Canvas(BaseWidget):
    capas = None
    guias = None
    tiles = None
    clip = None
    FONDO = None
    pressed = False
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
        self.pintarFondoCuadriculado()
        self.image = self.FONDO.subsurface(0,0,self.w,self.h)
        self.image.set_clip((0,0,self.w,self.h))
        self.clip = self.image.get_clip()
        self.rect = self.FONDO.get_rect(topleft=(self.x,self.y))
        self.capas = LayeredDirty()
        self.tiles = LayeredDirty()
        self.guias = LayeredDirty()
    
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
        if button == 1:
            if self.tiles.get_sprites_at((x,y)) != []:
                item = self.tiles.get_sprites_at((x,y))[0]
                item.onMouseDown(1)
            else:
                self.pressed = True
                
        elif self.ScrollY.enabled:
            if button == 5:
                self.ScrollY.moverCursor(dy=+10)
            if button == 4:
                self.ScrollY.moverCursor(dy=-10)
    
    def onMouseUp(self,button):
        x,y = self.getRelMousePos()
        if button == 1:
            if self.tiles.get_sprites_at((x,y)) != []:
                item = self.tiles.get_sprites_at((x,y))[-1]
                item.onMouseUp(1)
    
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
    
    def scroll(self,dx=0,dy=0):
        self.clip.x += dx
        self.clip.y += dy
        try:
            self.image.set_clip(self.clip)
            self.image = self.FONDO.subsurface(self.clip)
        except:
            self.clip.x -= dx
            self.clip.y -= dy
            self.image.set_clip(self.clip)
        self.ReglaX.scroll(dx)
        self.ReglaY.scroll(dy)
        self.Grilla.scroll(dx,dy)
    
    def pegar(self,elemento):
        x,y = self.getRelMousePos()
        img = elemento.image
        tile = SimboloCNVS(self,img,x-8,y-8)
        self.tiles.add(tile)

    def update(self):
        if not G.HabilitarTodo:
            self.guias.empty()
            self.capas.empty()
            self.tiles.empty()
            
        if len(G.IMGs_cargadas) <= 0:
            self.capas.empty()
            self.pintarFondoCuadriculado()

        else:
            for idx in G.IMGs_cargadas:
                spr = G.IMGs_cargadas[idx]
                if spr not in self.capas:
                    self.capas.add(spr)
            self.capas.draw(self.FONDO)
        
        self.tiles.update()
        self.tiles.draw(self.FONDO)
        self.guias.draw(self.FONDO)
        self.dirty = 1

class SimboloCNVS (BaseWidget):
    pressed = False
    def __init__(self,parent,imagen,x,y,**opciones):
        super().__init__(**opciones)
        self.image = imagen
        self.x,self.y = x,y
        self.w,self.h = self.image.get_size()
        self.parent = parent
        self.nombre = self.parent.nombre+'.Simbolo.'+'ejemplo'
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
    
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
    
    def update(self):
        if self.pressed:
            x,y = self.parent.getRelMousePos()
            self.x,self.y = x-self.w//2,y-self.h//2
            self.rect.topleft = x-self.w//2,y-self.h//2
        self.dirty = 1