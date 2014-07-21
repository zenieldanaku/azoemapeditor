from . import BaseWidget,Marco, Entry, Boton, DropDownList, subVentana
from . import Label, ScrollV, ScrollH, Tree, BaseOpcion
from pygame import Rect, font
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from globales import EventHandler, color, C
import os, os.path

class FileDiag(subVentana):
    pressed = False
    carpetaActual = ''
    archivoActual = ''
    nombredeArchivo = ''
    tipoSeleccinado = ''
    carpetaVieja = ''
    def __init__(self,comando,carpeta_actual=os.getcwd(),**opciones):      
        self.nombre = 'FileDiag'
        super().__init__(2*C+8,3*C,16*C,10*C+18,self.nombre,**opciones)
        self.comando = comando['cmd']
        self.TipoComando = comando['tipo']
        dummyList = ['*.png','*.json','*.mob','*.quest']
        x,y,w,h = self.x,self.y,self.w,self.h # abreviaturas de legibilidad
        self.carpetas = arbolCarpetas(self,x+2,y+19,w//2-2,8*C,carpeta_actual)
        self.archivos = listaDeArchivos(self,x+w//2,y+19,w//2-2,8*C)
        self.entryNombre = Entry(self,'IngresarRuta',x+2*C+3,y+8*C+23,11*C+16,'')
        self.BtnAccion = Boton(self,x+14*C-8,y+8*C+24,'Accion',self.ejecutar_comando,comando['scr'],**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.tipos = DropDownList(self,'TipoDeArchivo',x+2*C+3,y+9*C+19,11*C+16,dummyList)
        self.BtnCancelar = Boton(self,x+14*C-8,y+9*C+20,'Cancelar',lambda:EventHandler.delWidget(self),'Cancelar',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.lblTipo = Label(self,'Tipo',x+4,y+9*C+18,texto = "Tipo:",**{'fontType':'Tahoma','fontSize':12})
        self.lblNombre = Label(self,'Nombre',x+4,y+8*C+24, texto = 'Nombre:',**{'fontType':'Tahoma','fontSize':12})    
        
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
            ruta = os.path.join(self.carpetaActual,self.archivoActual)
        
        elif self.TipoComando == 'G':
            if self.tipoSeleccinado != '' and not self.nombredeArchivo.endswith(self.tipoSeleccinado):
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo+self.tipoSeleccinado)
            else:
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo)
        
        self.comando(ruta)
        EventHandler.delWidget(self)

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
            
        if self.archivos.ArchivoActual != '':
            self.archivoActual = self.archivos.ArchivoActual
            if self.nombredeArchivo == '':
                self.entryNombre.setText(self.archivoActual)
        
        self.dirty = 1

class arbolCarpetas(Marco):
    CarpetaSeleccionada = ''
    layer = 3
    def __init__(self,parent,x,y,w,h,carpeta_actual,**opciones):
        self.nombre = parent.nombre+'.ArbolDeCarpetas'
        super().__init__(x,y,w,h,False,**opciones)
        self.arbol = Tree(self,self.x,self.y,self.w-16,self.h,self._generar_arbol(os.getcwd()),carpeta_actual)
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
            if '.svn' in dirnames:
                dirnames.remove('.svn')
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
    layer = 3
    def __init__(self,parent,x,y,w,h,**opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        self.nombre = parent.nombre+'.ListaDeArchivos'
        super().__init__(x,y,w,h,False,**opciones)
        self.ScrollY = ScrollV(self,self.x+self.w-16,self.y)
        self.agregar(self.ScrollY,self.layer+1)
        self.items = LayeredDirty()
        self.ArchivoActual = ''
    
    @staticmethod
    def _FiltrarExtS(archivos,extension):
        if extension != '':
            filtrado = []
            for archivo in archivos:
                if extension != '':
                    split = archivo.split('.')
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
                lista.append(item)
        return lista
    
    def crearLista(self,opciones,ext):
        lista = self._FiltrarExtS(opciones,ext)
        h = 0
        for n in range(len(lista)):
            nom = lista[n]
            dy = self.y+(n*h)
            opcion = _Opcion(self,nom,self.x,dy,self.w-16)
            h = opcion.image.get_height()
            self.items.add(opcion)
            if self.rect.contains(opcion.rect):
                self.agregar(opcion)
       
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
                self.ArchivoActual = item.texto
        self.dirty = 1

class _Opcion(BaseOpcion):
    isSelected = False
    texto = ''
    
    def __init__(self,parent,nombre,x,y,w=0,**opciones):
        super().__init__(parent,nombre,x,y,w)
        self.texto = nombre
       
    def onFocusIn(self):
        super().onFocusIn()
        self.image = self.img_sel
        self.isSelected = True
            
    def onFocusOut(self):
        super().onFocusOut()
        self.image = self.img_des
        self.isSelected = False

