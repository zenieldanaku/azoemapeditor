from globales import Sistema as Sys
from widgets import Menu, FileDiag
from .menu_mapa import CuadroMapa

class Menu_Archivo(Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu.Archivo'
        self.barra = barra
        n,w,c,s,k = 'nom','win','cmd','csc','key'
        
        cascadas = {
            'exportar':[
                {n:'Colisiones',w:lambda:FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.GuardarMapaDeColisiones},carpeta_actual=Sys.fdExport)},
                {n:'Mapa',w:lambda:FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.exportarMapa},carpeta_actual=Sys.fdExport)}]}
        opciones = [
            {n:'Nuevo',c:lambda:CuadroMapa('Nuevo Mapa'),"icon":Sys.iconos['nuevo'],k:'Ctrl+N'},
            {n:'Abrir',w:lambda:FileDiag({'scr':'Aceptar','tipo':'A','cmd':Sys.abrirProyecto},filetypes=['.json'],carpeta_actual=Sys.fdProyectos),"icon":Sys.iconos['abrir'],k:'Ctrl+A'},
            {n:'Guardar',c:self.Guardar,"icon":Sys.iconos['guardar'],k:'Ctrl+S'},
            {n:'Guardar como',w:lambda:FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.guardarProyecto},carpeta_actual=Sys.fdProyectos)},
            {n:'Exportar',s:cascadas['exportar']},
            {n:'Cerrar',c:Sys.cerrarProyecto,k:'Ctrl+Q'},
            {n:'Salir',c:Sys.salir,k:'Esc'}]
        super().__init__('Archivo',opciones,x,y)
    
    @staticmethod
    def Guardar():
        if not Sys.Guardado:
            FileDiag({'scr':'Guardar','tipo':'G','cmd':Sys.guardarProyecto},Sys.fdProyectos)
        else:
            Sys.guardarProyecto(Sys.Guardado)