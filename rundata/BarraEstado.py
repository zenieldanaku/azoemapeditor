from azoe.engine import EventHandler, color
from globales import Sistema as Sys, C
from azoe.widgets import Marco, Label
from pygame import Rect, display


class BarraEstado(Marco):
    _estado = ''
    lblEstado = None
    # layer = 1

    def __init__(self):
        self.nombre = 'BarraEstado'
        super().__init__(0, 16 * C + 19, display.get_surface().get_width(), 26)

        self._estado = ''
        self.lblEstado = Label(self, 'Estado', self.x + 4, self.y + 3)
        EventHandler.add_widgets(self.lblEstado)

    def mostrar_estado(self, mensaje):
        if mensaje != self._estado:
            self._estado = mensaje
            self.lblEstado.set_text(mensaje)

    def update(self):
        self.mostrar_estado(Sys.estado)
