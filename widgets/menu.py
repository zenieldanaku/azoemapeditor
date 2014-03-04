from pygame import Surface,Rect,font,mouse
from libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from renderer import Renderer
from . import BaseWidget
from constantes import *

class Menu (BaseWidget):
    cascada = None
    _visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        super().__init__()
        self.boton = _Boton(self,nombre,x,y)
        Renderer.addWidget(self.boton,4)
        h = self.boton.rect.h
        self.cascada = _Cascada(ops,x,h,h)
    
    def showMenu(self):
        self.cascada.showMenu()

    def hideMenu(self):
        self.cascada.hideMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        self.hideMenu()

class _Boton(BaseWidget):
    nombre = ''
    menu = None
    
    def __init__(self,menu,nombre,x,y):
        super().__init__()
        self.nombre = nombre
        self.menu = menu
        self.layer = 2
        self.img_des = self.crear_boton(self.nombre,negro)
        self.img_sel = self.crear_boton(self.nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.dirty = 1
    
    def crear_boton(self,nombre,color):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,color,gris,1)
        return render
        
    def onMouseDown (self,button):
        if button == 1:
            self.menu.barra.onFocusIn(self.menu)
            
    def onFocusOut(self):
        self.menu.onFocusOut()
        super().onFocusOut()
   
    def onMouseOver(self):
        self.image = self.img_sel
    
    def onMouseOut(self):
        self.image = self.img_des
    
    def update(self):
        self.dirty = 1

class _Cascada (BaseWidget):
    opciones = None
    
    def __init__(self,opciones,x,y,h,j=0):
        super().__init__()
        self.opciones = LayeredDirty()
        alto,ancho, = 0,0
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            dy = (n+1)*h+5+j
            if 'cmd' in opciones[n]:
                opt = opciones[n]['cmd']
            else:
                opt = None
            opcion = _Opcion(_nom,[x,dy],opt,self)
            w,h = opcion.image.get_size()
            if 'csc' in opciones[n]:
                opcion.command = _Cascada(opciones[n]['csc'],x+w+1,dy,dy-5,h)
            alto += h+1
            if w > ancho: ancho = w
            self.opciones.add(opcion)

        image = Surface((ancho,alto-7))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y+5))
        self._visible = 0
        Renderer.addWidget(self,3)
        for op in self.opciones:
            Renderer.addWidget(op,3)
        self.dirty = 2
    
    def showMenu(self):
        self._visible = 1
        for opcion in self.opciones:
            opcion._visible = True
            opcion.enabled = True
            opcion.focusable = True
    
    def hideMenu(self):
        self._visible = 0
        for opcion in self.opciones:
            opcion._visible = False
            opcion.enabled = False
            opcion.focusable = False

class _Opcion(BaseWidget):
    nombre = ''
    
    def __init__(self,nombre,pos,cmd,menu):
        super().__init__()
        self.nombre = nombre
        self.visible = False
        self.enabled = False
        self.focusable = False
        self.command = cmd
        self.menu = menu
        self.img_des = self.crear(self.nombre,negro)
        self.img_sel = self.crear(self.nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
    
    def crear(self,nombre,color):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,color,gris,1)
        return render
    
    def onMouseOver(self):
        if self.enabled:
            self.image = self.img_sel
            if isinstance(self.command,_Cascada):
                self.command.showMenu()
    
    def onMouseOut(self):
        self.image = self.img_des
    
    def onMouseDown(self,button):
        self.comando()
        self.menu.hideMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        self.enabled=False
    
    def onFocusIn(self):
        super().onFocusIn()
        self.comando()
        self.menu.hideMenu()
    
    def comando (self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
        else:
            self.command()