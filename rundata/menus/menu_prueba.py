from azoe.widgets import Menu,subVentana, CuadroTexto, ScrollH,ScrollV
from globales import C

class Menu_Prueba (Menu):
    def  __init__(self,parent,x,y):
        opciones = [{'nom':'Prueba','win':CuadroPrueba}]
        super().__init__(parent,'Prueba',opciones,x,y)

class CuadroPrueba(subVentana):
    layer = 9
    def __init__(self):
        self.nombre = 'Cuadro Prueba'
        super().__init__(10*C,14*C,self.nombre)
        
        self.cuadro = CuadroTexto(self,self.x+2,self.y+22,self.w-19,self.h-42)
        self.scrX = ScrollH(self.cuadro,self.cuadro.x,self.cuadro.y+self.cuadro.h+2)
        self.scrY = ScrollV(self.cuadro,self.x+self.cuadro.w+2,self.cuadro.y)
        self.agregar(self.cuadro)
        self.agregar(self.scrX)