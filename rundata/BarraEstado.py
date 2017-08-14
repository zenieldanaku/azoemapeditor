from azoe.engine import EventHandler, color
from globales import Sistema as Sys, C
from azoe.widgets import Marco, Label
from pygame import Rect, display


class BarraEstado(Marco):
    _estado = ''
    lblEstado = None
    # layer = 1

    def __init__(self, **opciones):
        self.nombre = 'BarraEstado'
        super().__init__(0, 16 * C + 19, display.get_surface().get_width(), 26, **opciones)

        self._estado = ''
        self.lblEstado = Label(self, 'Estado', self.x + 4, self.y + 3)
        self.draw_area = Rect(4, 3, self.w - 8, self.h - 8)
        EventHandler.add_widgets(self.lblEstado)

    def mostrar_estado(self, mensaje):
        bgcolor = color(self.opciones.get('colorFondo', 'sysElmFace'))
        if mensaje != self._estado:
            self._estado = mensaje
            self.image.fill(bgcolor, self.draw_area)
            self.lblEstado.set_text(mensaje)

    def update(self):
        msj = Sys.estado
        self.mostrar_estado(msj)
