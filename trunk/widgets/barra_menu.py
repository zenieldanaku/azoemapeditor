from .basewidget import BaseWidget
from constantes import *
from pygame import Rect,Surface,draw,font,mouse
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from renderer import Renderer

class Menu_barra(BaseWidget):
    botones = None
    
    def __init__(self,nom_menu,x,y,w,h,botones):
        super().__init__()
        self.botones = LayeredDirty()
        self.nombre = nom_menu
        self.rect = Rect(x,y,w,h)
        self.image = Surface(self.rect.size)
        self.image.fill(gris)
        draw.rect(self.image,negro,(0,0,w-2,h-2),2)
        
        prev  = 0
        for btn in botones:
            boton = boton_menu(btn,prev+4,6)
            prev = boton.rect.right
            self.botones.add(boton)
            Renderer.addWidget(boton,2)
        
        self.botones.draw(self.image)
            
class boton_menu(BaseWidget):
    nombre = ''
    menu = None
    resaltado = False
    
    def __init__(self,nombre,x,y):
        super().__init__()
        self.nombre = nombre
        self.layer = 2
        self.img_des = self.crear_boton(self.nombre,negro)
        self.img_sel = self.crear_boton(self.nombre,cian_claro)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.menu = self.establecer_menus(nombre)
        self.dirty = 2
        
    def establecer_menus (self,nombre):
        # esto es chapuza
        if nombre == 'Archivo': 
            menu_nom = ['Nuevo','Abrir...','Guardar','Guardar como...','Cerrar']
        elif nombre == 'Editar':
            menu_nom = ['Preferencias...']
        elif nombre == 'Mapa':
            menu_nom = ['Grilla...','Capas...']
        elif nombre == 'Símbolo':
            menu_nom = ['Mobs...','Props...']
        else:
            menu_nom = ['']
        
        if menu_nom != ['']:
            return PullDownMenu(menu_nom,*self.rect.bottomleft)
    
    def crear_boton(self,nombre,color):
        fuente = font.SysFont('Verdana',14)
        w,h = fuente.size(nombre)
        rect = Rect(-1,-1,w,h+1)
        render = render_textrect(nombre,fuente,rect,color,gris,1)
        return render

    def onMouseDown (self,event):
        if event.button == 1:
            x,y = mouse.get_pos()
            if self.rect.collidepoint(x,y):
                if self.menu != None:
                    if self.menu.visible != True:
                        self.menu.visible = True
                        for boton in self.menu.botones:
                            boton.visible = True
                            boton.enabled = True
                    else:
                        self.menu.visible = False
                        for boton in self.menu.botones:
                            boton.visible = False
                            boton.enabled = False
    
    def onFocusOut(self):
        super().onFocusOut()
        if self.menu != None:
            self.menu.visible = False
            for boton in self.menu.botones:
                boton.visible = False
    
    def onMouseOver(self,event):
        self.image = self.img_sel
    
    def offMouseOver(self):
        self.image = self.img_des
    
class PullDownMenu (BaseWidget):
    botones = None
    def __init__(self,nombres,x,y):
        self.botones = LayeredDirty()
        alto,ancho = 0,0
        for n in range(len(nombres)):
            boton = boton_menu(nombres[n],x,y)
            w,h = boton.image.get_size()
            alto += h+1
            if w > ancho:
                ancho = w
            boton.rect.topleft = x,((h+1)*n)+y
            self.botones.add(boton)
            boton.visible = False
            boton.enabled = False
            Renderer.addWidget(boton,3)
        
        super().__init__()
        image = Surface((ancho,alto))
        image.fill(gris)
        self.image = image
        self.rect = self.image.get_rect(topleft = (x,y))
        Renderer.addWidget(self,2)
        self.visible = False
        self.dirty = 2