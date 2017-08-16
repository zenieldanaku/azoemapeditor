from azoe.widgets import Menu
from globales import Sistema as Sys


class MenuArchivo(Menu):
    def __init__(self, parent, x, y):
        # aliases
        n, w, c, s, k, i = 'nom', 'win', 'cmd', 'csc', 'key', 'icon'
        icons = Sys.iconos
        binded = Sys.binded_methods
        save = Sys.save_project
        # otherwise, line's too long
        items = [
            {n: 'Nuevo', w: Sys.new_project, "icon": icons['nuevo'], k: binded['new_project']},
            {n: 'Abrir', w: Sys.open_project, i: icons['abrir'], k: binded['open_project']},
            {n: 'Guardar', c: lambda: save(Sys.Guardado), i: icons['guardar'], k: binded['save_project']},
            {n: 'Guardar como', w: Sys.save_project_as, k: binded['save_project_as']},
            {n: 'Exportar', s: [{n: 'Colisiones', w: Sys.save_collition_map}, {n: 'Mapa', w: Sys.exportar_mapa}]},
            {n: 'Cerrar', c: Sys.close_project, k: binded['close_project']},
            {n: 'Salir', c: Sys.exit, k: binded['exit']}]

        super().__init__(parent, 'Archivo', items, x, y)

    def update(self):
        nombres = ['Guardar', 'Guardar como', 'Cerrar', 'Exportar']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO is None:
                objeto.ser_deshabilitado()
            elif not objeto.enabled:
                objeto.ser_habilitado()
