from pygame import Rect,Surface,draw,mouse
from pygame.sprite import LayeredDirty
from widgets import Marco, BaseWidget, FileDiag
from widgets import Boton, DropDownList, Entry
from renderer import Renderer
from colores import color
from constantes import *
from globales import SharedFunctions as shared, GLOBALES as G, Resources as r

class PanelSimbolos(Marco):
    simbolos = None
    botones = []
    def __init__(self,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = color('sysElmFace')

        super().__init__(16*C,1*C,4*C+8,16*C-1,**opciones)
        self.nombre = 'PanelSimbolos'
        self.simbolos = LayeredDirty()
        self.PrevArea = area_prev(self,self.x+3,self.y+3*C,self.w-6,13*C-2)
        n,s,t,c,d = 'nom','scr','tipo','cmd','des'
        elementos = [
            {n:'Nuevo',c:shared.nuevoMapa,s:"N",d:"Crear un mapa nuevo"},
            {n:'Abrir',c:lambda:FileDiag({s:'A',t:'A',c:shared.abrirMapa}),s:"A",d:"Abrir un mapa existente"},
            {n:'Guardar',c:self.Guardar,s:"G",d:"Guardar el mapa actual"},
            {n:'barra'},
            {n:'Cortar',c:self.Cortar,s:"X",d:"Cortar"},
            {n:'Copiar',c:self.Copiar,s:"C",d:"Copiar"},
            {n:'Pegar',c:self.Pegar,s:"P",d:"Pegar"},
            {n:'barra'},
            {n:'SetFondo',c:lambda:FileDiag({s:'A',t:'A',c:shared.setRutaFondo}),s:"Fd",d:"Cargar imagen de fondo"},
            {n:'SetColis',c:lambda:FileDiag({s:'A',t:'A',c:shared.setRutaColis}),s:"Cl",d:"Cargar imagen de colisiones"},
            {n:'addMob',c:lambda:FileDiag({s:'A',t:'A',c:self.addMob}),s:"Mb",d:"Cargar símbolo de mob (no funciona)"},
            {n:'addProp',c:lambda:FileDiag({s:'A',t:'A',c:self.addProp}),s:"Pr",d:"Cargar símbolo de prop"},
            ]
        x = self.x+4
        y = 1*C+4
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self,x+5,y,e['nom'],e['cmd'],e['scr'],descripcion = e['des'])
                x = boton.rect.right-2
                self.botones.append(boton)
                Renderer.addWidget(boton,2)
            else:
                x = self.x+4
                y += 32
                   
    def Guardar(self):
        #tendría que fijarse si hay cambios.
        FileDiag({'scr':'G','tipo':'G','cmd':shared.guardarMapa})

    # barra
    def Cortar(self):
        print('boton cortar')
    def Copiar(self):
        print('boton copiar')
    def Pegar(self):
        print('boton pegar')
    
    def addMob(self,ruta):
        sprite = r.split_spritesheet(ruta)
        nombre = os.path.split(ruta)[1][0:-4]
        
    def addProp(self,ruta):
        sprite = r.cargar_imagen(ruta)
        nombre = os.path.split(ruta)[1][0:-4]
        datos = {'nombre':nombre,'image':sprite,'tipo':'Prop','ruta':ruta}
        self.PrevArea.agregarSimbolo(datos)
    
    def update(self):
        if G.HabilitarTodo:
            G.habilitarItems(self.botones[2:])
        else:
            G.deshabilitarItems(self.botones[2:])
            
class area_prev(Marco):
    simbolos = None
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
    
    def agregarSimbolo(self,datos):
        simbolo = Simbolo(self,datos)
        simbolo.rect.x += self.area.x
        simbolo.rect.y += self.area.y

        if simbolo not in self.simbolos:
            self.simbolos.add(simbolo)
        self.agregar(simbolo)

class Simbolo (BaseWidget):
    pressed = False
    enArea = True
    copiar = False
    def __init__(self,parent,data,**opciones):
        super().__init__(**opciones)
        self.data = data
        self.parent = parent
        self.image = self.data['image']
        self._nombre = self.data['nombre']
        self.nombre = self.parent.nombre+'.Simbolo.'+self._nombre
        self.x,self.y = 0,0
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def onMouseDown(self,button):
        if button == 1:
            self.pressed = True
            
    def onMouseUp(self,button):
        if button == 1:
            self.pressed = False
            if self.copiar:
                shared.copiar(self)
                shared.pegar('Grilla.Canvas')
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        x,y = mouse.get_pos()
        dx = x-self.w//2
        dy = y-self.h//2
        self.enArea = self.parent.area.collidepoint(dx,dy)
        if self.pressed:
            if self.enArea:
                self.mover(dx,dy)
            elif x-self.rect.x < 0:
                self.copiar = True
        
    def mover(self,dx=0,dy=0):
        self.rect.topleft = dx,dy
        self.x,self.y = dx,dy
    
    def copy(self):
        #datos = {'nombre':self._nombre,'image':self.image}
        return Simbolo(self.parent,self.data)
