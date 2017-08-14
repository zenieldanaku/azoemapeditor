from azoe.widgets import Menu, FileOpenDialog as Fo, SubVentana, Label, Entry, BotonAceptarCancelar
from globales import Sistema as Sys, C
from azoe.engine import EventHandler


class MenuMapa(Menu):
    def __init__(self, parent, x, y):
        cascadas = {'imagen': [
            {'nom': 'Fondo', 'icon': Sys.iconos['fondo'], 'win': lambda: Fo(Sys.set_ruta_fondo, Sys.fdAssets)}]}
        opciones = [{'nom': 'Imagen', 'csc': cascadas['imagen']},
                    {'nom': 'Ajustes', 'win': lambda: CuadroMapa('Ajustar Mapa')}]
        super().__init__(parent, 'Mapa', opciones, x, y)

    def update(self):
        nombres = ['Ajustes', 'Fondo']
        for n in nombres:
            objeto = self.referencias[n]
            if Sys.PROYECTO is None:
                objeto.ser_deshabilitado()
            elif not objeto.enabled:
                objeto.ser_habilitado()


class CuadroMapa(SubVentana):
    value = False
    labels = []
    entrys = []
    # layer = 8

    def __init__(self, nombre):
        self.nombre = 'Nuevo Mapa'
        super().__init__(11 * C, 5 * C + 2, nombre)
        x, y, w, h = self.x, self.y, self.w, self.h
        ops = {'fontType': 'Tahoma', 'fontSize': 12}
        dx, dy, dw = 210, 23, 214

        self.btnAceptar = BotonAceptarCancelar(self, x + w - 142, y + h - 26, self.aceptar)
        self.btnCancelar = BotonAceptarCancelar(self, x + w - 72, y + h - 26)
        items = {}
        lista = [['Fondo', 'Carpeta de imágenes fondo:', 'maps/fondos/'],
                 ['Colisiones', 'Carpeta de mapas de colisiones:', 'maps/colisiones/'],
                 ['Props', 'Ruta de archivo de datos para Props:', 'props/'],
                 ['Mobs', 'Ruta de archivo de datos para Mobs:', 'mobs/'],
                 ['Ambiente', 'Ambiente (Exterior/Interior):', 'exterior']]
        for i in range(len(lista)):
            nombre, txt, ref = lista[i]
            j = i + 1
            if Sys.referencias[nombre.lower()] is not None:
                ref = Sys.referencias[nombre.lower()]
            items[nombre] = {
                'label': [nombre, x + 2, y + dy * j, txt],
                'entry': [nombre, x + dx, y - 3 + dy * j, w - dw, ref]
            }

        for nombre in items:
            label = Label(self, *items[nombre]['label'], **ops)
            entry = Entry(self, *items[nombre]['entry'])
            self.labels.append(label)
            self.entrys.append(entry)
            self.agregar(label)
            self.agregar(entry)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)

    def aceptar(self):
        data = {}
        for entry in self.entrys:
            data[entry.get_real_name().lower()] = entry.return_text()

        if Sys.PROYECTO is None:
            Sys.new_proyect(data)
        else:
            Sys.referencias.update(data)

        self.cerrar()

    def cerrar(self):
        EventHandler.del_widgets(self)
