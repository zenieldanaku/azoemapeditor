from azoe.widgets import Menu, FileOpenDialog as Fo, FileSaveDialog as Fs
from globales import Sistema as Sys
from .menu_mapa import CuadroMapa


class Menu_Archivo(Menu):
    def __init__(self, parent, x, y):
        n, w, c, s, k, i = 'nom', 'win', 'cmd', 'csc', 'key', 'icon'
        incons = Sys.iconos
        cascadas = {
            'exportar': [
                {n: 'Colisiones', w: lambda: Fs(Sys.GuardarMapaDeColisiones, Sys.fdExport, ft=['*.png'], )},
                {n: 'Mapa', w: lambda: Fs(Sys.exportarMapa, Sys.fdExport, ft=['*.json'])}
            ],
        }
        opciones = [
            {n: 'Nuevo', c: lambda: CuadroMapa('Nuevo Mapa'), "icon": Sys.iconos['nuevo'], k: 'Ctrl+N'},
            {n: 'Abrir', w: lambda: Fo(Sys.abrirProyecto, Sys.fdProyectos, ft=['.json']), i: incons['abrir'],
             k: 'Ctrl+A'},
            {n: 'Guardar', c: self.Guardar, i: Sys.iconos['guardar'], k: 'Ctrl+S'},
            {n: 'Guardar como', w: lambda: Fs(Sys.guardarProyecto, Sys.fdProyectos, ft=['*.json']), k: 'Ctrl+Alt+S'},
            {n: 'Exportar', s: cascadas['exportar']},
            {n: 'Cerrar', c: Sys.cerrarProyecto, k: 'Ctrl+Q'},
            {n: 'Salir', c: Sys.salir, k: 'Esc'}]

        super().__init__(parent, 'Archivo', opciones, x, y)

    @staticmethod
    def Guardar():
        if not Sys.Guardado:
            Fs(Sys.guardarProyecto, Sys.fdProyectos, ft=['*.json'])
        else:
            Sys.guardarProyecto(Sys.Guardado)

    def update(self):
        nombres = ['Guardar', 'Guardar como', 'Cerrar', 'Exportar']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO == None:
                objeto.serDeshabilitado()
            elif not objeto.enabled:
                objeto.serHabilitado()
