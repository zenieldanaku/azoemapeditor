from widgets import subVentana, Label, Entry, BotonAceptarCancelar, DataGrid, ScrollV
from globales import C, Sistema
from pygame import Rect

class CuadroEntrada(subVentana):
    def __init__(self,**opciones):
        super().__init__(6*C+16,8*C-8,'Entradas',**opciones)
        DX = 18
        self.grid = DataGrid(self,'datos',self.x+3+DX,self.y+23+15,{},
                             titulos=['Nombre','X','Y'],cel_w=53,n_fil=9,sep=2)
        ops = {'fontType':'Tahoma','fontSize':12}
        Nombre = Label(self,'nmbr',self.x+9+DX,self.y+23,'Nombre',**ops)
        lblPosX = Label(self,'PosX',self.x+C*2+16+DX,self.y+23,'X',**ops)
        lblPosY = Label(self,'PosY',self.x+C*4+6+DX,self.y+23,'Y',**ops)
        self.agregar(Nombre)
        self.agregar(lblPosX)
        self.agregar(lblPosY)
        
        sort = sorted([nombre for nombre in Sistema.PROYECTO.script['entradas']])
        relleno = []
        for nombre in sort:
            x = Sistema.PROYECTO.script['entradas'][nombre]['x']
            y = Sistema.PROYECTO.script['entradas'][nombre]['y']
            relleno.append([nombre,x,y])
        
        self.grid.rellenar(relleno)
        
        scroll = ScrollV(self.grid,self.x+self.w-16-4,self.y+20+19)
        self.agregar(scroll)
    
    def onDestruction(self):
        super().onDestruction()
        self.grid.onDestruction()

class UnaEntrada(subVentana):
    entrada_nombre = ''
    entrada_px = 0
    entrada_py = 0
    
    def __init__(self,px,py):
        super().__init__(4*C+16,C*3-2,'Insertar Entrada')
        ops = {'fontType':'Tahoma','fontSize':12}
        
        self.lblNombre = Label(self,'nmbr',self.x+3,self.y+23,'Nombre',**ops)
        self.lblPosX = Label(self,'PosX',self.x+3,self.y+23+23,'X',**ops)
        self.lblPosY = Label(self,'PosY',self.x+C*2+9,self.y+23+23,'Y',**ops)
        
        self.entryNombre = Entry(self,'nmbr',self.x+C*2+9,self.y+20,68)
        self.entryPosX = Entry(self,'PosX',self.x+3+10,self.y+20+23,C+26,texto=str(px))
        self.entryPosY = Entry(self,'PosY',self.x+C*2+9+10,self.y+20+23,C+26,texto=str(py))
        
        self.btnAceptar = BotonAceptarCancelar(self,self.x+3,self.y+70,self.aceptar)
        self.btnCancelar = BotonAceptarCancelar(self,self.x+C*2+9,self.y+70)
        
        self.agregar(self.lblNombre)
        self.agregar(self.lblPosX)
        self.agregar(self.lblPosY)
        
        self.agregar(self.entryNombre)
        self.agregar(self.entryPosY)
        self.agregar(self.entryPosX)
        
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
        
        self.btnAceptar.serDeshabilitado()
        
    def aceptar(self):
        Sistema.PROYECTO.addEntrada(self.entrada_nombre,self.entrada_px,self.entrada_py)
        self.cerrar()
        
    def update(self):
        self.entrada_nombre = self.entryNombre.devolver_texto()
        self.entrada_px = self.entryPosX.devolver_texto()
        self.entrada_py = self.entryPosY.devolver_texto()
        
        if self.entrada_nombre != '':
            self.btnAceptar.serHabilitado()
        else:
            self.btnAceptar.serDeshabilitado()