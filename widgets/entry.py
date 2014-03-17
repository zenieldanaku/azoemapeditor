from pygame.constants import  K_END, K_HOME, K_LEFT, K_RIGHT, KMOD_LSHIFT, KMOD_RSHIFT
from pygame.constants import K_BACKSPACE, K_DELETE, K_RETURN, K_KP_ENTER
from pygame import Rect,Surface,font,draw,mouse,cursors,key
from . import BaseWidget
from constantes import *

class Entry(BaseWidget):
    texto = []
    cur_x = 4
    idx = 0
    cur_visible = False
    ticks,max_tick = 0,30
    seleccionando = False
    sel_start,sel_end = 0,0
    seleccion = None
    
    def __init__(self,parent,nombre,x,y,w,texto):
        super().__init__()
        self.parent = parent
        self.nombre = self.parent.nombre+'.Entry.'+nombre
        self.fuente = font.SysFont('courier new',14)
        self.x,self.y,self.w = x,y,w
        self.cursor =  ("        ",
                        "ooo ooo ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "   o    ",
                        "ooo ooo ")
        self.h = self.fuente.get_height()+4#21
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.image = Surface(self.rect.size)
        self.erase_area = Rect(1,1,self.w-2,self.h-2)
        self.write_area = Rect(4,2,self.w-2,self.h-4)
        self.dx = x+4
        self.setText(texto)
    
    def setText(self,texto):
        self.borrar_todo()
        self.texto = list(texto)
        self.imprimir()
        
    def devolver_texto(self):
        return ''.join(self.texto)
    
    def ingresar_caracter(self,char):
        index = self.idx
        if self.seleccion != None:
            self.borrar_seleccion()
        self.texto.insert(index,char)
    
    def borrar_caracter(self,dx):
        if 0 <= self.idx+dx < len(self.texto):
            del self.texto[self.idx+dx]
    
    def borrar_seleccion(self):
        del self.texto[self.seleccion]
        self.deseleccionar()
        #self.insertar_cursor()
        
    def borrar_todo(self):
        self.image.fill(blanco,self.erase_area)
    
    def imprimir(self):
        txt = ''.join(self.texto)
        render = self.fuente.render(txt,True,gris,blanco)

        if self.seleccion != None:
            sel = ''.join(self.texto[self.seleccion])
            render_sel = self.fuente.render(sel,True,negro,gris_seleccion)
            x = self.seleccion.start*8
            render.blit(render_sel,(x,0))

        self.image.blit(render,self.write_area)
    
    def dibujar_cursor(self):
        x = self.cur_x
        if not self.cur_visible:
            draw.line(self.image,negro,(x,3),(x,16),1)
        else:
            draw.line(self.image,blanco,(x,3),(x,16),1)
    
    def insertar_cursor(self):
        self.set_x()
        if self.idx > len(self.texto):
            self.cur_x = len(self.texto)*8+4
            self.idx = self.cur_x//8
            
    def mover_cursor(self,dx):
        self.idx += dx
        self.cur_x = self.idx*8+4
        if self.idx > len(self.texto):
            self.cur_x = len(self.texto)*8+4
            self.idx = self.cur_x//8
        elif self.idx < 0:
            self.cur_x = 4
            self.idx = 0
    
    def set_x(self):
        absX,absY = mouse.get_pos()
        self.cur_x = round((absX-self.dx)/8)*8+4
        self.idx = (round((absX-self.dx)/8)*8+4)//8
    
    def get_x(self):
        absX,absY = mouse.get_pos()
        cur_x = round((absX-self.dx)/8)*8+4
        idx = (round((absX-self.dx)/8)*8+4)//8
        return cur_x,idx
    
    def seleccionar(self):
        if self.sel_end != self.sel_start:
            if self.sel_end > self.sel_start:
                self.seleccion = slice(self.sel_start,self.sel_end,1)
            else:
                self.seleccion = slice(self.sel_end,self.sel_start,1)
        else:
            self.deseleccionar()
    
    def modificar_seleccion(self,dx):
        cur = self.idx
        if dx < 0:
            if cur < self.sel_start:
                self.sel_start += dx
                if self.sel_start <= 0:
                    self.sel_start = 0
                #print('caso A,','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
            elif cur > self.sel_start:
                self.sel_end += dx
                if self.sel_end > len(self.texto):
                    self.sel_end = len(self.texto)
                elif self.sel_end < 0:
                    self.sel_end = 0
                #print('caso B,','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
            elif cur > 0: # cur == self.sel_start
                self.sel_end += dx
                #print('caso E','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
        else:
            if cur > self.sel_end:
                self.sel_end += dx
                if self.sel_end < 0:
                    self.sel_end = 0
                #print('caso C,','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
            elif cur < self.sel_end:
                self.sel_start += dx
                if self.sel_start > len(self.texto):
                    self.sel_start = len(self.texto)
                #print('caso D,','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
            elif cur < len(self.texto): # cur == self.sel_end
                self.sel_start += dx
                #print('caso F','start',self.sel_start,'end',self.sel_end,'cur',cur,'dx',dx)
            
        self.seleccionar()
    
    def deseleccionar(self):
        self.seleccion = None
        self.sel_start = self.idx
        self.sel_end = self.idx
        
    def onMouseOver(self):
        if self.hasFocus:
            text = self.cursor
            curs,mask = cursors.compile(text,'o','o')
            mouse.set_cursor([8,16],[4,1],curs,mask)
            if self.seleccionando:
                self.sel_end = self.get_x()[1]
                self.seleccionar()
    
    def onMouseOut(self):
        super().onMouseOut()
        mouse.set_cursor(*cursors.arrow)
    
    def onMouseDown(self,dummy):
        self.insertar_cursor()
        self.seleccionando = True
        self.sel_start = self.idx
    
    def onMouseUp(self,dummy):
        self.insertar_cursor()
        self.seleccionando = False
        self.sel_end = self.idx
        self.seleccionar()
        
    def onKeyDown(self,event):
        mods = key.get_mods()
        if event.key == K_BACKSPACE:
            if self.seleccion == None:
                self.borrar_caracter(-1)
                self.mover_cursor(-1)
            else:
                self.borrar_seleccion()
        
        elif event.key == K_DELETE:
            if self.seleccion == None:
                self.borrar_caracter(+0)
            else:
                self.borrar_seleccion()
        
        elif event.key == K_RETURN or event.key == K_KP_ENTER:
            return self.texto # ????
        
        elif event.key == K_END:
            for i in range(len(self.texto)):
                self.mover_cursor(+1)
                if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT:    
                    self.modificar_seleccion(+1)
                else: self.deseleccionar()
                
        elif event.key == K_HOME:
            for i in range(len(self.texto)):
                self.mover_cursor(-1)
                if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT:
                    self.modificar_seleccion(+1)
                else: self.deseleccionar()
        
        elif event.key == K_LEFT:
            self.mover_cursor(-1)
            if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT:
                self.modificar_seleccion(-1)
            else: self.deseleccionar()
        
        elif event.key == K_RIGHT:
            self.mover_cursor(+1)
            if mods & KMOD_LSHIFT or mods & KMOD_RSHIFT:
                self.modificar_seleccion(+1)
            else: self.deseleccionar()
            
        elif event.unicode != '':
            self.ingresar_caracter(event.unicode)
            self.mover_cursor(+1)
        
        elif '[' in key.name(event.key):
            self.ingresar_caracter(key.name(event.key).strip('[]'))
            self.mover_cursor(+1)

        self.imprimir()
    
    def update(self):
        if self.hasFocus:
            self.ticks += 1
            if self.ticks == self.max_tick:
                self.ticks = 0
                self.cur_visible = not self.cur_visible
            self.borrar_todo()
            self.imprimir()
            self.dibujar_cursor()
        self.dirty = 1