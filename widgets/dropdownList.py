from . import BaseWidget, Entry, Boton
from renderer import Renderer
from pygame import Surface,draw, Rect
from colores import color

class DropDownList(BaseWidget):
    def __init__(self,parent,nombre,x,y,w,lista,**opciones):
        super().__init__(**opciones)
        self.parent = parent
        self.nombre = self.parent.nombre+'.DropDownList'+nombre
        self.x,self.y = x,y
        self.entry = Entry(self,nombre,self.x,self.y-2,w-30,'')
        self.w,self.h = w,self.entry.h
        self.flecha = Boton(self,self.x+self.w-28,self.y-3,'Flecha',lambda:None,self.crear_flecha())
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.visible = 0
        Renderer.addWidget(self.entry)      
        Renderer.addWidget(self.flecha)
    
    def crear_flecha(self):
        imagen = Surface((28,25))
        imagen.fill(color('sysElmFace'))
        rect = imagen.get_rect()
        draw.polygon(imagen, color('sysScrArrow'), [[8,7],[rect.w//2-1,rect.h-10],[rect.w-10,7]])
        return imagen
    
    def onDestruction(self):
        Renderer.delWidget(self.entry)
        Renderer.delWidget(self.flecha)
    