from globales import Sistema as Sys, C, EventHandler
from widgets import Menu, FileDiag, subVentana, Label, Entry, BotonAceptarCancelar

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Mapa'
        self.barra = barra
        cascadas = {'imagen':[
                {'nom':'Fondo','icon':Sys.iconos['fondo'],
                 'win':lambda:FileDiag({'scr':'Abrir','tipo':'A','cmd':Sys.setRutaFondo},carpeta_actual=Sys.fdAssets)},
                #{'nom':'Colisiones','win':lambda:FileDiag({'scr':'Abrir','tipo':'A','cmd':Sys.setRutaColis},Sys.fdAssets)}
                ]}
        opciones = [{'nom':'Imagen','csc':cascadas['imagen']},
                    {'nom':'Ajustes','win':lambda:CuadroMapa('Ajustar Mapa')}]
        super().__init__('Mapa',opciones,x,y)
    
    def update(self):
        nombres = ['Ajustes','Fondo']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO is None:
                objeto.serDeshabilitado()
            elif not objeto.enabled:
                objeto.serHabilitado()

class CuadroMapa(subVentana):
    value = False
    labels = []
    entrys = []
    def __init__(self,nombre):
        self.nombre = 'Nuevo Mapa'
        super().__init__(11*C,5*C+2,nombre)
        x,y,w,h = self.x,self.y,self.w,self.h
        ops = {'fontType':'Tahoma','fontSize':12}
        dx,dy,dw = 210,23,214
        
        self.btnAceptar = BotonAceptarCancelar(self,x+w-142,y+h-26,self.Aceptar)
        self.btnCancelar = BotonAceptarCancelar(self,x+w-72,y+h-26)
        items = {}
        lista = [['Fondo','Carpeta de imágenes fondo:','maps/fondos/'],
                ['Colisiones','Carpeta de mapas de colisiones:','maps/colisiones/'],
                ['Props','Ruta de archivo de datos para Props:','props/'],
                ['Mobs','Ruta de archivo de datos para Mobs:','mobs/'],
                ['Ambiente','Ambiente (Exterior/Interior):','exterior']]
        for i in range(len(lista)):
            nombre,txt,ref = lista[i]
            j = i+1
            if Sys.referencias[nombre.lower()] is not None:
                ref = Sys.referencias[nombre.lower()]
            items[nombre] = {
                'label':[nombre,x+2,y+dy*j,txt],
                'entry':[nombre,x+dx,y-3+dy*j,w-dw,ref]
                }
        
        for nombre in items:
            label = Label(self,*items[nombre]['label'],**ops)
            entry = Entry(self,*items[nombre]['entry'])
            self.labels.append(label)
            self.entrys.append(entry)
            self.agregar(label)
            self.agregar(entry)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
    
    def Aceptar(self):
        data = {}
        for entry in self.entrys:
            data[entry._nombre.lower()] = entry.devolver_texto()
        
        if Sys.PROYECTO is None:
            Sys.nuevoProyecto(data)
        else:
            Sys.referencias.update(data)
            
        self.cerrar()
    
    def cerrar(self):
        EventHandler.delWidget(self)
