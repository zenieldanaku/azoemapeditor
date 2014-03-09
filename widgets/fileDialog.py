from . import BaseWidget,Marco, Entry, Boton, DropDownList, Label
from pygame import Rect, font, Surface, mouse
from libs.textrect import render_textrect
from renderer import Renderer
from constantes import *
from colores import color

class FileDiag(Marco):
    x,y,w,h = 0,0,0,0
    pressed = False

    def __init__(self,comando,**opciones):
        self.nombre = 'FileDiag'
        super().__init__(5*C,5*C,16*C,10*C+18,**opciones)
        self.titular(self.nombre)
        self.comando = comando['cmd']
        
        self.carpetas = arbolCarpetas(self,self.x+2,self.y+19,self.w//2-2,8*C)
        self.archivos = listaDeArchivos(self,self.x+self.w//2,self.y+19,self.w//2-2,8*C)
        self.entryNombre = Entry(self,'.IngresarRuta',self.x+2*C+3,self.y+8*C+23,12*C+25,'')
        self.BtnAccion = Boton(self,self.x+14*C+32,self.y+8*C+21,'Accion',self.ejecutar_comando,comando['scr'])
        self.tipos = DropDownList(self,'.TipoDeArchivo',self.x+2*C+3,self.y+9*C+17,12*C+25,[])
        self.BtnCancelar = Boton(self,self.x+15*C,self.y+9*C+15,'Cancelar',self.cerrar_ventana,'C')
        self.lblTipo = Label(self,'Tipo',self.x+4,self.y+9*C+16,texto = "Tipo:")
        self.lblNombre = Label(self,'Nombre',self.x+4,self.y+8*C+24, texto = 'Nombre:')    
        
        self.agregar(self.carpetas)
        self.agregar(self.archivos)
        self.agregar(self.entryNombre)
        self.agregar(self.BtnAccion)
        self.agregar(self.tipos)
        self.agregar(self.BtnCancelar)
        self.agregar(self.lblTipo)
        self.agregar(self.lblNombre)
    
    def titular(self,texto):
        fuente = font.SysFont('verdana',12)
        rect = Rect(2,2,self.w-4,fuente.get_height()+1)
        render = render_textrect(texto,fuente,rect,(255,255,255),(0,0,0))
        self.image.blit(render,rect)
    
    def ejecutar_comando(self):
        self.comando()
        self.cerrar_ventana()
    
    def cerrar_ventana(self):
        for widget in self.contenido:
            self.quitar(widget)
        Renderer.delWidget(self)
        
    
    def onMouseDown(self,boton):
        if boton == 1:
            self.cerrar_ventana()
    
    def onMouseUp(self,boton):
        if boton == 1:
            self.pressed = False
    
    def onMouseOut(self):
        if not self.pressed:
            super().onMouseOut()
    
    def onMouseOver(self):
        if self.pressed == True:
            x,y = mouse.get_pos()
            self.rect.x = x
            self.rect.y = y
            self.dirty = 1

class arbolCarpetas(Marco):
    def __init__(self,parent,x,y,w,h,**opciones):
        self.nombre = parent.nombre+'.ArbolDeCarpetas'
        super().__init__(x,y,w,h,False,**opciones)
        self.image.fill((255,0,0))

class listaDeArchivos(Marco):
    def __init__(self,parent,x,y,w,h,**opciones):
        self.nombre = parent.nombre+'.ListaDeArchivos'
        super().__init__(x,y,w,h,False,**opciones)
        self.image.fill((0,0,255))