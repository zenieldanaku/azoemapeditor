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
    
    def renombrar(self,texto):
        self._nombre = texto
        self.nombre = self.parent.nombre+'.Simbolo.'+self._nombre
        self.data['nombre'] = texto

class SimboloSimple (MetaSimbolo):
    copiar = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        self.img_pos = self._imagen.copy()
        self.img_neg = self._crear_transparencia(self._imagen.copy())
        self.image = self.img_pos
        self.context = ContextMenu(self)

class SimboloMultiple(MetaSimbolo):
    rot_idxs = {}
    curr_rot = 0
    def __init__(self,parent,data,**opciones):
        self.imgs_pos = self.cargar_anims(data['imagenes'],['S','I','D'])
        self.imgs_neg = self.cargar_anims(data['imagenes'],['S','I','D'],True)
        data['image'] = self.imgs_pos['Sabajo']
        self.curr_rot = 0
        super().__init__(parent,data,**opciones)
        self.img_pos = self.imgs_pos['Sabajo']
        self.img_neg = self.imgs_neg['Sabajo']
        self.image = self.img_pos
        
        cmds = [
            {'nom':"Abajo",'cmd':lambda:self.cambiar_imagen('abajo')},
            {'nom':"Arriba",'cmd':lambda:self.cambiar_imagen('arriba')},
            {'nom':"Derecha",'cmd':lambda:self.cambiar_imagen('derecha')},
            {'nom':"Izquierda",'cmd':lambda:self.cambiar_imagen('izquierda')}]
            
        self.context = ContextMenu(self,cmds)
    
    def cambiar_imagen(self,direccion):
        self.img_pos = self.imgs_pos['S'+direccion]
        self.img_neg = self.imgs_neg['S'+direccion]
        self.curr_rot = self.rot_idxs['S'+direccion]
        self.image = self.img_pos
        self.data['image'] = self.image
        self.data['rot'] = self.curr_rot
    
    def cargar_anims(self,spritesheet,seq,alpha=False):
        dicc,keys = {},[]
        dires = ['abajo','arriba','izquierda','derecha']
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            idx = keys.index(key)
            if not alpha:
                dicc[key] = spritesheet[idx]
                self.rot_idxs[key] = idx
            else:
                dicc[key] = self._crear_transparencia(spritesheet[idx])
        return dicc

