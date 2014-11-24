from globales import EventHandler, color, Sistema as Sys, Resources as r
from pygame import Surface,Rect,font,mouse,draw
from libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from . import BaseWidget

class Menu (BaseWidget):
    cascada = None
    boton = None
    visible = 0
    nombre = ''
    referencias = None
    def __init__(self,nombre,ops,x,y):
        self.fuente = font.Font(Sys.fdLibs+'\\fonts_tahoma.ttf',12)
        self.cascada = None
        self.boton = None
        super().__init__()
        self.referencias = {}
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
            w = 19+_fuente.size(opciones[n]['nom'])[0]+15
            if 'key' in opciones[n]:
                w += _fuente.size(opciones[n]['key'])[0]+15
            if 'csc' in opciones[n]:
                opciones[n]['scr'] = 'flecha'
                w += 80
            elif 'win' in opciones[n]:
                opciones[n]['scr'] = '...'
            else:
                opciones[n]['scr'] = None
            if w > self.w: self.w = w
        h = 19
        ajuste = 0
        self.h = h*len(opciones)+2
        
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            if _nom != 'barra':
                opcion = OpcionCascada(self,opciones[n],1,n*h+ajuste+1,self.w-22,h)
                _h = opcion.rect.bottom
                w = opcion.image.get_size()[0]
                if 'csc' in opciones[n]:
                    x = self.x+self.w-3
                    y = (n+1)*h+ajuste-1
                    opcion.command = _Cascada(self,_nom,opciones[n]['csc'],x,y)
                elif 'win' in opciones[n]:
                    opcion.command = opciones[n]['win']
                else:
                    opcion.command = opciones[n]['cmd']
                self.addToReferences(_nom,opcion)
            else:
                opcion = BaseWidget()
                opcion.image = self._linea_horizontal(self.w-1)
                opcion.rect = opcion.image.get_rect(topleft=(3,_h+4))
                ajuste -= 10  
            self.componentes.add(opcion)
        self.image = Surface((self.w+5,self.h+ajuste))
        self.image.fill(color('sysMenBack'),(1,1,self.w+3,self.h+ajuste-2))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        EventHandler.addWidget(self,self.layer)
    
    def addToReferences(self,key,item):
        recursion = True
        ancestro = self.parent
        while recursion:
            if hasattr(ancestro,'parent'):
                ancestro = ancestro.parent
            else:
                recursion = False
        if hasattr(ancestro,'referencias'):
            ancestro.referencias[key] = item
    
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
    
    def KeyCombination(self,key):
        for componente in self.componentes:
            if componente.KeyCombination == key:
                componente.execute_key_binding()
        
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
        icon = False
        rapido = False
        if 'icon' in data: icon = data['icon']
        if 'key' in data:  rapido = data['key']
        self.KeyCombination = rapido
        self.img_uns = self.crear(data,fuente,color('sysElmText'),color('sysMenBack'),w,h,icon,rapido)
        self.img_sel = self.crear(data,fuente,color('sysElmText'),color('sysBoxSelBack'),w,h,icon,rapido)
        self.img_des = self.crear(data,fuente,color('sysDisText'),color('sysMenBack'),w,h,icon,rapido)
        self.image = self.img_uns
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.dirty = 1
        
    @staticmethod
    def crear(data,fuente,fgcolor,bgcolor,w,h,icono,rapido):
        imagen = Surface((w+25,h))
        imagen.fill(bgcolor)
        if icono:
            imagen.blit(icono,(0,0))
        if rapido:
            abrv = fuente.render(rapido,True,fgcolor,bgcolor)
            
        nombre = data['nom']
        if data['scr'] == '...':
            nombre += data['scr']
        elif data['scr'] == 'flecha':
            flecha = Surface((9,9))
            flecha.fill(bgcolor)
            draw.polygon(flecha, fgcolor, [[1,1],[1,8],[6,4]])
            imagen.blit(flecha,(w+10,4))
        
        render = fuente.render(nombre,True,fgcolor,bgcolor)
        imagen.blit(render,(4+19,2))
        if rapido:
            imagen.blit(abrv,(85,2))
        return imagen
    
    def onMouseDown(self,button):
        if self.enabled:
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
        if self.enabled:
            self.serDeseleccionado()
    
    def serSeleccionado(self): 
        if self.enabled: self.image = self.img_sel
            
    def serDeseleccionado(self):
        if self.enabled: self.image = self.img_uns
    
    def serDeshabilitado(self):
        self.image = self.img_des
        self.enabled = False
        
    def serHabilitado(self):
        self.image = self.img_uns
        self.enabled = True
        
    def onMouseOver(self):
        if isinstance(self.command,_Cascada):
            self.command.showMenu()
            
    def execute_key_binding(self): self.command()

class ContextMenu(_Cascada):
    def __init__(self,parent,comandos = False):
        if not comandos:
            comandos = [{'nom':'Dummy','cmd':lambda:None}]
        super().__init__(parent,'ContextMenu',comandos,0,0)
        
    def show (self):
        x,y = mouse.get_pos()
        self.rect.topleft = x,y
        self.x,self.y = x,y
        self.showMenu()
    
    def onFocusOut(self):
        self.hasFocus = False
        self.hideMenu()