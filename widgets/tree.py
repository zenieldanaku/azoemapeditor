from pygame import font, Rect, Surface, draw
from . import Marco, BaseWidget, BaseOpcion
from libs.textrect import render_textrect
from globales import EventHandler, color
from pygame.sprite import LayeredDirty
from globales.constantes import *

class Tree (Marco):
    ItemActual = ''
    items = None
    layer = 4
    def __init__(self,parent,x,y,w,h,walk,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack' 
        super().__init__(x,y,w,h,False,**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.Tree'
        self.items = LayeredDirty()
        self.crearLista(walk)
        self.ItemActual = ''
    
    def scroll(self,dy):
        pass
    
    def crearLista(self,opciones):        
        h = 0
        for y in range(len(opciones)):
            x = opciones[y]['x']
            dx = self.x+(x*16)
            dy = self.y+(y*h)
            item = Item(self,dx,dy,opciones[y])
            h = item.h
            self.items.add(item)
            self.agregar(item)
        
        for i in range(len(self.items)):
            padre = self.items.get_sprite(i)
            for nomhijo in opciones[i]['hijos']:
                for j in range(len(self.items)):
                    hijo = self.items.get_sprite(j)
                    if hijo.nom_obj == nomhijo:
                        padre.hijos.add(hijo)
    
    def mover(self,item,dy):
        sprites = self.items.sprites()
        for idx in range(len(sprites)):
            if sprites[idx].nombre == item.nombre:
                idx += 1
                break
        dh = 0
        for hijo in item.hijos:
            dh += hijo.h
            idx += 1
        
        for i in range(idx,len(self.items)):
            widget = self.items.get_sprite(i)
            widget.mover(dh*dy)
    
    def onMouseDown(self,button):
        if self.ScrollY.enabled:
            if button == 5:
                self.ScrollY.moverCursor(dy=+10)
            if button == 4:
                self.ScrollY.moverCursor(dy=-10)

class Item (BaseWidget):
    hijos = None
    def __init__(self,parent,x,y,keyargs,**opciones):
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.Item.'+keyargs['obj']
        self.layer  = self.parent.layer +1
        self.nom_obj = keyargs['obj']
        self.hijos = LayeredDirty()
        self.visible = 0 # no es que sea invisible, es que no tiene imagen
        self.opcion = _Opcion(self,self.nom_obj,keyargs['path'],x+16+3,y)
        h = self.opcion.image.get_height()
        self.cursor = _Cursor(self,self.nom_obj,x,y,16,h-2,keyargs['empty'])
        w = self.cursor.rect.w+3+self.opcion.rect.w
        self.rect = Rect(x,y,w,h)
        self.w,self.h = self.rect.size
        EventHandler.addWidget(self.opcion,self.layer+1)
        EventHandler.addWidget(self.cursor,self.layer+1)      
                
    def onDestruction(self):
        EventHandler.delWidget(self.opcion)
        EventHandler.delWidget(self.cursor)
    
    def colapsarHijos(self):
        for hijo in self.hijos:
            hijo.AutoColapsar()
            hijo.colapsarHijos()

    def mostrarHijos(self):
        for hijo in self.hijos:
            hijo.AutoMostrar()
            if hijo.cursor.open:
                hijo.mostrarHijos()
            
    def AutoColapsar(self):
        for obj in [self.opcion,self.cursor]:
            obj.visible = False
            obj.enabled = False
        self.enabled = False

    def AutoMostrar(self):
        for obj in [self.opcion,self.cursor]:
            obj.visible = True
            obj.enabled = True
        self.enabled = True
    
    def mover(self,dy):
        for obj in [self,self.opcion,self.cursor]:
            obj.y += dy
            obj.rect.y += dy
    
class _Opcion(BaseOpcion):
    path = ''
    
    def __init__(self,parent,nombre,path,x,y,w=0):
        super().__init__(parent,nombre,x,y,w)
        self.texto = nombre
        self.path = path
    
    def onMouseDown(self,button):
        if button == 1:
            self.parent.parent.ItemActual = self.path
    
    def onFocusIn(self):
        super().onFocusIn()
        self.image = self.img_sel
    
    def onFocusOut(self):
        super().onFocusOut()
        self.image = self.img_des

class _Cursor(BaseWidget):
    def __init__(self,parent,nombre,x,y,w,h,vacio,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.Cursor.'+nombre
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.open = True
        self.vacio = vacio
        self.img_cld = self._crear(False)
        self.img_opn = self._crear(True)
        self.setStatus()
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    
    def _crear(self,closed):
        imagen = Surface((self.w,self.h))
        imagen.fill(color('sysMenBack'))
        rect = imagen.get_rect()
        if closed:
            draw.line(imagen,(0,0,0),(5,rect.h//2),(rect.w-4,rect.h//2),2)
        else:
            draw.line(imagen,(0,0,0),(5,rect.h//2),(rect.w-4,rect.h//2),2)
            draw.line(imagen,(0,0,0),(8,4),(8,rect.h-4),2)
        draw.rect(imagen,(0,0,0),(2,2,rect.w-2,rect.h-2),1)
        return imagen
    
    def onMouseDown(self,button):
        if button == 1:
            if not self.vacio:
                self.open = not self.open
            
            if self.open:
                self.parent.mostrarHijos()
                dy = +1
            else:
                self.parent.colapsarHijos()
                dy = -1
            
            self.parent.parent.mover(self.parent,dy)
    
    def setStatus(self):
        if self.open:
            self.image = self.img_opn
        else:
            self.image = self.img_cld
        
    def update(self):
        self.setStatus()
        self.dirty = 1

