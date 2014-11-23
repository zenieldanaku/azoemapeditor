from .simboloVirtual import SimboloVirtual
from .simboloBase import SimboloBase
from globales import EventHandler
from widgets import ContextMenu
from pygame import mouse, Surface

class MetaSimbolo(SimboloBase):
    '''Metaclass para no repetir onMouseOver'''
    
    def onMouseOver(self):
        if self.pressed:
            x,y = mouse.get_pos()
            z = self.layer
            pos = x,y,z
            dx,dy = self._arrastrar()
            if dx != 0 or dy != 0:
                self.data['colisiones'] = self.img_cls
                self.data['cols_code'] = self.cls_code
                self.copia = SimboloVirtual(self,self.image.copy(),pos,self.data)
                EventHandler.setFocus(self.copia)
                self.pressed = False
        else:
            pass #showTooltip()
    
    def imagen_positiva(self):
        self.image = self.img_pos
    
    def imagen_negativa(self):
        if self.img_cls != None:
            img = self.img_cls.copy()
            img.blit(self.img_neg,(0,0),special_flags=6)
            self.image = img
        else:
            img = Surface(self.image.get_size())
            img.set_alpha(0)
            self.image = img

class SimboloSimple (MetaSimbolo):
    copiar = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        self.img_pos = self._imagen.copy()
        self.img_neg = self._crear_transparencia(self._imagen.copy())
        self.image = self.img_pos
        self.context = ContextMenu(self)

class SimboloMultiple(MetaSimbolo):
    def __init__(self,parent,data,**opciones):
        self.imgs_pos = self.cargar_anims(data['imagenes'],['S','I','D'])
        self.imgs_neg = self.cargar_anims(data['imagenes'],['S','I','D'],True)
        data['image'] = self.imgs_pos['Sabajo']
        super().__init__(parent,data,**opciones)
        self.img_pos = self.imgs_pos['Sabajo']
        self.img_neg = self.imgs_neg['Sabajo']
        self.image = self.img_pos
        
        cmds = [
            {'nom':"Arriba",'cmd':lambda:self.cambiar_imagen('arriba')},
            {'nom':"Abajo",'cmd':lambda:self.cambiar_imagen('abajo')},
            {'nom':"Izquierda",'cmd':lambda:self.cambiar_imagen('izquierda')},
            {'nom':"Derecha",'cmd':lambda:self.cambiar_imagen('derecha')}]
        
        self.context = ContextMenu(self,cmds)
    
    def cambiar_imagen(self,direccion):
        #self.image = self.images['S'+direccion]
        self.img_pos = self.imgs_pos['S'+direccion]
        self.img_neg = self.imgs_neg['S'+direccion]
        self.image = self.img_pos
        self.data['image'] = self.image
    
    def cargar_anims(self,spritesheet,seq,alpha=False):
        dicc,keys = {},[]
        dires = ['abajo','arriba','izquierda','derecha']
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            if not alpha:
                dicc[key] = spritesheet[keys.index(key)]
            else:
                dicc[key] = self._crear_transparencia(spritesheet[keys.index(key)])
            
        return dicc

