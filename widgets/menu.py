from pygame import Surface,Rect,font,mouse
from libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from renderer import Renderer
from . import BaseWidget
from colores import *
from colores import color

class Menu (BaseWidget):
    cascada = None
    boton = None
    _visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        self.cascada = None
        self.boton = None
        super().__init__()
        self.boton = _Boton(self,nombre,x,y)
        h = self.boton.rect.h
        self.cascada = _Cascada(self,nombre,ops,x,h,h)
        
    def showMenu(self):
        self.cascada.showMenu()

    def hideMenu(self):
        self.cascada.hideMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        self.cascada.hideMenu()

class _Boton(BaseWidget):
    nombre = ''
    menu = None
    
    def __init__(self,parent,nombre,x,y, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        if 'colorTexto' not in opciones:
            opciones['colorTexto'] = 'sysMenText'
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.Boton'

        self._layer = 2
        self.img_des = self.crear_boton(nombre,color(opciones['colorTexto']))
        self.img_sel = self.crear_boton(nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.dirty = 1
        Renderer.addWidget(self,4)
    
    def crear_boton(self,nombre,colorTexto):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,colorTexto,color(self.opciones['colorFondo']),1)
        return render
        
    def onMouseDown (self,button):
        if button == 1:
            self.parent.barra.onFocusIn(self.parent)
            
    def onFocusOut(self):
        #self.menu.onFocusOut()
        super().onFocusOut()
   
    def onMouseIn(self):
        super().onMouseIn()
        self.image = self.img_sel
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des
        
class _Cascada (BaseWidget):
    opciones = None
    parent = None
    
    def __init__(self,parent,nombre,opciones,x,y,j=19):
        super().__init__()
        self.opciones = LayeredDirty()
        self.parent = parent
        self.nombre = parent.nombre+'.'+nombre
        # Determinar el ancho de la opcion con mas caracteres
        l = [opciones[n]['nom'] for n in range(len(opciones))]
        w_max = len(max(l,key=lambda n:len(n)))
        # Agregar una cantidad de espacios igual a la diferencia mediante format
        # mocho, porque limita la fuente de la opcion a una de fixed width
        # pero funciona
        for n in range(len(opciones)):
            if '{}' not in opciones[n]['nom']:
                opciones[n]['nom'] += '{}'
            opciones[n]['nom']= opciones[n]['nom'].format(' '*int(w_max-len(l[n])))            
        
        alto,ancho,h = 0,0,0
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            dy = j+(n*h)+5
            opcion = _Opcion(self,_nom,[x,dy])
            w,h = opcion.image.get_size()
            if 'csc' in opciones[n]:
                opcion.command = _Cascada(self,_nom,opciones[n]['csc'],x+w+1,dy,h*(n+1))
            elif 'cmd' in opciones[n]:
                opcion.command = opciones[n]['cmd']
            alto += h+1
            if w > ancho: ancho = w
            self.opciones.add(opcion)

        image = Surface((ancho,alto-8))
        image.fill(negro)
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
    
    def onFocusIn(self):
        super().onFocusIn()
        self.showMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        recursion = True
        parent = self.parent
        while recursion:
            if hasattr(parent,'parent'):
                parent.hideMenu()
                parent = parent.parent
            else:
                recursion = False
        self.hideMenu()
    
    def onMouseIn(self):
        if self._visible:
            self.onFocusIn()

class _Opcion(BaseWidget):
    command = None
    
    def __init__(self,parent,nombre,pos):
        super().__init__()
        self.parent = parent
        self.nombre = self.parent.nombre+'.Opcion'+nombre
        self.visible = False
        self.enabled = False
        self.img_des = self.crear(nombre,negro)
        self.img_sel = self.crear(nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
    
    def crear(self,nombre,fgcolor):
        fuente = font.SysFont('Courier new',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,fgcolor,color('sysMenBack'),1)
        return render
            
    def onMouseDown(self,button):
        self.comando()
        self.parent.onFocusOut()
    
    #def onFocusIn(self):
    #    super().onFocusIn()
        
    def onFocusOut(self):
        super().onFocusOut()
        self.enabled=False
        self.parent.hideMenu()
        
    #def onMouseIn(self):
    #    super().onMouseIn()
    #    if self.enabled:
    #        self.image = self.img_sel
    #        if isinstance(self.command,_Cascada):
    #            self.command.showMenu()
                
    def onMouseIn(self):
        if self.enabled:
            super().onMouseIn()
            self.image = self.img_sel
            self.onFocusIn()
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des
    
    def onMouseOver(self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
    
    def comando (self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
        else:
            self.command()