from pygame import mouse, K_RIGHT,K_LEFT,K_UP,K_DOWN,K_DELETE
from .simboloBase import SimboloBase
from globales import Sistema as Sys, LAYER_FONDO, LAYER_COLISIONES
from widgets import ContextMenu

class SimboloCNVS (SimboloBase):
    selected = False
    
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        
        self.grupo = self.data['grupo']
        self.tipo = self.data['tipo']
        self.index = self.data['index']
        self.ruta = self.data['ruta']

        self.img_uns = self._imagen.copy()
        self.img_neg = self._crear_transparencia(self._imagen.copy())
        self.image = self.img_uns
        
        comandos = [
            {'nom':'subir','cmd':lambda:self.change_layer(+1)},
            {'nom':'bajar','cmd':lambda:self.change_layer(-1)}
        ]
        self.context = ContextMenu(self,comandos)

    @staticmethod
    def crear_img_sel(imagebase):
        over = imagebase.copy()
        over.fill((0,0,100), special_flags=1)
        return over
    
    def onMouseDown(self,button):
        if button == 1 or button == 3:
            self.onFocusIn()
            self.img_sel = self.crear_img_sel(self.image)
            self.image = self.img_sel
            self.selected = not self.selected
            self.pressed = True
            x,y = mouse.get_pos()
            self.px = x-self.x
            self.py = y-self.y
            if button == 3:
                self.pressed = False
                self.context.show()

    def onKeyDown(self,tecla,shift):
        if self.selected:
            x,y,d = 0,0,1
            if shift: d = 10
                
            if tecla == K_RIGHT:  x = +1*d
            elif tecla == K_LEFT: x = -1*d
            elif tecla == K_DOWN: y = +1*d
            elif tecla == K_UP:   y = -1*d
            elif tecla == K_DELETE:
                return True
            self.dx,self.dy = x,y
            self.mover(self.dx,self.dy)
    
    def onKeyUp(self,tecla):
        if tecla == K_RIGHT or tecla == K_LEFT:
            self.dx = 0
        elif tecla == K_DOWN or tecla == K_UP:
            self.dy = 0
    
    def onMouseOver(self):
        print('aca')
        
    def mover(self,dx,dy):
        super().mover(dx,dy)
        Sys.estado = self.tipo+' '+self._nombre+' #'+str(self.index)+' @ '+str(self.rect.topleft)
    
    def change_layer(self,mod):
        self.parent.cambiar_layer(self,mod)
        print(self.layer)
    
    def update(self):
        if self.selected:
            self.image = self.img_sel
            if self.pressed:
                dx,dy = self._arrastrar()
                self.mover(dx,dy)    
        elif Sys.capa_actual == LAYER_COLISIONES:
            self.image = self.img_neg
        elif Sys.capa_actual == LAYER_FONDO:
            self.image = self.img_uns
        self.dirty = 1