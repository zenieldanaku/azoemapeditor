from pygame import K_UP,K_DOWN,K_RIGHT,K_LEFT, \
                   K_DELETE,K_RSHIFT,K_LSHIFT, \
                   transform, Surface,draw,mouse,Rect
from pygame.sprite import LayeredDirty, DirtySprite
from globales import Sistema as Sys, C, LAYER_FONDO,LAYER_COLISIONES
from .simbolos import SimboloCNVS
from widgets import Canvas, ContextMenu

class SpecialCanvas (Canvas):
    capas = None
    guias = None
    tiles = None
    
    def __init__(self,parent,x,y,w,h,clip,**opciones):
        super().__init__(parent,x,y,w,h,clip,**opciones)
        self.capas = LayeredDirty()
        self.guias = LayeredDirty()
        self.tiles = LayeredDirty()
        comandos = [
            {'nom':'Pegar','cmd':lambda:Sys.pegar(),'icon':Sys.iconos['pegar']},
        ]
        self.context = ContextMenu(self,comandos)
    
    def onMouseOver (self):
        over = self.detect()
        
        for item in over:
            if item in self.tiles:#is tile
                if item.isMoving:
                    if self.SeleccionMultiple:
                        self.mover_tiles(item.dx,item.dy)
            elif item in self.guias: #is guide
                print(item)
    
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
                    Sys.selected = None
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
    
    @staticmethod
    def _imagen_colisiones (w,h):
        spr = DirtySprite()
        spr.image = Surface((w,h))
        spr.rect = spr.image.get_rect()
        spr.dirty = 2
        return spr
    
    def pegar(self,item):
        if type(item) == dict:              # copy
            self.colocar_tile(item)
        else:                               # cut
            pos = mouse.get_pos()           
            x,y = self.getRelMousePos()
            if self.rect.collidepoint(pos): # Ctrl+V o menu contextual
                item.rect.center = x,y
            else:                           # Boton "pegar" en panel
                item.rect.center = self.rect.center
            
            item.x,item.y = item.rect.topleft
            self.tiles.add(item)
    
    def colocar_tile(self,datos):
        pos = mouse.get_pos()
        rect = datos['rect']
        if self.rect.collidepoint(pos):
            rect.center = self.getRelMousePos(*rect.center)
        else:
            rect.center = self.rect.center
        z = datos['pos'][2]
        datos['pos'] = rect.x,rect.y,z
        datos['index'] = Sys.addItem(datos['nombre'],datos['ruta'],datos['grupo'],datos['colisiones'])
        self.addTile(datos)
        self.update()
    
    def addTile(self,datos):
        #print(datos)
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
    
    def render(self):
        base = self.capas.get_sprites_from_layer(LAYER_COLISIONES)[0].image
        for tile in self.tiles:
            base.blit(tile.img_cls,tile.rect)
        return base
    
    def mover_tiles(self,dx,dy):
        
        cadena = []
        for tile in self.tiles:
            if not tile.isMoving:#el que estamos moviendo manualmente
                if tile.selected:
                    cadena.insert(tile.index,tile.tipo+' '+tile._nombre+' #'+str(tile.index)+' @ ('+str(tile.rect.x)+','+str(tile.rect.y)+','+str(tile.layer)+')')
                    tile.mover(dx,dy)#el resto de los que estan seleccionados
            else:
                cadena.insert(tile.index,tile.tipo+' '+tile._nombre+' #'+str(tile.index)+' @ ('+str(tile.rect.x)+','+str(tile.rect.y)+','+str(tile.layer)+')')
            Sys.estado = ', '.join(cadena)
    
    def habilitar(self,control):
        if not control:
            self.guias.empty()
            self.capas.empty()
            self.tiles.empty()
            self.clip.topleft = 0,0
            self.actualizar_tamanio_fondo(15*C,15*C)
        
    def update(self):
        super().update()
            
        if Sys.IMG_FONDO == None:
            self.capas.empty()
            self.pintarFondoCuadriculado()

        else:
            spr = Sys.IMG_FONDO
            if self.FONDO.get_size() != spr.rect.size:
                self.actualizar_tamanio_fondo(*spr.rect.size)
                img = self._imagen_colisiones(*spr.rect.size)
                
            if spr not in self.capas:
                self.capas.add(spr,layer = LAYER_FONDO)
                self.capas.add(img,layer = LAYER_COLISIONES)
            self.capas.draw(self.FONDO)
        
        self.tiles.update()
        self.guias.update()
        self.tiles.draw(self.FONDO)
        self.guias.draw(self.FONDO)
        if self.eleccion.size != (0,0):
            draw.rect(self.FONDO,(0,255,255),self.eleccion,1)
        for tile in self.tiles:
            Sys.updateItemPos(tile._nombre,tile.grupo,tile.index,tile.rect.topleft,tile.layer,tile.rot)
        self.dirty = 1