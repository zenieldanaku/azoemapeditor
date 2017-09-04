from azoe.widgets import Menu, FileOpenDialog as Fo
from globales import Sistema as Sys
from .cuadros.cuadroMapa import CuadroMapa


class MenuMapa(Menu):
    def __init__(self, parent, x, y):
        n, w, c = 'nom', 'win', 'csc'
        lista = [{n: 'Fondo', 'icon': Sys.iconos['fondo'], w: lambda: Fo(Sys.set_ruta_fondo, Sys.fdAssets)},
                 {n: 'Ajustes', w: lambda: CuadroMapa('Ajustar Mapa')},
                 {n: 'Límites', w: lambda: None}
                 ]
        super().__init__(parent, 'Mapa', lista, x, y)

    def update(self):
        nombres = ['Fondo']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO is None:
                objeto.ser_deshabilitado()
            elif not objeto.enabled:
                objeto.ser_habilitado()
