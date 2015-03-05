from pygame.constants import  K_END, K_HOME, K_LEFT, K_RIGHT, KMOD_LSHIFT, KMOD_RSHIFT
from pygame.constants import K_BACKSPACE, K_DELETE, K_RETURN, K_KP_ENTER
from pygame import Rect,Surface,font,draw,mouse,cursors,key
from . import BaseWidget
from globales import color, C

class Entry(BaseWidget):
    texto = []
    cur_x = 4
    idx = 0
    cur_visible = False
    ticks,max_tick = 0,10
    seleccionando = False
    sel_start,sel_end = 0,0
    seleccion = None
    
    def __init__(self,parent,nombre,x,y,w,texto='',**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysBoxBack'
        if 'colorTexto' not in opciones:
            opciones['colorTexto'] = 'sysElmText'
        if 'colorSelect' not in opciones:
            opciones['colorSelect'] = 'sysBoxSelBack'
        if 'fontType' not in opciones:
            opciones['fontType'] = 'courier new'
        if 'fontSize' not in opciones:
            opciones['fontSize'] = 14
        super().__init__(**opciones)
        self.parent = parent
        self._nombre = nombre
        self.nombre = self.parent.nombre+'.Entry.'+self._nombre
        self.fuente = font.SysFont(opciones['fontType'],opciones['fontSize'])
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
        self.erase_area = Rect(1,1,self.w-2,self.h-2)
        self.write_area = Rect(4,2,self.w-2,self.h-4)
        self.image = Surface(self.rect.size)
        self.image.set_clip(self.erase_area)
        self.dx = x+4
        self.setText(texto)
    
    def setText(self,texto):
        self.borrar_todo()
        self.texto = list(texto)
        self.imprimir()
    
    def setMultipleTexts(self,lista):
        self.borrar_todo()
        self.texto = lista
        self.imprimir(True)
    
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
        self.image.fill(color(self.opciones['colorFondo']),self.erase_area)
    
    def imprimir(self,lista=False):
        cTexto =  color(self.opciones['colorTexto'])
        cFondo =  color(self.opciones['colorFondo'])
        cSelect = color(self.opciones['colorSelect'])
        
        if not lista:
            txt = ''.join(self.texto)
        else:
            txt = ', '.join(self.texto)
        render = self.fuente.render(txt,True,cTexto,cFondo)

        if self.seleccion != None:
            sel = ''.join(self.texto[self.seleccion])
            render_sel = self.fuente.render(sel,True,cTexto,cSelect)
            x = self.seleccion.start*8
            render.blit(render_sel,(x,0))

        self.image.blit(render,self.write_area)
    
    def dibujar_cursor(self,orden=None):
        x = self.cur_x
        if orden == None:
            if not self.cur_visible:
                draw.line(self.image,color(self.opciones['colorTexto']),(x,3),(x,16),1)
            else:
                draw.line(self.image,color(self.opciones['colorFondo']),(x,3),(x,16),1)
        elif orden:
            draw.line(self.image,color(self.opciones['colorTexto']),(x,3),(x,16),1)
        else:
            draw.line(self.image,color(self.opciones['colorFondo']),(x,3),(x,16),1)
    
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
            self.parent.onKeyDown(K_RETURN)
        
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
        else:
            self.dibujar_cursor(False)
        self.dirty = 1