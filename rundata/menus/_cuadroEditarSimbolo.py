from pygame.sprite import DirtySprite, LayeredDirty
from pygame import Rect,Surface,draw, mouse
from widgets import subVentana, Marco, Boton, Label
from globales import Sistema as Sys, C, EventHandler

class EditarSimbolo(subVentana):
    pressed = False
    brocha = 1
    esTransparente = False
    tile = None
    LAYER_COLISION = 0
    LAYER_SPRITE = 1
    def __init__(self):
        self.nombre = 'Editar Simbolo'
        super().__init__(4*C,3*C,12*C,10*C,self.nombre)
        x,y,w,h = self.x,self.y,self.w,self.h

        self.area = self.crear_area(x,y)
        self.image.fill((0,0,0),(self.area.rect))
        self.capas = LayeredDirty()
        self.capas.add(self.area,layer=self.LAYER_COLISION)
        for tile in EventHandler.getWidget('Grilla.Canvas').tiles:
            if tile.selected:
                self.tile = self.crear_sprite(tile,self.area.rect.center)
                self.capas.add(self.tile,layer=self.LAYER_SPRITE)
                break
        
        self.btnMas = Boton(self,x+w-C,y+C,'Aumentar',lambda:self.ajustar_brocha(+1),'+',tip='Aumenta en un punto el tamaño de la brocha')
        self.btnMenos = Boton(self,x+w-C,y+2*C-7,'Disminuir',lambda:self.ajustar_brocha(-1),'-',tip='Disminuye en un punto el tamaño de la brocha')
        self.btnTrans = Boton(self,x+w-C,y+3*C-7,'Transparencia',lambda:self.alternar_transparencia(),'Tr',tip='Alterna entre la transparencia del sprite')
        self.btnCapas = Boton(self,x+w-C,y+4*C-14,'AlterarCapas',lambda:self.alternar_capas(),'Cp',tip='Alerna el orden de las capas de sprite y de colisiones')
        self.btnAceptar = Boton(self,x+w-C*4-16,y+h-28,'Aceptar',lambda:None,'Aceptar',tip='',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.btnCancelar = Boton(self,x+w-C*2-10,y+h-28,'Cancelar',lambda:None,'Cancelar',tip='',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.lblBrocha = Label(self,'TamanioDeBrocha',x+3,y+h-28,'Brocha: '+str(self.brocha))
        self.agregar(self.btnMas)
        self.agregar(self.btnMenos)
        self.agregar(self.btnTrans)
        self.agregar(self.btnCapas)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
        self.agregar(self.lblBrocha,layer=self.layer+1)
    
    @staticmethod
    def crear_area(x,y):
        spr = DirtySprite()
        spr.image = Surface((10*C,8*C))
        spr.image.set_colorkey((0,0,0))
        spr.rect = spr.image.get_rect(topleft=(C,C))
        spr.dRect = spr.image.get_rect(topleft=(x+C,y+C))
        spr.dirty = 2
        return spr
    
    @staticmethod
    def crear_sprite(sprite,center_pos):
        spr = DirtySprite()
        spr.img_uns = sprite.img_uns
        spr.img_neg = sprite.img_neg
        spr.image = spr.img_uns
        spr.rect = spr.image.get_rect(center = center_pos)
        spr.dirty = 2
        return spr
    
    def ajustar_brocha(self,mod):
        self.brocha += mod
        if self.brocha < 1:  self.brocha = 1
        if self.brocha > 99: self.brocha = 99
        self.lblBrocha.setText('Brocha: '+str(self.brocha))
    
    def alternar_transparencia(self): self.esTransparente = not self.esTransparente
    def alternar_capas(self): self.capas.switch_layer(self.LAYER_COLISION,self.LAYER_SPRITE)
    
    def onMouseUp(self,button): self.pressed = False
    
    def onMouseDown(self,button):
        x,y = mouse.get_pos()
        _rect = self.area.rect.copy()
        _rect.topleft = (self.x+C,self.y+C)
        if button == 1:
            if _rect.collidepoint((x,y)):
                self.pressed = True
    
    def update(self):
        if self.pressed:
            x,y = mouse.get_pos()
            rect = Rect(0,0,self.brocha,self.brocha)
            dx = x-(self.x+C)-rect.w//2
            dy = y-(self.y+C)-rect.h//2
            self.area.image.fill((255,0,255),((dx,dy),(rect.size)))
        
        if self.tile != None:
            if self.esTransparente:
                self.tile.image = self.tile.img_neg            
            else:
                self.tile.image = self.tile.img_uns    
        
        self.capas.draw(self.image)
        
        self.dirty = 1
        
