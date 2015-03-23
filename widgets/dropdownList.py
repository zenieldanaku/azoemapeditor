from . import BaseWidget, Entry, BaseOpcion
from pygame import Surface,draw, Rect,font, mouse
from pygame.sprite import LayeredDirty,DirtySprite
from libs.textrect import render_textrect
from globales import color, C, EventHandler

class DropDownList(BaseWidget):
    lista_de_opciones = None # LayeredDirty
    
    def __init__(self,parent,nombre,x,y,w,lista=[],**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.DropDownList.'+nombre
        self.layer = self.parent.layer +1
        self.lista = lista
        self.x,self.y = x,y
        self.w,self.h = w,21
        self.entry = Entry(self,nombre,self.x,self.y,w-18,**opciones)
        self.flecha = _Flecha(self,18)
        
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.lista_de_opciones = LayeredDirty(*self.crearLista(self.lista))
        
        self.ItemActual = ''
        EventHandler.addWidget(self.entry,layer=self.layer)
        EventHandler.addWidget(self.flecha,layer=self.layer)
        
        self.visible = 0
            
    def crearLista(self,opciones):
        lista = []
        
        h = 0
        for n in range(len(opciones)):   
            nom = opciones[n]
            dy = self.h+(n*h)-19
            opcion = _Opcion(self,nom,self.x+4,self.y+dy,self.w-23)
            opcion.layer = self.layer +50
            h = opcion.image.get_height()-1

            lista.append(opcion)
        if len(opciones) != 0:
            self.setText(opciones[0])
        return lista        
    
    def reubicar_en_ventana(self,dx=0,dy=0):
        self.entry.reubicar_en_ventana(dx,dy)
        self.flecha.reubicar_en_ventana(dx,dy)
    
    def setText(self,texto):
        self.entry.setText(texto)
        # acá podría stripearse el texto, si fuera onda Archivo de mapa (*.json)
        # extrayendo solo el .json
        self.ItemActual = texto
    
    def setItem(self,item):
        self.lista_de_opciones.empty()
        if item not in self.lista:
            self.lista.append(item)
        self.lista_de_opciones.add(*self.crearLista(self.lista))
        
        self.setText(item)
    
    def getItemActual(self): return self.ItemActual
    
    def getItem(self,item):
        for opcion in self.lista_de_opciones:
            if hasattr(item,'_nombre'):
                if opcion.texto == item._nombre:
                    return opcion
    
    def delItem(self,item):
        opcion = self.getItem(item)
        self.lista_de_opciones.empty()
        self.entry.borrar_todo()
        self.lista.remove(opcion.texto)
        
        self.lista_de_opciones.add(*self.crearLista(self.lista))
    
    def clear(self):
        self.lista.clear()
        self.entry.borrar_todo()
        
    def onDestruction(self):
        EventHandler.delWidget(self.entry)
        EventHandler.delWidget(self.flecha)
        self.hideItems()
        
    def showItems(self):
        for item in self.lista_de_opciones:
            EventHandler.addWidget(item,layer=self.layer+1)
    
    def hideItems(self):
        for item in self.lista_de_opciones:
            EventHandler.delWidget(item)
    
    def onFocusOut(self):
        super().onFocusOut()
        self.hideItems()
        
    def onKeyDown(self,key):
        entry = self.entry.devolver_texto()
        if self.ItemActual in self.lista:
            idx = self.lista.index(self.ItemActual)
            if entry != self.ItemActual:
                self.lista[idx] = entry
                self.lista_de_opciones.get_sprite(idx).setText(entry)
                self.ItemActual = self.lista[idx]
        
        self.parent.onKeyDown(key)
        
class _Flecha(BaseWidget):
    def __init__(self,parent,w,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = parent.nombre+'.flecha'
        self.w,self.h = w,self.parent.h
        self.x,self.y = self.parent.x+self.parent.w-self.w,self.parent.y
        cF,cB = color('sysScrArrow'),color('sysElmFace') # cFlecha,cBackground
        cL,cS = color('sysElmLight'),color('sysElmShadow') # cLuz,cSombra
        self.img_pre = self._biselar(self._crear(self.w,self.h,cF,cB),cS,cL)
        self.img_uns = self._biselar(self._crear(self.w,self.h,cF,cB),cL,cS)
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _crear(w,h,cFlecha,cFondo):
        imagen = Surface((w,h))
        imagen.fill(cFondo)
        points = [[4,7],[w//2-1,h-9],[w-6,7]]
        draw.polygon(imagen,cFlecha,points)
        return imagen
      
    def onMouseDown(self,dummy):
        self.image = self.img_pre
        self.parent.showItems()
    
    def onMouseUp(self,dummy):
        self.image = self.img_uns
        EventHandler.setFocus(self.parent)
    
    def onMouseOut(self):
        self.image = self.img_uns

class _Opcion(BaseOpcion):
    command = None
    
    def __init__(self,parent,nombre,x,y,w=0):
        super().__init__(parent,nombre,x,y,w)
        self.texto = nombre
    
    def setText(self,texto):
        super().setText(texto)
        self.texto = texto
    
    def devolverTexto(self):
        self.parent.setText(self.texto)
    
    def onMouseDown(self,button):
        self.devolverTexto()
        self.parent.onFocusOut()
        
    def onMouseIn(self):
        super().onMouseIn()
        self.image = self.img_sel
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des
        
    def update(self):
        self.dirty = 1