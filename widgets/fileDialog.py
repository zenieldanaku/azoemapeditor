from . import BaseWidget,Marco, Entry, Boton, BotonAceptarCancelar, DropDownList, subVentana
from . import Label, ScrollV, ScrollH, Tree, BaseOpcion, ToolTip
from pygame import Rect, font, key, KMOD_LCTRL, KMOD_RCTRL
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from globales import color, C
import os, os.path

class FileDiag(subVentana):
    pressed = False
    carpetaActual = ''
    ArchivosSeleccionados = []
    UltimaSeleccion = ''
    nombredeArchivo = ''
    tipoSeleccinado = ''
    carpetaVieja = ''
    layer = 10
    def __init__(self,comando,permitirmultiple=False,filetypes=[],carpeta_actual=os.getcwd(),**opciones):      
        self.comando = comando['cmd']
        self.TipoComando = comando['tipo']
        self.nombre = 'FileDialog.'
        if self.TipoComando == 'A':
            self.nombre += 'Abrir'
        elif self.TipoComando == 'G':
            self.nombre += 'Guardar'
        elif self.TipoComando == 'Gc':
            self.nombre += 'Guardar como...'
        super().__init__(16*C,10*C+18,self.nombre,**opciones)
        self.SeleccionMultiple = permitirmultiple
        self.carpetaActual = ''
        self.ArchivosSeleccionados = []
        self.UltimaSeleccion = ''
        self.nombredeArchivo = ''
        self.tipoSeleccinado = ''
        self.carpetaVieja = ''
        
        if len(filetypes) == 0: filetypes = ['*.png','*.json','*.mob','*.quest']
        x,y,w,h = self.x,self.y,self.w,self.h # abreviaturas de legibilidad
        self.carpetas = arbolCarpetas(self,x+2,y+19,w//2-2,8*C,carpeta_actual)
        self.archivos = listaDeArchivos(self,x+w//2,y+19,w//2-2,8*C,self.SeleccionMultiple)
        self.entryNombre = Entry(self,'IngresarRuta',x+2*C+3,y+8*C+23,11*C+16,'')
        self.BtnAccion = BotonAceptarCancelar(self,x+14*C-8,y+8*C+24,self.ejecutar_comando,comando['scr'])
        self.tipos = DropDownList(self,'TipoDeArchivo',x+2*C+3,y+9*C+19,11*C+16,filetypes)
        self.BtnCancelar = BotonAceptarCancelar(self,x+14*C-8,y+9*C+20)
        self.lblNombre = Label(self,'Nombre',x+4,y+9*C-7, texto = 'Nombre:',**{'fontType':'Tahoma','fontSize':13})
        self.lblTipo = Label(self,'Tipo',x+4,y+9*C+19,texto = "Tipo:",**{'fontType':'Tahoma','fontSize':13})
        
        self.agregar(self.carpetas,self.layer+1)
        self.agregar(self.archivos,self.layer+1)
        self.agregar(self.entryNombre,self.layer+1)
        self.agregar(self.BtnAccion,self.layer+1)
        self.agregar(self.tipos,self.layer+1)
        self.agregar(self.BtnCancelar,self.layer+1)
        self.agregar(self.lblTipo,self.layer+1)
        self.agregar(self.lblNombre,self.layer+1)
        
    def titular(self,texto):
        fuente = font.SysFont('verdana',12)
        rect = Rect(2,2,self.w-4,fuente.get_height()+1)
        render = render_textrect(texto,fuente,rect,(255,255,255),(0,0,0))
        self.image.blit(render,rect)
    
    def ejecutar_comando(self):
        if self.TipoComando == 'A':
            if self.SeleccionMultiple:
                rutas = []
                for archivo in self.ArchivosSeleccionados:
                    rutas.append(os.path.join(self.carpetaActual,archivo))
                self.comando(rutas)
            else:
                
                ruta = os.path.join(self.carpetaActual,self.UltimaSeleccion)
                self.comando(ruta)
                
        elif self.TipoComando == 'G' or self.TipoComando == 'Gc':
            if self.tipoSeleccinado != '' and not self.nombredeArchivo.endswith(self.tipoSeleccinado):
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo+self.tipoSeleccinado)
            else:
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo)
            self.comando(ruta)
            
        self.cerrar()
    
    def update(self):
        tipo = self.tipos.ItemActual.lstrip('*')
        if self.tipoSeleccinado != tipo:
            self.tipoSeleccinado = tipo
            self.archivos.actualizarLista(self.carpetaActual,self.tipoSeleccinado.lstrip('.'))
            
        self.carpetaActual = self.carpetas.CarpetaSeleccionada
        if self.carpetaActual != self.carpetaVieja:
            self.carpetaVieja = self.carpetaActual
            self.archivos.actualizarLista(self.carpetaActual,self.tipoSeleccinado.lstrip('.'))
        
        nombre = self.entryNombre.devolver_texto()
        if nombre != '':
            self.nombredeArchivo = nombre
        
        if self.archivos.Seleccionados != []:
            if self.SeleccionMultiple:
                for archivo in self.archivos.Seleccionados:
                    if archivo not in self.ArchivosSeleccionados:
                        self.ArchivosSeleccionados.append(archivo)
                self.entryNombre.setMultipleTexts(self.archivos.Seleccionados)
                    
            elif self.archivos.UltimaSeleccion != self.nombredeArchivo:
                self.entryNombre.setText(self.archivos.UltimaSeleccion)
                self.UltimaSeleccion = self.archivos.UltimaSeleccion
        
        self.dirty = 1

class arbolCarpetas(Marco):
    CarpetaSeleccionada = ''
    
    def __init__(self,parent,x,y,w,h,carpeta_actual,**opciones):
        self.nombre = parent.nombre+'.ArbolDeCarpetas'
        self.layer = parent.layer+2
        super().__init__(x,y,w,h,False,**opciones)
        self.arbol = Tree(self,self.x,self.y,self.w-16,self.h,self._generar_arbol(os.getcwd()),carpeta_actual)
        #self.arbol.doc_h = h
        self.arbol.ScrollY = ScrollV(self.arbol,self.x+self.w-16,self.y)
        self.agregar(self.arbol.ScrollY,self.layer+1)
        self.agregar(self.arbol,self.layer+1)
        self.CarpetaSeleccionada = carpeta_actual
    
    @staticmethod #decorator! ^^ 'cause explicit is better than implicit
    def _generar_arbol(path):
        walk = []
        x,y = -1,-1
        root_ = ''
        roots = []
        for dirname, dirnames, dummy in os.walk(path):
            split = os.path.split(dirname)
            nombre = split[1]
            root = os.path.split(split[0])[1]
            if '.git' in dirnames:
                dirnames.remove('.git')
            if '__pycache__' in dirnames:
                dirnames.remove('__pycache__')
            for subdirname in dirnames:
                if subdirname.startswith('_'):
                    dirnames.remove(subdirname)
            
            if root in roots:
                x = roots.index(root)
            elif root != root_:
                roots.append(root)
                x+=1
                root_ = root
            
            if dirnames != []:
                empty = False
            else:
                empty = True
            
            
            walk.append({'x':x,'obj':nombre,'empty':empty,'path':dirname,'hijos':dirnames})
            
        return walk
    
    def scroll(self,dy):
        pass
    
    def update(self):
        item = self.arbol.ItemActual
        if item != '':
            self.CarpetaSeleccionada = item
        self.dirty = 1

class listaDeArchivos(Marco):
    layer = 4
    SeleccionMultiple = False
    UltimaSeleccion = ''
    def __init__(self,parent,x,y,w,h,permitirmultiple=False,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        self.nombre = parent.nombre+'.ListaDeArchivos'
        super().__init__(x,y,w,h,False,**opciones)
        self.ScrollY = ScrollV(self,self.x+self.w-16,self.y)
        self.agregar(self.ScrollY,self.layer+1)
        self.items = LayeredDirty()
        self.Seleccionados = []
        self.SeleccionMultiple = permitirmultiple
        self.doc_h = h
        
    @staticmethod
    def _FiltrarExtS(archivos,extension):
        if extension != '':
            filtrado = []
            for archivo in archivos:
                if extension != '':
                    split = archivo[0].split('.')
                    ext = split[-1]
                    if ext == extension:
                        filtrado.append(archivo)    
            return filtrado         
        else:
            return archivos
    
    @staticmethod
    def _listar_archivos(fold):
        lista = []
        for item in os.listdir(fold):
            if os.path.isfile(os.path.join(fold,item)):
                lista.append([item,os.path.join(fold,item)])
        return lista
    
    def crearLista(self,opciones,ext):
        m = self.SeleccionMultiple
        lista = self._FiltrarExtS(opciones,ext)
        h = 0
        for n in range(len(lista)):
            nom = lista[n][0]
            ruta = lista[n][1]
            dy = self.y+(n*h)
            opcion = _Opcion(self,nom,ruta,self.x,dy,self.w-16,multi=m)
            h = opcion.image.get_height()
            self.items.add(opcion)
            if self.rect.contains(opcion.rect):
                self.agregar(opcion,self.layer+1)
       
    def borrarLista(self):
        for item in self.items:
            self.items.remove(item)
            if item in self:
                self.quitar(item)
    
    def scroll(self,dy=0):
        pass
    
    def actualizarLista(self,carpeta,tipo):
        self.borrarLista()
        nuevalista = self._listar_archivos(carpeta)
        self.crearLista(nuevalista,tipo)

    def onMouseDown(self,button):
        if self.ScrollY.enabled:
            if button == 5:
                self.ScrollY.moverCursor(dy=+10)
            if button == 4:
                self.ScrollY.moverCursor(dy=-10)
                
    def update(self):
        for item in self.items:
            if item.isSelected:
                self.UltimaSeleccion = item.texto
                if item.texto not in self.Seleccionados:
                    self.Seleccionados.append(item.texto)
                    if not self.SeleccionMultiple:
                        break
        self.dirty = 1

class _Opcion(BaseOpcion):
    isSelected = False
    texto = ''
    MultipleSelection  = False
    def __init__(self,parent,nombre,ruta,x,y,w=0,multi=False,**opciones):
        super().__init__(parent,nombre,x,y,w)
        self.texto = nombre
        self.tooltip = ToolTip(self,ruta,x,y)
        self.MultipleSelection = multi
       
    def onFocusIn(self):
        super().onFocusIn()
        self.image = self.img_sel
        self.isSelected = True
            
    def onFocusOut(self):
        super().onFocusOut()
        mods = key.get_mods()
        if not (mods & KMOD_LCTRL or mods & KMOD_RCTRL) or not self.MultipleSelection:
            self.image = self.img_des
            self.isSelected = False
    
    def update(self):
        if self.hasMouseOver:
            self.tooltip.show()
        else:
            self.tooltip.hide()