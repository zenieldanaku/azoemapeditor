from globales import Sistema as Sys, Resources as r, C, color, LAYER_COLISIONES, LAYER_FONDO
from widgets import Marco, FileDiag, Boton, DropDownList
from .simbolos import SimboloSimple,SimboloMultiple
from .menus.menu_mapa import CuadroMapa
from pygame.sprite import LayeredDirty
from pygame import Rect,draw, Surface
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
            {n:'Abrir',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.abrirProyecto},carpeta_actual=Sys.fdProyectos),s:"A",d:"Abrir un mapa existente"},
            {n:'Guardar',c:self.Guardar,s:"G",d:"Guardar el mapa actual"},
            {n:'barra'},
            {n:'Cortar',c:self.Cortar,s:"X",d:"Cortar"},
            {n:'Copiar',c:self.Copiar,s:"C",d:"Copiar"},
            {n:'Pegar',c:self.Pegar,s:"P",d:"Pegar"},
            {n:'barra'},
            {n:'SetFondo',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.setRutaFondo},carpeta_actual=Sys.fdAssets),s:"Fd",d:"Cargar imagen de fondo"},
            #{n:'SetColis',c:lambda:FileDiag({s:'Aceptar',t:'A',c:Sys.setRutaColis},carpeta_actual=Sys.fdAssets),s:"Cl",d:"Cargar imagen de colisiones"},
            {n:'addMob',c:lambda:FileDiag({s:'Aceptar',t:'A',c:self.addMob},carpeta_actual=Sys.fdAssets),s:"Mb",d:"Cargar símbolo de mob"},
            {n:'addProp',c:lambda:FileDiag({s:'Aceptar',t:'A',c:self.addProp},carpeta_actual=Sys.fdAssets),s:"Pr",d:"Cargar símbolo de prop"}            
            ]
        x = self.x+4
        y = 19+4
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+5,y,e['nom'],e['cmd'],e['scr'],e['des'])
                x = boton.rect.right-2
                self.botones.append(boton)
                self.agregar(boton,2)
            else:
                x = self.x+4
                y += 32
        self.agregar(self.Items,4)
    
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
        simbolo = SimboloSimple(self.PrevArea,datos)
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
        self.img_pos = self._dibujar_grilla(self._biselar(self.image,sombra,luz),grilla)
        self.img_neg = self._dibujar_grilla(self._biselar(Surface((w,h)),sombra,luz),grilla)
        self.image = self.img_pos
        self.area = Rect(self.x+2,self.y+2,self.w-4,self.h-18)
        self.simbolos = LayeredDirty()
        
        self.btnDel = Boton(self,self.rect.right-31,self.rect.bottom+2,'delSim',self.eliminarSimboloActual,'D',"Eliminar este símbolo")
        self.btnDel.serDeshabilitado()
        self.agregar(self.btnDel,4)
        
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
    
    def eliminarSimboloActual(self):
        for simbolo in self.simbolos:
            if simbolo._nombre == self.simbolo_actual:
                self.simbolos.remove(simbolo)
                self.quitar(simbolo)
                self.parent.Items.delItem(simbolo)
                break
    
    def clear(self):
        self.simbolos.empty()
        self.limpiar()
        self.parent.Items.clear()
    
    def update(self):
        if not Sys.HabilitarTodo:
            self.clear()
        nombre = self.parent.Items.getItemActual()
        if nombre != self.simbolo_actual:
            for simbolo in self.simbolos:
                if simbolo._nombre != nombre:
                    simbolo.visible = False
                else:
                    self.simbolo_actual = simbolo._nombre
                    simbolo.visible = True
                    self.parent.Items.setText(self.simbolo_actual)
        
        if len(self.simbolos)!= 0:
            self.btnDel.serHabilitado()
        
        capa = Sys.capa_actual
        if capa == LAYER_FONDO:
            self.image = self.img_pos
            for simbolo in self.simbolos:
                simbolo.image = simbolo.img_pos
        elif capa == LAYER_COLISIONES:
            self.image = self.img_neg
            for simbolo in self.simbolos:
                simbolo.image = simbolo.img_neg