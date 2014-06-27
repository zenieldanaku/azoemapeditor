from pygame import Surface,Rect,font,mouse,draw
from libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from renderer import Renderer
from . import BaseWidget
from colores import color

class Menu (BaseWidget):
    cascada = None
    boton = None
    visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        self.fuente = font.SysFont('Tahoma',11)
        self.cascada = None
        self.boton = None
        super().__init__()
        self.boton = _Boton(self,nombre,x,y)
        h = self.boton.rect.h
        self.cascada = _Cascada(self,nombre,ops,x,h-1)
        
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
        self.img_des = self.crear_boton(nombre,parent.fuente,color(opciones['colorTexto']),color(self.opciones['colorFondo']))
        self.img_sel = self.crear_boton(nombre,parent.fuente,color(opciones['colorTexto']),color(self.opciones['colorBgSel']))
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.dirty = 1
        Renderer.addWidget(self,4)
    
    @staticmethod
    def crear_boton(nombre,fuente,fgcolor,bgcolor):
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w+15,h+1)
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
    
    def __init__(self,parent,nombre,opciones,x,y):
        super().__init__()
        self.opciones = LayeredDirty()
        self.parent = parent
        self.nombre = parent.nombre+'.Cascada.'+nombre
        self.layer+=2
        _fuente = font.SysFont('Tahoma',11)
        _w = 0
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            __w = _fuente.size(_nom)[0]
            if __w > _w:
                _w = __w
            if 'csc' in opciones[n]:
                opciones[n]['scr'] = 'flecha'
            elif 'win' in opciones[n]:
                opciones[n]['scr'] = '...'
            else:
                opciones[n]['scr'] = None
        h = 19
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            dy = y+(n*h)+5
            if _nom != 'barra':
                opcion = OpcionCascada(self,opciones[n],x,dy,_w,19)
                w = opcion.image.get_size()[0]
                if 'csc' in opciones[n]:
                    opcion.command = _Cascada(self,_nom,opciones[n]['csc'],x+w-3,h*(n+1)-5)
                elif 'win' in opciones[n]:
                    opcion.command = opciones[n]['win']
                else:
                    opcion.command = opciones[n]['cmd']
            
            self.opciones.add(opcion)
    
    def getRelMousePos(self):
        abs_x,abs_y = mouse.get_pos()
        dx = abs_x-self.x
        dy = abs_y-self.y
        
        return dx,dy
    def get_component(self):
        x,y = self.getRelMousePos()
        if self.componentes.get_sprites_at((x,y)) != []:
            return self.componentes.get_sprites_at((x,y))[-1]
        return self
    def onMouseDown(self,button):
        pass
    def onMouseUp(self,button):
        pass
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
        ancestro = self.parent
        while recursion:
            if hasattr(ancestro,'parent'):
                ancestro = ancestro.parent
            else:
                recursion = False
        ancestro.hideMenu()
    def onMouseIn(self):
        if self._visible:
            self.onFocusIn()
    def update(self):
        pass

class OpcionCascada(BaseWidget):
    command = None
    setFocus_onIn = True
    
    def __init__(self,parent,data,x,y,w,h,**opciones):
        super().__init__(**opciones)
        if 'Fuente' not in self.opciones:
            self.opciones['fontType'] = 'Tahoma'
        if 'fontSize' not in self.opciones:
            self.opciones['fontSize'] = 11
        fuente = font.SysFont(self.opciones['fontType'],self.opciones['fontSize'])
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.Opcion.'+data['nom']
        self.img_des = self.crear(data,fuente,color('sysElmText'),color('sysMenBack'),w,h)
        self.img_sel = self.crear(data,fuente,color('sysElmText'),color('sysBoxSelBack'),w,h)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.dirty = 1
        
    @staticmethod
    def crear(data,fuente,fgcolor,bgcolor,w,h):
        imagen = Surface((w+25,h))
        imagen.fill(bgcolor)
        
        nombre = data['nom']
        if data['scr'] == '...':
            nombre += data['scr']
        elif data['scr'] == 'flecha':
            flecha = Surface((9,9))
            flecha.fill(bgcolor)
            draw.polygon(flecha, fgcolor, [[1,1],[1,8],[6,4]])
            imagen.blit(flecha,(w+10,4))
        
        render = fuente.render(nombre,True,fgcolor,bgcolor)
        imagen.blit(render,(4,2))
        return imagen
    
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