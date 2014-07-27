from globales import Sistema as Sys, C, EventHandler
from widgets import Menu, FileDiag, subVentana, Label, Entry, Boton

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Mapa'
        self.barra = barra
        cascadas = {'imagen':[
                {'nom':'Fondo','win':lambda:FileDiag({'scr':'Abrir','tipo':'A','cmd':Sys.setRutaFondo},Sys.fdAssets)},
                {'nom':'Colisiones','win':lambda:FileDiag({'scr':'Abrir','tipo':'A','cmd':Sys.setRutaColis},Sys.fdAssets)}]}
        opciones = [{'nom':'Imagen','csc':cascadas['imagen']},
                    {'nom':'Ajustes','win':lambda:CuadroMapa('Ajustar Mapa')}]
        super().__init__('Mapa',opciones,x,y)

class CuadroMapa(subVentana):
    value = False
    labels = []
    entrys = []
    def __init__(self,nombre):
        self.nombre = 'Nuevo Mapa'
        super().__init__(4*C+16,6*C,11*C,4*C+12,nombre)
        x,y,w,h = self.x,self.y,self.w,self.h
        ops = {'fontType':'Tahoma','fontSize':12}
        dx,dy,dw = 210,23,214
        
        self.btnAceptar = Boton(self,x+w-142,y+h-26,'Aceptar',self.Aceptar,'Aceptar',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        self.btnCancelar = Boton(self,x+w-72,y+h-26,'Cancelar',self.cerrar,'Cancelar',**{'fontType':'Tahoma','fontSize':14,'w':68,'h':20})
        
        self.labels.append(Label(self,'Fondo',x+2,y+dy*1,'Carpeta de imágenes fondo:',**ops))
        self.labels.append(Label(self,'Colisiones',x+2,y+dy*2,'Carpeta de mapas de colisiones:',**ops))
        self.labels.append(Label(self,'Props',x+2,y+dy*3,'Ruta de archivo de datos para Props:',**ops))
        self.labels.append(Label(self,'Mobs',x+2,y+dy*4,'Ruta de archivo de datos para Mobs:',**ops))       
        
        self.entrys.append(Entry(self,'Fondo',x+dx,y-3+dy*1,w-dw,'maps/fondos/'))
        self.entrys.append(Entry(self,'Colisiones',x+dx,y-3+dy*2,w-dw,'maps/colisiones/'))
        self.entrys.append(Entry(self,'Props',x+dx,y-3+dy*3,w-dw,'props/'))
        self.entrys.append(Entry(self,'Mobs',x+dx,y-3+dy*4,w-dw,'mobs/'))
        
        for label in self.labels:
            self.agregar(label)
        for entry in self.entrys:
            self.agregar(entry)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
    
    def Aceptar(self):
        data = {}
        for entry in self.entrys:
            data[entry._nombre.lower()] = entry.devolver_texto()
        Sys.nuevoProyecto(data)
        self.cerrar()
    
    def cerrar(self):
        EventHandler.delWidget(self)