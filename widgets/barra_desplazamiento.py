from pygame import Rect,Surface,MOUSEBUTTONUP,MOUSEBUTTONDOWN,mouse
from .basewidget import BaseWidget
from .cursor_barra import Cursor
from constantes import *

class Barra(BaseWidget):
    cursor = None
    
    def __init__(self,x,y,w,h):
        super().__init__()
        self.image = Surface((w,h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.image.fill(blanco)
        self.x,self.y = x,y
        self.w,self.h = h,w

        self.cursor = Cursor(self)
        self.crear_cursor()
        self.dirty = 2
        
    def crear_cursor(self):
        if self.w > self.h: # horizontal
            pos = (0,int(self.w/2))
            topleft = (15*C)+5,10*C
        else: # vertical
            pos = (int(self.h/2),0)
            topleft = 10*C,(15*C)+5
        
        cursor_rect = Rect(pos,self.cursor.rect.size)
        self.image.blit(self.cursor.image,cursor_rect)
        self.cursor.rect.topleft = topleft
    
    def redibujar(self):
        x,y = self.cursor.rect.topleft
        #print(y) # y-69 = 256
        self.image.fill(blanco)
        self.image.fill(verde,((0,y-69),self.cursor.rect.size))
        self.dirty = 2
    
    def event_handler(self,events):
        for event in events:                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y = mouse.get_pos()
                    x = int(x/32)*C+5
                    y = int(y/32)*C+5
                    if self.cursor.rect.collidepoint(x,y): 
                        self.cursor.pressed = True
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    x,y = mouse.get_pos()
                    x = int(x/32)*C+5
                    y = int(y/32)*C+5
                    if self.rect.collidepoint(x,y):
                        if self.cursor.pressed:
                            self.cursor.pressed = False
                            if self.w > self.h:
                                self.cursor.reposisionar(x-5)
                            else:
                                self.cursor.reposisionar(y-5)
                            
                            self.redibujar()
                            #_cursor_V = pygame.Rect((x,y),cursor_V.size)
                            #fondo.fill((125,0,125),(_cursor_V))
                            #cursor_V = _cursor_V