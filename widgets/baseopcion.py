from . import BaseWidget
from pygame import font,Rect, Surface
from globales import color
#from libs.textrect import render_textrect

class BaseOpcion(BaseWidget):
        
    def __init__(self,parent,nombre,x,y,w=0,h=0,**opciones):
        super().__init__(**opciones)
        self.x,self.y = x,y
        self.parent = parent
        self.nombre = self.parent.nombre+'.Opcion:'+nombre
        self.img_des = self.crear(nombre,color('sysElmText'),color('sysMenBack'),w)
        self.img_sel = self.crear(nombre,color('sysElmText'),color('sysBoxSelBack'),w)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
        self.dirty = 1
        
    def crear(self,nombre,fgcolor,bgcolor,w=0):
        if 'Fuente' not in self.opciones:
            self.opciones['fontType'] = 'Courier new'
        if 'fontSize' not in self.opciones:
            self.opciones['fontSize'] = 14
        
        fuente = font.SysFont(self.opciones['fontType'],self.opciones['fontSize'])
        if w == 0:
            
            w,h = fuente.size(nombre)
        else:
            h = fuente.get_height()
        rect = Rect(0,0,w,h)
        render = fuente.render(nombre,True,fgcolor,bgcolor)
        image = Surface(rect.size)
        image.fill(bgcolor)
        #image.set_clip(rect)
        image.blit(render,rect)
        
        
        return image
    
    def setText(self,text):
        self.nombre = self.parent.nombre+'.Opcion.'+text
        self.img_des = self.crear(text,color('sysElmText'),color('sysMenBack'),self.w)
        self.img_sel = self.crear(text,color('sysElmText'),color('sysBoxSelBack'),self.w)
        self.image = self.img_des
        self.w,self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft = (self.x,self.y))