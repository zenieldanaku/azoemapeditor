from widgets import Menu,subVentana, CuadroTexto
from globales import C

class Menu_Prueba (Menu):
    def  __init__(self,parent,x,y):
        opciones = [{'nom':'Prueba','win':CuadroPrueba}]
        super().__init__(parent,'Prueba',opciones,x,y)

class CuadroPrueba(subVentana):
    def __init__(self):
        self.nombre = 'Cuadro Prueba'
        super().__init__(1*C,1*C,18*C,16*C,self.nombre)
        self.cuadro = CuadroTexto(self,self.x+C,self.y+32,self.w-C*2,self.h-C*2+16)
        self.agregar(self.cuadro,self.layer+1)