from pygame import mouse, K_RIGHT,K_LEFT,K_UP,K_DOWN,K_DELETE,Surface
from globales import Sistema as Sys, LAYER_FONDO, LAYER_COLISIONES
from .simboloBase import SimboloBase
from azoe.widgets import ContextMenu

class SimboloCNVS (SimboloBase):
    selected = False
    isMoving = False
    dx,dy = 0,0
    def __init__(self,parent,data,**opciones):
        super().__init__(parent,data,**opciones)
        
        self.grupo = self.data['grupo']
        self.tipo = self.data['tipo']
        self.index = self.data['index']
        self.ruta = self.data['ruta']
        self.rot = self.data.get('rot',0)

        self.img_pos = self._imagen.copy()
        self.img_neg = self._crear_transparencia(self._imagen.copy())
        self.img_cls = self.crear_img_cls(self.data['colisiones'])
        self.img_sel = self.crear_img_sel(self._imagen.copy())
        self.image = self.img_pos
        
        comandos = [
            {'nom':'Subir','cmd':lambda:self.change_layer(+1)},
            {'nom':'Bajar','cmd':lambda:self.change_layer(-1)},
            {'nom':'barra'},
            {'nom':'Cortar','cmd':Sys.cortar,'icon':Sys.iconos['cortar']},
            {'nom':'Copiar','cmd':Sys.copiar,'icon':Sys.iconos['copiar']},
        ]
        self.context = ContextMenu(self,comandos)
    
    def copiar(self):
        datos = self.data.copy()
        datos['rect'] = self.rect.copy()
        datos['original'] = False
        return datos
        
    @staticmethod
    def crear_img_sel(imagebase):
        over = imagebase.copy()
        over.fill((0,0,100), special_flags=1)
        return over
    
    def crear_img_cls(self,imagebase):
        if imagebase != None:
            return imagebase
        else:
            img = Surface(self.img_pos.get_size())
            img.set_alpha(0)
            return img
    
    def on_mouse_down(self, button):
        if button == 1:
            self.on_focus_in()
            self.img_sel = self.crear_img_sel(self._imagen.copy())
            if not self.selected:
                self.serElegido()
            self.pressed = True
            x,y = mouse.get_pos()
            self.px = x-self.x
            self.py = y-self.y
        
        elif button == 3:
            if not self.selected:
                self.serElegido()
            self.context.show()
    
    def on_key_down(self, tecla, shift):
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
    
    def on_key_up(self, tecla):
        if tecla == K_RIGHT or tecla == K_LEFT:
            self.dx = 0
        elif tecla == K_DOWN or tecla == K_UP:
            self.dy = 0
        
    def mover(self,dx,dy):
        self.isMoving = True
        super().mover(dx,dy)
        Sys.estado = self.tipo+' '+self._nombre+' #'+str(self.index)+' @ ('+str(self.rect.x)+','+str(self.rect.y)+','+str(self.z)+')'
    
    def change_layer(self,mod):
        self.parent.cambiar_layer(self,mod)
        self.z += mod
        Sys.estado = self.tipo+' '+self._nombre+' #'+str(self.index)+' @ ('+str(self.rect.x)+','+str(self.rect.y)+','+str(self.z)+')'
    
    def serElegido(self):
        self.selected = True
        Sys.selected = self
        self.image = self.img_sel
        Sys.estado = self.tipo+' '+self._nombre+' #'+str(self.index)+' @ ('+str(self.rect.x)+','+str(self.rect.y)+','+str(self.z)+')'
    
    def serDeselegido(self):
        self.selected = False
        Sys.selected = None
    
    def update(self):
        self.dx,self.dy = 0,0
        self.isMoving = False
        if self.selected:
            if self.pressed:
                dx,dy = self._arrastrar()
                if (dx,dy) != (0,0):
                    self.mover(dx,dy)
                self.dx,self.dy = dx,dy
        elif Sys.capa_actual == LAYER_COLISIONES:
            self.image = self.img_cls
        
        elif Sys.capa_actual == LAYER_FONDO:
            self.image = self.img_pos
        self.dirty = 1