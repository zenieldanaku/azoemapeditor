from pygame import Surface,Rect,font,mouse
from libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from renderer import Renderer
from . import BaseWidget, BaseOpcion
from colores import color

class Menu (BaseWidget):
    cascada = None
    boton = None
    visible = 0
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
        # TODO:
        # hacer esto con recursion,
        # de manera que cierre cualquier
        # cantidad de cascadas abiertas.
        for opcion in self.cascada.opciones:
            if isinstance(opcion.command,_Cascada):
                if opcion.command.mostrar:
                    opcion.command.hideMenu()
        
        if self.cascada.mostrar:
            self.cascada.hideMenu()
    
class _Boton(BaseWidget):
    nombre = ''
    menu = None
    
    def __init__(self,parent,nombre,x,y, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        if 'colorTexto' not in opciones:
            opciones['colorTexto'] = 'sysMenText'
        if 'colorBgSel' not in opciones:
            opciones['colorBgSel'] = 'sysBoxSelBack'
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.Boton'
        self.img_des = self.crear_boton(nombre,color(opciones['colorTexto']),color(self.opciones['colorFondo']))
        self.img_sel = self.crear_boton(nombre,color(opciones['colorTexto']),color(self.opciones['colorBgSel']))
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.dirty = 1
        Renderer.addWidget(self,4)
    
    @staticmethod
    def crear_boton(nombre,fgcolor,bgcolor):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,fgcolor,bgcolor,1)
        return render
        
    def onMouseDown (self,dummy):
        self.parent.cascada.onFocusIn()
        self.parent.barra.soloUnMenu(self.parent)
 
    def onMouseIn(self):
        super().onMouseIn()
        self.image = self.img_sel
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des
        
class _Cascada (BaseWidget):
    opciones = None
    parent = None
    mostrar = False
    
    def __init__(self,parent,nombre,opciones,x,y,j=19):
        super().__init__()
        self.opciones = LayeredDirty()
        self.parent = parent
        self.nombre = parent.nombre+'.Cascada.'+nombre
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
            opcion = _Opcion(self,_nom,x,dy)
            w,h = opcion.image.get_size()
            if 'csc' in opciones[n]:
                opcion.command = _Cascada(self,_nom,opciones[n]['csc'],x+w,dy,h*(n+1))
            elif 'cmd' in opciones[n]:
                opcion.command = opciones[n]['cmd']
            alto += h+1
            if w > ancho: ancho = w
            self.opciones.add(opcion)

        self.rect = Rect(x,y+5,ancho,alto-8)

    def showMenu(self):
        self.mostrar = True
        for opcion in self.opciones:
            Renderer.addWidget(opcion,2)

    def hideMenu(self):
        self.mostrar = False
        for opcion in self.opciones:
            Renderer.delWidget(opcion)

    def onFocusIn(self):
        super().onFocusIn()
        self.showMenu()
    
    def onFocusOut(self):
        super().onFocusOut()
        recursion = True
        parent = self.parent
        while recursion:
            if hasattr(parent,'parent'):
                parent = parent.parent
            else:
                recursion = False
        parent.hideMenu()
    
    def onMouseIn(self):
        if self._visible:
            self.onFocusIn()

class _Opcion(BaseOpcion):
    command = None
    setFocus_onIn = True
    
    def __init__(self,parent,nombre,x,y):
        super().__init__(parent,nombre,x,y)

    def onMouseDown(self,button):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
        else:
            self.command()
            self.parent.onFocusOut()
            
    def onMouseIn(self):
        if self.enabled:
            super().onMouseIn()
            self.image = self.img_sel
    
    def onMouseOut(self):
        super().onMouseOut()
        self.image = self.img_des
    
    def onMouseOver(self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()