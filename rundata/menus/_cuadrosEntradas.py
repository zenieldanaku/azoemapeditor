from widgets import subVentana, ScrollV, Label, Entry, BotonAceptarCancelar
from globales import C, Sistema

class CuadroEntrada(subVentana):
    def __init__(self):    
        super().__init__(6*C,8*C,'Entradas')

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
        Sistema.addEntrada(self.entrada_nombre,self.entrada_px,self.entrada_py)
        self.cerrar()
        
    def update(self):
        self.entrada_nombre = self.entryNombre.devolver_texto()
        self.entrada_px = self.entryPosX.devolver_texto()
        self.entrada_py = self.entryPosY.devolver_texto()
        
        if self.entrada_nombre != '':
            self.btnAceptar.serHabilitado()
        else:
            self.btnAceptar.serDeshabilitado()