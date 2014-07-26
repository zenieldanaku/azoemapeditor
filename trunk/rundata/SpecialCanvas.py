from pygame import K_UP,K_DOWN,K_RIGHT,K_LEFT, \
                   K_DELETE,K_RSHIFT,K_LSHIFT, \
                   transform
from pygame.sprite import LayeredDirty
from globales import Sistema as Sys, C
from .simbolos import SimboloCNVS
from widgets import Canvas

class SpecialCanvas (Canvas):
    capas = None
    guias = None
    tiles = None
    
    def __init__(self,parent,x,y,w,h,clip,**opciones):
        super().__init__(parent,x,y,w,h,clip,**opciones)
        self.capas = LayeredDirty()
        self.guias = LayeredDirty()
        self.tiles = LayeredDirty()
        
    def onMouseDown(self,button):
        if button == 1 or button == 3:
            super().onMouseDown(button)

        elif self.ScrollY.enabled:
            if button == 5:
                self.ScrollY.moverCursor(dy=+10)
            if button == 4:
                self.ScrollY.moverCursor(dy=-10)
    
    def onKeyDown(self,event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = True
        for tile in self.tiles:
            if tile.selected:
                if tile.onKeyDown(event.key,self.shift): #delete
                    index = tile.index
                    self.tiles.remove(tile)
                    del Sys.PROYECTO.script[tile.grupo][tile._nombre][index]
                    for tile in self.tiles:
                        if tile.index > index:
                            tile.index -= 1
    
    def onKeyUp(self,event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = False
            
        for tile in self.tiles:
            if tile.selected:
                tile.onKeyUp(event.key)
                
    def actualizar_tamanio_fondo (self,w,h):
        self.FONDO = transform.scale(self.FONDO,(w,h))
        self.image = self.FONDO.subsurface(self.clip)
        self.ReglaX.actualizar_tamanio(w)
        self.ReglaY.actualizar_tamanio(h)
        self.Grilla.actualizar_tamanio(w,h)
        self.doc_w,self.doc_h = w,h
        self.Th,self.Tw = w,h
        
    def pegar(self,datos):
        rect = datos['rect']
        rect.center=self.getRelMousePos()
        datos['pos'] = rect.topleft    
        datos['index'] = Sys.addItem(datos['nombre'],datos['ruta'],datos['grupo'])
        self.addTile(datos)
    
    def addTile(self,datos):
        tile = SimboloCNVS(self,datos)
        self.tiles.add(tile)
        
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
        
    def update(self):
        if not Sys.HabilitarTodo:
            self.guias.empty()
            self.capas.empty()
            self.tiles.empty()
            self.clip.topleft = 0,0
            self.actualizar_tamanio_fondo(15*C+1,15*C+1)
            
        if len(Sys.IMGs_cargadas) <= 0:
            self.capas.empty()
            self.pintarFondoCuadriculado()

        else:
            for idx in Sys.IMGs_cargadas:
                spr = Sys.IMGs_cargadas[idx]
                if self.FONDO.get_size() != spr.rect.size:
                    self.actualizar_tamanio_fondo(*spr.rect.size)
                if spr not in self.capas:
                    self.capas.add(spr)
            self.capas.draw(self.FONDO)
        
        self.tiles.update()
        self.tiles.draw(self.FONDO)
        self.guias.draw(self.FONDO)
        for tile in self.tiles:
            Sys.updateItemPos(tile._nombre,tile.grupo,tile.index,tile.rect.topleft)
        self.dirty = 1