from . import BaseWidget,Marco, Entry, Boton, DropDownList
from . import Label, ScrollV, ScrollH, Tree, BaseOpcion
from pygame import Rect, font, Surface, mouse
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect
from renderer import Renderer
from constantes import *
from colores import color
import os, os.path

class FileDiag(Marco):
    x,y,w,h = 0,0,0,0
    pressed = False
    carpetaActual = ''
    archivoActual = ''
    nombredeArchivo = ''
    tipoSeleccinado = ''
    def __init__(self,comando,**opciones):      
        self.nombre = 'FileDiag'
        super().__init__(5*C,5*C,16*C,10*C+18,**opciones)
        self.titular(self.nombre)
        self.comando = comando['cmd']
        self.TipoComando = comando['tipo']
        dummyList = ['*.png','*.json','*.mob','*.quest']
        self.carpetas = arbolCarpetas(self,self.x+2,self.y+19,self.w//2-2,8*C)
        self.archivos = listaDeArchivos(self,self.x+self.w//2,self.y+19,self.w//2-2,8*C)
        self.entryNombre = Entry(self,'IngresarRuta',self.x+2*C+3,self.y+8*C+23,12*C+25,'')
        self.BtnAccion = Boton(self,self.x+14*C+32,self.y+8*C+21,'Accion',self.ejecutar_comando,comando['scr'])
        self.tipos = DropDownList(self,'TipoDeArchivo',self.x+2*C+3,self.y+9*C+19,12*C+25,dummyList)
        self.BtnCancelar = Boton(self,self.x+15*C,self.y+9*C+15,'Cancelar',self.cerrar_ventana,'C')
        self.lblTipo = Label(self,'Tipo',self.x+4,self.y+9*C+18,texto = "Tipo:")
        self.lblNombre = Label(self,'Nombre',self.x+4,self.y+8*C+24, texto = 'Nombre:')    
        
        self.agregar(self.carpetas)
        self.agregar(self.archivos)
        self.agregar(self.entryNombre)
        self.agregar(self.BtnAccion)
        self.agregar(self.tipos)
        self.agregar(self.BtnCancelar)
        self.agregar(self.lblTipo)
        self.agregar(self.lblNombre)
    
    def titular(self,texto):
        fuente = font.SysFont('verdana',12)
        rect = Rect(2,2,self.w-4,fuente.get_height()+1)
        render = render_textrect(texto,fuente,rect,(255,255,255),(0,0,0))
        self.image.blit(render,rect)
    
    def ejecutar_comando(self):
        if self.TipoComando == 'A':
            ruta = os.path.join(self.carpetaActual,self.archivoActual)
        elif self.TipoComando == 'G':
            if self.tipoSeleccinado != '':
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo+self.tipoSeleccinado)
            else:
                ruta = os.path.join(self.carpetaActual,self.nombredeArchivo)
        
        self.comando(ruta)
        self.cerrar_ventana()
    
    def cerrar_ventana(self):
        Renderer.delWidget(self)
          
    @staticmethod
    def listar_archivos(fold):
        lista = []
        for item in os.listdir(fold):
            if os.path.isfile(os.path.join(fold,item)):
                lista.append(item)
        return lista
    
    def update(self):
        tipo = self.tipos.ItemActual.lstrip('*')
        carpeta = self.carpetas.CarpetaSeleccionada
        nombre = self.entryNombre.devolver_texto()
        if carpeta != '':
            self.carpetaActual = carpeta
            self.archivos.borrarLista()
            lista_de_archivos = self.listar_archivos(carpeta)
            self.archivos.crearLista(lista_de_archivos,tipo.lstrip('.'))
            
        if self.archivos.ArchivoActual != '':
            self.archivoActual = self.archivos.ArchivoActual
        
        if nombre != '':
            self.nombredeArchivo = nombre
        
        if tipo != '':
            self.tipoSeleccinado = tipo
            
        self.dirty = 1

class arbolCarpetas(Marco):
    CarpetaSeleccionada = ''
    def __init__(self,parent,x,y,w,h,**opciones):
        self.nombre = parent.nombre+'.ArbolDeCarpetas'
        super().__init__(x,y,w,h,False,**opciones)
        self.focusable = False
        self.arbol = Tree(self,self.x,self.y,self.w-16,self.h,self.generar_arbol(os.getcwd()))
        self.ScrollY = ScrollV(self.arbol,self.x+self.w-16,self.y,self.h)
        self.agregar(self.ScrollY)
        self.agregar(self.arbol)
        self.CarpetaSeleccionada = ''
    
    @staticmethod #decorator! ^^ 'cause explicit is better than implicit
    def generar_arbol(path):
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
    def __init__(self,parent,x,y,w,h,**opciones):
        self.nombre = parent.nombre+'.ListaDeArchivos'
        super().__init__(x,y,w,h,False,**opciones)
        self.image.fill(color('sysMenBack'))
        self.ScrollY = ScrollV(self,self.x+self.w-16,self.y,self.h)
        self.agregar(self.ScrollY)
        self.items = LayeredDirty()
        self.ArchivoActual = ''
    
    @staticmethod
    def FiltrarExtS(archivos,extension):
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

    def crearLista(self,opciones,ext):
        lista = self.FiltrarExtS(opciones,ext)
        h = 0
        for n in range(len(lista)):
            nom = lista[n]
            dy = self.y+(n*h)
            opcion = _Opcion(self,nom,self.x,dy,self.w-16)
            h = opcion.image.get_height()
            self.items.add(opcion)
            self.agregar(opcion)
       
    def borrarLista(self):
        for item in self.items:
            self.items.remove(item)
            self.quitar(item)
    
    def scroll(self,dy):
        pass
    
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

