from globales import Sistema as Sys, Resources as r, EventHandler, C, color
from widgets import Marco, BaseWidget, FileDiag, SimboloBase
from widgets import Boton, DropDownList, Entry, ContextMenu
from .menus.menu_mapa import CuadroMapa
from pygame import Rect,Surface,draw,mouse
from pygame.sprite import LayeredDirty
from os import path

class PanelSimbolos(Marco):
    simbolos = None
    botones = []
    def __init__(self,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = color('sysElmFace')

        super().__init__(16*C,19,4*C+8,16*C-1,**opciones)
        self.nombre = 'PanelSimbolos'
        self.simbolos = LayeredDirty()
        self.Items = DropDownList(self,'Items',self.x+3,self.y+3*C,self.w-6)
        self.PrevArea = area_prev(self,self.x+3,self.y+4*C-8,self.w-6,4*C)
        n,s,t,c,d = 'nom','scr','tipo','cmd','des'
        elementos = [
            {n:'Nuevo',c:lambda:CuadroMapa('Nuevo Mapa'),s:"N",d:"Crear un mapa nuevo"},
            {n:'Abrir',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.abrirProyecto},Sys.fdProyectos),s:"A",d:"Abrir un mapa existente"},
            {n:'Guardar',c:self.Guardar,s:"G",d:"Guardar el mapa actual"},
            {n:'barra'},
            {n:'Cortar',c:self.Cortar,s:"X",d:"Cortar"},
            {n:'Copiar',c:self.Copiar,s:"C",d:"Copiar"},
            {n:'Pegar',c:self.Pegar,s:"P",d:"Pegar"},
            {n:'barra'},
            {n:'SetFondo',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.setRutaFondo},Sys.fdAssets),s:"Fd",d:"Cargar imagen de fondo"},
            {n:'SetColis',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.setRutaColis},Sys.fdAssets),s:"Cl",d:"Cargar imagen de colisiones"},
            {n:'addMob',c:lambda:FileDiag({s:'Aceptar',t:'A',c:self.addMob},Sys.fdAssets),s:"Mb",d:"Cargar símbolo de mob (no funciona)"},
            {n:'addProp',c:lambda:FileDiag({s:'Aceptar',t:'A',c:self.addProp},Sys.fdAssets),s:"Pr",d:"Cargar símbolo de prop"},
            ]
        x = self.x+4
        y = 19+4
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+5,y,e['nom'],e['cmd'],e['scr'],descripcion = e['des'])
                x = boton.rect.right-2
                self.botones.append(boton)
                EventHandler.addWidget(boton,2)
            else:
                x = self.x+4
                y += 32
        EventHandler.addWidget(self.Items,4)
    
    @staticmethod
    def Guardar():
        if not Sys.Guardado:
            FileDiag({'scr':'Aceptar','tipo':'G','cmd':Sys.guardarProyecto},Sys.fdProyectos)
        else:
            Sys.guardarProyecto(Sys.Guardado)

    # barra
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    
    def addMob(self,ruta):
        sprite = r.split_spritesheet(ruta)
        nombre = path.split(ruta)[1][0:-4]
        _rect = sprite[0].get_rect(center=self.PrevArea.area.center)
        datos = {'nombre':nombre,'imagenes':sprite,'grupo':'mobs','tipo':'Mob','ruta':ruta,'pos':_rect.topleft}
        simbolo = SimboloMultiple(self.PrevArea,datos)
        self.addToPrevArea(nombre,simbolo)
        
    def addProp(self,ruta):
        sprite = r.cargar_imagen(ruta)
        nombre = path.split(ruta)[1][0:-4]
        _rect = sprite.get_rect(center=self.PrevArea.area.center)
        datos = {'nombre':nombre,'image':sprite,'grupo':'props','tipo':'Prop','ruta':ruta,'pos':_rect.topleft}
        simbolo = SimboloPanel(self.PrevArea,datos)
        self.addToPrevArea(nombre,simbolo)
    
    def addToPrevArea(self,nombre,simbolo):
        self.Items.setItem(nombre)
        self.PrevArea.agregarSimbolo(simbolo)
    
    def update(self):
        if Sys.HabilitarTodo:
            Sys.habilitarItems(self.botones[2:])
        else:
            Sys.deshabilitarItems(self.botones[2:])
    
    def hideMenu(self):
        print('dummy')

class area_prev(Marco):
    simbolos = None
    simbolo_actual = ''
    def __init__(self,parent,x,y,w,h,**opciones):
        if 'colorGrilla' not in opciones:
            opciones['colorGrilla'] = (150,200,200)
        super().__init__(x,y,w,h,False,**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.AreaPrev'
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        grilla = self.opciones['colorGrilla']
        self.image = self._dibujar_grilla(self._biselar(self.image,sombra,luz),grilla)
        self.area = Rect(self.x+2,self.y+2,self.w-4,self.h-18)
        self.simbolos = LayeredDirty()
        
    @staticmethod
    def _dibujar_grilla(imagen,color):
        w,h = imagen.get_size()
        marco = Rect(0,0,w-2,h-2)
        for x in range(1*C,6*C,C):
            draw.line(imagen, color, (x,marco.top), (x,marco.bottom))
        
        for y in range(1*C,13*C,C):
            draw.line(imagen, color, (marco.left,y), (marco.right,y))
        return imagen
    
    def agregarSimbolo(self,nuevoSimbolo):
        for simbolo in self.simbolos:
            simbolo.visible = False
        
        if nuevoSimbolo not in self.simbolos:
            self.simbolos.add(nuevoSimbolo)
        self.agregar(nuevoSimbolo)
    
    def update(self):
        nombre = self.parent.Items.getItemActual()
        if nombre != self.simbolo_actual:
            for simbolo in self.simbolos:
                if simbolo._nombre != nombre:
                    simbolo.visible = False
                else:
                    self.simbolo_actual = simbolo._nombre
                    simbolo.visible = True

class SimboloPanel (SimboloBase):
    copiar = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        self.image = self._imagen.copy()
        self.context = ContextMenu(self)
    
    def onMouseUp(self,button):
        if button == 1:
            super().onMouseUp(button)
            if self.copiar:
                Sys.copiar(self)
                Sys.pegar('Grilla.Canvas')
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            x,y = mouse.get_pos()
            self.px = x-self.x
            self.py = y-self.y
        elif button == 3:
            self.context.show()
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        if self.pressed:
            abs_x = mouse.get_pos()[0]
            dx,dy = self._arrastrar()
            #if self.parent.area.collidepoint(self.rect.x+dx,self.rect.y+dy):
            #    self.mover(dx,dy)
            if abs_x-self.rect.x < 0:
                self.copiar = True
    
    def hideMenu(self):
        print('dummy')
    
    def copy(self):
        self.data['rect'] = self.rect.copy()
        self.copiar = False
        return self.data

class SimboloMultiple(SimboloPanel):
    def __init__(self,parent,data,**opciones):
        self.images = self.cargar_anims(data['imagenes'],['S','I','D'])
        data['image'] = self.images['Sabajo']
        super().__init__(parent,data,**opciones)
        
        cmds = [
            {'nom':"Arriba",'cmd':lambda:self.cambiar_imagen('arriba')},
            {'nom':"Abajo",'cmd':lambda:self.cambiar_imagen('abajo')},
            {'nom':"Izquierda",'cmd':lambda:self.cambiar_imagen('izquierda')},
            {'nom':"Derecha",'cmd':lambda:self.cambiar_imagen('derecha')}]
        
        self.context = ContextMenu(self,cmds)
    
    def cambiar_imagen(self,direccion):
        self.image = self.images['S'+direccion]
        self.data['image'] = self.image
    
    @staticmethod
    def cargar_anims(spritesheet,seq,alpha=False):
        dicc,keys = {},[]
        dires = ['abajo','arriba','izquierda','derecha']
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            dicc[key] = spritesheet[keys.index(key)]
            
        return dicc