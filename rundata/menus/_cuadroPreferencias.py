from widgets import subVentana, Label, Entry, Boton
from globales import C, GLOBALES
from renderer import Renderer

class cuadroPreferencias (subVentana):    
    def __init__(self):
        self.nombre = 'Preferencias'
        super().__init__(2*C+8,3*C,16*C,10*C+18)
        dx,dy,dw,dh = self.x,self.y,self.w,self.h
        self.lblModFolder = Label(self,'ModFolder',dx+2,dy+19,'ModFolder')
        self.entryModFolder = Entry(self,'ModFolder',dx+80,dy+19,100)
        self.btnAceptar = Boton(self,dx+dw-150,dy+dh-28,'Aceptar',self.Aceptar,'Aceptar')
        self.btnCancelar = Boton(self,dx+dw-80,dy+dh-28,'Cancelar',self.cerrar,'Cancelar')
        
        self.agregar(self.lblModFolder)
        self.agregar(self.entryModFolder)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
    
    def Aceptar(self):
        GLOBALES.preferencias['ModFolder'] = self.entryModFolder.devolver_texto()
        self.cerrar()
    
    def cerrar(self):
        Renderer.delWidget(self)
