from pygame import Surface, mouse, K_UP,K_DOWN,K_RIGHT,K_LEFT,mask,transform
from pygame.sprite import LayeredDirty, DirtySprite
from . import BaseWidget, SimboloBase
from globales import Sistema as Sys
from globales.constantes import *

class Canvas(BaseWidget):
    capas = None
    guias = None
    tiles = None
    clip = None
    FONDO = None
    doc_w = None
    doc_h = None
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
        self.doc_w,self.doc_h = w,h
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
            for tile in self.tiles:
                tile.selected = False
            tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                item = tiles[-1]
                mascara = mask.from_surface(item.image)
                if mascara.get_at((x-item.x,y-item.y)):
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
            tiles = self.tiles.get_sprites_at((x,y))
            if tiles != []:
                for tile in tiles:
                    tile.onMouseUp(1)
            else:
                self.pressed = False
            
    def onKeyDown(self,event):
        for tile in self.tiles:
            if tile.selected:
                tile.onKeyDown(event.key)
    
    def onKeyUp(self,event):
        for tile in self.tiles:
            if tile.selected:
                tile.onKeyUp(event.key)
            
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
    
    def pegar(self,datos):
        rect = datos['rect']
        rect.center=self.getRelMousePos()
        datos['pos'] = rect.topleft
        if datos['tipo'] == 'Prop':
            root = Sys.MAPA.script['capa_ground']['props']
            if datos['nombre'] not in root:
                root[datos['nombre']] = [[]]
                index = 0
            else:
                root[datos['nombre']].append([])
                index = len(root[datos['nombre']])-1
        datos['index'] = index
        tile = SimboloCNVS(self,datos)
        self.tiles.add(tile)
    
    def actualizar_tamanio_fondo (self,w,h):
        self.FONDO = transform.scale(self.FONDO,(w,h))
        self.image = self.FONDO.subsurface(self.clip)
        self.ReglaX.actualizar_tamanio(w)
        self.ReglaY.actualizar_tamanio(h)
        self.Grilla.actualizar_tamanio(w,h)
        self.doc_w,self.doc_h = w,h
        self.Th,self.Tw = w,h
        
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
        self.dirty = 1

class SimboloCNVS (SimboloBase):
    selected = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        
        self.tipo = self.data['tipo']
        self.index = self.data['index']
        self.ruta = self.data['ruta']

        self.img_uns = self._imagen.copy()
        self.img_sel = self.crear_img_sel(self.img_uns)
        self.image = self.img_uns

    @staticmethod
    def crear_img_sel(imagebase):
        over = imagebase.copy()
        over.fill((0,0,100), special_flags=1)
        return over
    
    def onMouseDown(self,button):
        if button == 1:
            self.onFocusIn()
            self.image = self.img_sel
            self.selected = not self.selected
            super().onMouseDown(button)

    def onKeyDown(self,tecla):
        if self.selected:
            dx,dy = 0,0
            if tecla == K_RIGHT:
                dx = +1
            elif tecla == K_LEFT:
                dx = -1
            elif tecla == K_DOWN:
                dy = +1
            elif tecla == K_UP:
                dy = -1
            self.dx,self.dy = dx,dy
            self.mover(self.dx,self.dy)
    
    def onKeyUp(self,tecla):
        if tecla == K_RIGHT or tecla == K_LEFT:
            self.dx = 0
        elif tecla == K_DOWN or tecla == K_UP:
            self.dy = 0
    
    def mover(self,dx,dy):
        super().mover(dx,dy)
        Sys.estado = self.tipo+' '+self._nombre+' '+str(self.index)+' @ '+str(self.rect.topleft)
    
    def update(self):
        if self.selected:
            self.image = self.img_sel
            if self.pressed:
                dx,dy = self._arrastrar()
                self.mover(dx,dy)
        
            #esto no le correponde al simbolo en sí.          
            if self.tipo == "Prop":
                #Sys.addProp(self._nombre,self.index,self.rect.topleft)
                root = Sys.MAPA.script['capa_ground']['props']
                root[self._nombre][self.index] = self.rect.topleft
            Sys.addRef(self._nombre,self.ruta)
            
        else:
            self.image = self.img_uns
        
        self.dirty = 1