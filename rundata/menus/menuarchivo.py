from azoe.widgets import Menu, FileOpenDialog as Fo, FileSaveDialog as Fs
from globales import Sistema as Sys
from .menumapa import CuadroMapa


class MenuArchivo(Menu):
    def __init__(self, parent, x, y, **opciones):
        n, w, c, s, k, i = 'nom', 'win', 'cmd', 'csc', 'key', 'icon'
        incons = Sys.iconos
        cascadas = {
            'exportar': [
                {n: 'Colisiones', w: lambda: Fs(Sys.save_collition_map, Sys.fdExport, ft=['*.png'], **opciones)},
                {n: 'Mapa', w: lambda: Fs(Sys.exportar_mapa, Sys.fdExport, ft=['*.json'], **opciones)}
            ],
        }
        items = [
            {n: 'Nuevo', c: lambda: CuadroMapa('Nuevo Mapa', **opciones), "icon": Sys.iconos['nuevo'], k: 'Ctrl+N'},
            {n: 'Abrir', w: lambda: Fo(Sys.open_proyect, Sys.fdProyectos, ft=['.json'], **opciones), i: incons['abrir'],
             k: 'Ctrl+A'},
            {n: 'Guardar', c: lambda: Sys.save_proyect(Sys.Guardado, **opciones), i: Sys.iconos['guardar'], k: 'Ctrl+S'},
            {n: 'Guardar como', c: lambda: Sys.save_proyect(**opciones), k: 'Ctrl+Alt+S'},
            {n: 'Exportar', s: cascadas['exportar']},
            {n: 'Cerrar', c: Sys.close_proyect, k: 'Ctrl+Q'},
            {n: 'Salir', c: Sys.salir, k: 'Esc'}]

        super().__init__(parent, 'Archivo', items, x, y, **opciones)

    # @staticmethod
    # def guardar():
    #     if not Sys.Guardado:
    #         Fs(Sys.save_proyect, Sys.fdProyectos, ft=['*.json'], **opciones)
    #     else:
    #         Sys.save_proyect(Sys.Guardado)

    def update(self):
        nombres = ['Guardar', 'Guardar como', 'Cerrar', 'Exportar']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO is None:
                objeto.ser_deshabilitado()
            elif not objeto.enabled:
                objeto.ser_habilitado()
