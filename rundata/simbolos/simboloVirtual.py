from globales import Sistema as Sys
from azoe import EventHandler
from .simboloBase import SimboloBase
from pygame import mouse
from azoe.widgets import Alerta


class SimboloVirtual(SimboloBase):
    copiar = False

    def __init__(self, parent, imagen, pos, data):
        x, y, z = pos
        rot = 0
        if 'rot' in data:
            rot = data['rot']
        _rect = imagen.get_rect(center=(x, y))
        self.datos = data
        data = {'nombre': 'Virtual',
                'image': imagen, 'pos': [_rect.x, _rect.y, z, rot]}

        super().__init__(parent, data)
        self.image = self._crear_transparencia(self._imagen)
        if self.nombre not in EventHandler.widgets:
            EventHandler.add_widgets(self)
        self.pressed = True

    def on_mouse_out(self):
        if not self.pressed:
            super().on_mouse_out()

    def on_mouse_over(self):
        if self.pressed:
            x, y = mouse.get_pos()
            self.rect.center = (x, y)

    def on_mouse_up(self, button):
        self.pressed = False
        self.x, self.y = mouse.get_pos()
        if self.datos['colisiones'] is None:
            texto = 'El símbolo ' + self.datos['nombre'] + ' '
            texto += 'carece de un mapa de colisiones.\n¿Desea continuar de todos modos?'
            borrar = lambda: EventHandler.del_widgets(self)

            if NoColitionAlert.repeat(texto, self.copy, borrar):
                self.copiar = True

    def copy(self):
        x, y = self.x, self.y
        widget = EventHandler.get_widget('Grilla.Canvas')
        if widget.rect.collidepoint((x, y)):
            self.datos['rect'] = self.rect.copy()
            self.datos['original'] = True
            widget.colocar_tile(self.datos)
            EventHandler.del_widgets(self)

    def update(self):
        if self.pressed:
            self.dirty = 1
        elif self.copiar:
            self.copy()


class NoColitionAlert(Alerta):
    @classmethod
    def repeat(cls, texto, accion_si, accion_no):
        if 'NoColition' in Sys.DiagBoxes_repeat:
            if not Sys.DiagBoxes_repeat['NoColition']:
                Sys.DiagBox = NoColitionAlert(texto, accion_si, accion_no)
            else:
                return True
        else:
            Sys.DiagBox = NoColitionAlert(texto, accion_si, accion_no)

    def __init__(self, texto, accion_si, accion_no):
        super().__init__('NoColition', texto, accion_si, accion_no)
