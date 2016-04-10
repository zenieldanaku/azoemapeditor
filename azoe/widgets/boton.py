from azoe.engine import Resources as r, color, EventHandler
from pygame import font,Rect,draw,Surface, Color 
from azoe.libs.textrect import render_textrect
from . import BaseWidget, ToolTip
import os.path

class Boton(BaseWidget):
    comando = None
    presionado = False
    def __init__(self,parent,x,y,nombre,cmd,scr,tip=None,**opciones):
        opciones = self._opcionesPorDefault(opciones)
        super().__init__(parent,**opciones)
        self.x,self.y = x,y
        self.w,self.h = self.opciones['w'],self.opciones['h']
        self.nombre = self.parent.nombre+'.Boton.'+nombre
        self.comando = cmd
        if tip is not None:
            self.tooltip = ToolTip(self,tip,self.x,self.y)
        else:
            self.tooltip = None
        
        self._crear_imagenes(scr)
        
        self.image = self.img_uns
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    @staticmethod
    def _opcionesPorDefault(opciones):
        if 'colorBordeSombra' not in opciones:
            opciones['colorBordeSombra'] = 'sysElmShadow'
        if 'colorBordeLuz' not in opciones:
            opciones['colorBordeLuz'] = 'sysElmLight'
        if 'colorSelect' not in opciones:
            opciones['colorSelect'] = Color(125,255,255)
        if 'colorText' not in opciones:
            opciones['colorText'] = 'sysElmText'
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysElmFace'
        if 'colorDisabled'not in opciones:
            opciones['colorDisabled'] = 'sysDisText'
        if 'w' not in opciones:
            opciones['w'] = 28
        if 'h' not in opciones:
            opciones['h'] = 25
        if 'fontType' not in opciones:
            opciones['fontType'] = 'Verdana'
        if 'fontSize' not in opciones:
            opciones['fontSize'] = 16
        
        return opciones
    
    @staticmethod
    def  _crear(scr, color_texto, color_fondo,w,h,fuente):
        _rect = Rect(0,0,w,h)
        if type (scr) == Surface:
            img_rect = scr.get_rect(center=_rect.center)
            render = Surface((_rect.w,_rect.h))
            render.fill(color_fondo)
            render.blit(scr,img_rect)
        elif type (scr) == str:
            try:
                render = render_textrect(scr,fuente,_rect,color_texto,color_fondo,1)
            except:
                w,h = fuente.size(scr)
                _rect = Rect(-1,-1,w,h+1)
                render = render_textrect(scr,fuente,_rect,color_texto,color_fondo,1)
        
        return render
    
    def _crear_imagenes(self,scr):
        fuente = font.SysFont(self.opciones['fontType'],self.opciones['fontSize'])
        colorFondo   = color(self.opciones['colorFondo'])
        colorTexto   = color(self.opciones['colorText'])
        colorSText   = color(self.opciones['colorSelect'])
        colorDText   = color(self.opciones['colorDisabled'])
        colorBLuz    = color(self.opciones['colorBordeLuz'])
        colorBSombra = color(self.opciones['colorBordeSombra'])
        
        if type(scr) != list: #suponemos string
            scr = [scr,scr] #porque si no, serian dos imagenes.
        self.img_sel = self._biselar(self._crear(scr[0], colorSText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
        self.img_pre = self._biselar(self._crear(scr[0], colorSText, colorFondo,self.w,self.h,fuente),colorBSombra,colorBLuz)
        if type(scr[0]) != Surface:
            self.img_uns = self._biselar(self._crear(scr[0], colorTexto, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
            self.img_dis = self._biselar(self._crear(scr[1], colorDText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
        else:
            self.img_uns = self._crear(scr[0], colorTexto, colorFondo,self.w,self.h,fuente)
            self.img_dis = self._crear(scr[1], colorDText, colorFondo,self.w,self.h,fuente)
    
    def serElegido(self):
        if self.enabled:
            self.image = self.img_sel
            self.dirty = 1
    
    def serDeselegido(self):
        if self.enabled:
            self.image = self.img_uns
            self.presionado = False
            self.dirty = 1
    
    def serPresionado(self):
        if self.enabled:
            self.image = self.img_pre
            self.presionado = True
            self.dirty = 1
    
    def serDeshabilitado(self):
        if self.enabled:
            self.image = self.img_dis
            self.enabled = False
            self.dirty = 1
    
    def serHabilitado(self):
        if not self.enabled:
            self.image = self.img_uns
            self.enabled = True
            self.dirty = 1
    
    def on_mouse_in(self):
        super().on_mouse_in()
        self.serElegido()

    def on_mouse_out(self):
        super().on_mouse_out()
        self.serDeselegido()
        
    def on_mouse_down(self, button):
        if button == 1:
            if self.hasMouseOver:
                self.serPresionado()
    
    def on_mouse_up(self, dummy):
        if self.hasMouseOver and self.enabled:
            self.serElegido()
            self.comando()
    
    def update(self):
        if self.tooltip is not None:
            if self.enabled:
                if self.hasMouseOver:
                    self.tooltip.show()
                else:
                    self.tooltip.hide()
            else:
                self.tooltip.hide()

class BotonToggle(Boton):
    toggled = False
    def toggle(self):
        self.toggled = not self.toggled
        if self.toggled:
            self.img_sel = self.img_sel_T
            self.img_uns = self.img_uns_T
            self.img_dis = self.img_dis_T
            self.img_pre = self.img_pre_T
        else:
            self.img_sel = self.img_sel_nT
            self.img_uns = self.img_uns_nT
            self.img_dis = self.img_dis_nT
            self.img_pre = self.img_pre_nT
    
    def on_mouse_down(self, button):
        super().on_mouse_down(button)
        self.toggle()
    
    def _crear_imagenes(self,scr):
        fuente = font.SysFont(self.opciones['fontType'],self.opciones['fontSize'])
        colorFondo   = color(self.opciones['colorFondo'])
        colorTexto   = color(self.opciones['colorText'])
        colorSText   = color(self.opciones['colorSelect'])
        colorToggled = 255,0,0
        colorNonToggled = 255,255,255
        colorDText   = color(self.opciones['colorDisabled'])
        colorBLuz    = color(self.opciones['colorBordeLuz'])
        colorBSombra = color(self.opciones['colorBordeSombra'])
        
        if type(scr) != list: #suponemos string
            scr = [scr,scr,scr] #porque si no, serian dos imagenes.
    
        self.img_sel_T = self._biselar(self._crear(scr[0], colorSText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
        self.img_sel_nT = self._biselar(self._crear(scr[1], colorSText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
        
        self.img_pre_T = self._biselar(self._crear(scr[0], colorSText, colorFondo,self.w,self.h,fuente),colorBSombra,colorBLuz)
        self.img_pre_nT = self._biselar(self._crear(scr[1], colorSText, colorFondo,self.w,self.h,fuente),colorBSombra,colorBLuz)
        
        if type(scr[0]) != Surface:
            self.img_uns_T = self._biselar(self._crear(scr[0], colorToggled, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
            self.img_dis_T = self._biselar(self._crear(scr[2], colorDText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
            
            self.img_uns_nT = self._biselar(self._crear(scr[1], colorNonToggled, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
            self.img_dis_nT = self._biselar(self._crear(scr[2], colorDText, colorFondo,self.w,self.h,fuente),colorBLuz,colorBSombra)
        else:
            self.img_uns_T = self._crear(scr[0], colorToggled, colorFondo,self.w,self.h,fuente)
            self.img_dis_T = self._crear(scr[2], colorDText, colorFondo,self.w,self.h,fuente)
            
            self.img_uns_nT = self._crear(scr[1], colorNonToggled, colorFondo,self.w,self.h,fuente)
            self.img_dis_nT = self._crear(scr[2], colorDText, colorFondo,self.w,self.h,fuente)
        
        self.toggle()

class BotonAceptarCancelar(Boton):
    def __init__(self,parent,x,y,cmd=None,scr = '',**opciones):
        opciones.update({'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        
        if cmd is None:
            if hasattr(parent,'cerrar'):
                nombre = 'Cancelar'
                scr = 'Cancelar'
                cmd = lambda:EventHandler.del_widget(parent)
            else:
                raise TypeError
        else:
            if scr == '':
                nombre = 'Aceptar'
                scr = 'Aceptar'
            elif type(scr) is str:
                nombre = scr.title()
            
        super().__init__(parent,x,y,nombre,cmd,scr,**opciones)

class BotonCerrar(Boton):
    def __init__(self,parent,x,y,w,h,nombre,cmd,**opciones):
        opciones.update({'w':w,'h':h})
        
        fg_uns = color('sysElmText')
        fg_dis = color('sysDisText')
        bg = color('sysElmFace')
        
        img1 = Surface((11,11))
        img1.fill(bg)
        
        img2 = Surface((11,11))
        img2.fill(bg)

        draw.aaline(img2,fg_dis,[1,2],[9,8]) # \
        draw.aaline(img2,fg_dis,[1,8],[9,2]) # /
        
        draw.aaline(img1,fg_uns,[1,2],[9,8]) # \
        draw.aaline(img1,fg_uns,[1,8],[9,2]) # /
        
        super().__init__(parent,x,y,nombre,cmd,[img1,img2],**opciones)