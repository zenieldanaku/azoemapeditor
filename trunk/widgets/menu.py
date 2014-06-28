from pygame import Surface,Rect,font,mouse,draw
from libs.textrect import render_textrect
from globales import EventHandler, color
from pygame.sprite import LayeredDirty
from . import BaseWidget
from os import getcwd

class Menu (BaseWidget):
    cascada = None
    boton = None
    visible = 0
    nombre = ''
    def __init__(self,nombre,ops,x,y):
        self.fuente = font.Font(getcwd()+'/rundata/menus/fonts_tahoma.ttf',12)
        self.cascada = None
        self.boton = None
        super().__init__()
        self.boton = _Boton(self,nombre,x,y)
        h = self.boton.rect.h
        self.cascada = _Cascada(self,nombre,ops,x,h+1)
        
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
        EventHandler.addWidget(self,4)
    
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
        self.visible = False
        self.componentes = LayeredDirty()
        self.parent = parent
        self.nombre = parent.nombre+'.Cascada.'+nombre
        self.layer = self.parent.layer +20
        self.x,self.y = x,y
        _fuente = font.SysFont('Tahoma',11)
        self.w = 0
        for n in range(len(opciones)):
            w = _fuente.size(opciones[n]['nom'])[0]
            if w > self.w: self.w = w
            if 'csc' in opciones[n]:
                opciones[n]['scr'] = 'flecha'
            elif 'win' in opciones[n]:
                opciones[n]['scr'] = '...'
            else:
                opciones[n]['scr'] = None
        h = 19
        ajuste = 0
        self.h = h*len(opciones)+2
        self.w += 20
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            if _nom != 'barra':
                opcion = OpcionCascada(self,opciones[n],1,n*h+ajuste+1,self.w-22,h)
                w = opcion.image.get_size()[0]
                if 'csc' in opciones[n]:
                    x = self.x+self.w-3
                    y = (n+1)*h+ajuste-1
                    opcion.command = _Cascada(self,_nom,opciones[n]['csc'],x,y)
                elif 'win' in opciones[n]:
                    opcion.command = opciones[n]['win']
                else:
                    opcion.command = opciones[n]['cmd']
            else:
                opcion = BaseWidget()
                opcion.image = self._linea_horizontal(self.w-1)
                opcion.rect = opcion.image.get_rect(topleft=(3,n*h+5))
                ajuste += -10
            
            self.componentes.add(opcion)
        self.image = Surface((self.w+5,self.h+ajuste))
        self.image.fill((255,255,255),(1,1,self.w+3,self.h+ajuste-2))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        EventHandler.addWidget(self,self.layer)
    
    @staticmethod
    def _linea_horizontal(w):
        line = Surface((w,2))
        draw.line(line,(100,100,100),[0,0],[w,0])
        draw.line(line,(200,200,200),[0,1],[w,1])
        return line
    
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
        item = self.get_component()
        if item != self:
            item.onMouseDown(button)
        if not self.parent._visible:
            self._visible = False
        
    def onMouseUp(self,button):
        item = self.get_component()
        if item != self:
            item.onMouseUp(button)
    
    def showMenu(self):
        self.mostrar = True
        self._visible = True
            
    def hideMenu(self):
        self.mostrar = False
        for componente in self.componentes:
            if isinstance(componente,OpcionCascada):
                componente.serDeseleccionado()
                if isinstance(componente.command,_Cascada):
                    componente.command.hideMenu()
        self._visible = False
    
    def onMouseOver(self):
        if self.mostrar:
            for item in self.componentes:
                item.onMouseOut()
            item = self.get_component()
            if item != self:
                item.onMouseIn()
    
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
        
    def update(self):
        self.componentes.update()
        self.componentes.draw(self.image)
        self.dirty = 1

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
        self.nombre = self.parent.nombre+'.OpcionCascada.'+data['nom']
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
            self.serSeleccionado()
    
    def onMouseOut(self):
        super().onMouseOut()
        self.serDeseleccionado()
    
    def serSeleccionado(self):
        self.image = self.img_sel
    
    def serDeseleccionado(self):
        self.image = self.img_des
    
    def onMouseOver(self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
