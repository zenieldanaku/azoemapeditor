from globales import Sistema as Sys
from widgets import Menu, FileDiag
from .menu_mapa import CuadroMapa

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Archivo'
        self.barra = barra
        opciones = [
            {'nom':'Nuevo','cmd':lambda:CuadroMapa('Nuevo Mapa')},
            {'nom':'Abrir',"win":lambda:FileDiag({'scr':'Aceptar','tipo':'A','cmd':Sys.abrirProyecto},Sys.fdProyectos)},
            {'nom':'Guardar','cmd':self.Guardar},
            {'nom':'Guardar como','win':lambda:FileDiag({'scr':'G','tipo':'G','cmd':Sys.guardarProyecto},Sys.fdProyectos)},
            {'nom':'Exportar','win':lambda:FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.exportarMapa},Sys.fdExport)},
            {'nom':'Cerrar','cmd':Sys.cerrarMapa},
            {'nom':'Salir','cmd':Sys.salir}]
        super().__init__('Archivo',opciones,x,y)
    
    @staticmethod
    def Guardar():
        if not Sys.Guardado:
            FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.guardarProyecto},Sys.fdProyectos)
        else:
            Sys.guardarProyecto(Sys.Guardado)