from azoe.widgets import SubVentana, Label, Entry, Boton
from azoe.engine import EventHandler
from globales import C, Sistema as Sys


class CuadroPreferencias(SubVentana):
    def __init__(self):
        super().__init__(16 * C, 10 * C + 18, 'Preferencias')
        dx, dy, dw, dh = self.x, self.y, self.w, self.h
        self.lblModFolder = Label(self, 'ModFolder', dx + 2, dy + 19, 'ModFolder')
        self.entryModFolder = Entry(self, 'ModFolder', dx + 80, dy + 19, 100)
        self.btnAceptar = Boton(self, dx + dw - 150, dy + dh - 28, 'aceptar', self.aceptar, 'aceptar')
        self.btnCancelar = Boton(self, dx + dw - 80, dy + dh - 28, 'Cancelar', self.cerrar, 'Cancelar')

        self.agregar(self.lblModFolder)
        self.agregar(self.entryModFolder)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)

    def aceptar(self):
        Sys.preferencias['ModFolder'] = self.entryModFolder.return_text()
        self.cerrar()

    def cerrar(self):
        EventHandler.del_widget(self)
