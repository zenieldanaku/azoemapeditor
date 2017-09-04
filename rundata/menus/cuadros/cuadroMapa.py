from azoe.widgets import SubVentana, Label, Entry, BotonAceptarCancelar
from globales import Sistema as Sys, C
from pygame import font


class CuadroMapa(SubVentana):
    entries = []

    def __init__(self, nombre):
        self.nombre = 'Nuevo Mapa'
        super().__init__(11 * C, 4 * C + 10, nombre)
        x, y, w, h = self.x, self.y, self.w, self.h
        fuente = font.SysFont('Tahoma', 12)
        dx, dy, dw = 210, 23, 214

        self.btnAceptar = BotonAceptarCancelar(self, x + w - 142, y + h - 26, self.aceptar)
        self.btnCancelar = BotonAceptarCancelar(self, x + w - 72, y + h - 26)
        items = {}
        lista = [['Fondo', 'Carpeta de imágenes fondo:', 'maps/fondos/'],
                 ['Colisiones', 'Carpeta de mapas de colisiones:', 'maps/colisiones/'],
                 ['Props', 'Ruta de archivo de datos para Props:', 'props/'],
                 ['Mobs', 'Ruta de archivo de datos para Mobs:', 'mobs/']]

        for i, item in enumerate(lista, start=1):
            name, txt, ref = item
            if Sys.referencias[name.lower()] is not None:
                ref = Sys.referencias[nombre.lower()]
            items[name] = {
                'label': [name, x + 2, y + dy * i, txt],
                'entry': [name, x + dx, y - 3 + dy * i, w - dw, ref]
            }

        for name in items:
            l = items[name]['label']
            e = items[name]['entry']
            Label(self, *l[:3], texto=l[3], fuente=fuente)
            entry = Entry(self, *e[:3], w=e[3], texto=e[4])
            self.entries.append(entry)

    def aceptar(self):
        data = {}
        for entry in self.entries:
            data[entry.get_real_name().lower()] = entry.return_text()

        Sys.new_project(data)
        self.cerrar()
