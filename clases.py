from pygame.sprite import DirtySprite
from pygame import draw,Rect,Surface
from constantes import Colores as k, C

class Grilla(DirtySprite):
    pos = [0,0]
    tam = [0,0]
    
    def __init__(self,posicion,tamanio):
        super().__init__()
        self.pos = posicion
        self.tam = tamanio
        self.image = self.dibujar_grilla(tamanio)
        self.rect = self.image.get_rect(topleft=posicion)
    
    def dibujar_grilla(self,tamanio):
        grilla_surf = Surface(tamanio)
        grilla_surf.fill(k.gris)
        marco = Rect(64,64,(16*32)-2,(16*32)-2)
        for i in range(3*32,18*32,32):
            draw.line(grilla_surf, k.blanco, (i,marco.top), (i,marco.bottom),1)
            draw.line(grilla_surf, k.blanco, (marco.left,i), (marco.right,i),1)
        draw.rect(grilla_surf, k.negro, marco, 2)
        
        return grilla_surf
    
    def redibujar(self):
        self.image = dibujar_grilla(self.tam)

class barra_desplazamiento(DirtySprite):
    cursor = None
    
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = Surface((w,h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image.fill(k.blanco)
        self.x,self.y = x,y
        self.w,self.h = h,w

        self.cursor = cursor_barra()
        self.crear_cursor()
        self.dirty = 2
        
    def crear_cursor(self):
        if self.w > self.h: # horizontal
            pos = (0,8*C)
            topleft = (18*C)+5,10*C
        else: # vertical
            pos = (8*C,0)
            topleft = 10*C,(18*C)+5
        
        cursor_rect = Rect(pos,self.cursor.rect.size)
        self.image.blit(self.cursor.image,cursor_rect)
        self.cursor.rect.topleft = topleft
    
    def redibujar(self):
        x,y = self.cursor.rect.topleft
        #print(y) # y-69 = 256
        print(x)
        self.image.fill(k.blanco)
        self.image.fill(k.verde,((0,y-69),self.cursor.rect.size))
        self.dirty = 2
    
class cursor_barra(DirtySprite):
    size = 1/2*C,1/2*C
    pressed = False
    def __init__(self):
        super().__init__()
        self.image = Surface(self.size)
        self.image.fill(k.violeta)
        self.rect = self.image.get_rect()
        self.pressed = False
        self.dirty = 2
    
    def reposisionar(self,x,y):
        self.rect.topleft = x,y
        self.image.fill(k.verde)
        self.dirty = 2