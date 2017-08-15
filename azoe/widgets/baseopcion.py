from . import BaseWidget
from pygame import font, Rect, Surface
from azoe.engine import color


class BaseOpcion(BaseWidget):
    def __init__(self, parent, nombre, x, y, w=0, **opciones):
        super().__init__(parent, **opciones)
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + '.Opcion:' + nombre
        txt = color(opciones.get('colorTexto', 'sysElmText'))
        fnd = color(opciones.get('FondoMenus', 'sysMenBack'))
        sel = color(opciones.get('colorSelect', 'sysBoxSelBack'))

        self.img_des = self.crear(nombre, txt, fnd, w)
        self.img_sel = self.crear(nombre, txt, sel, w)
        self.image = self.img_des
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def crear(self, nombre, fgcolor, bgcolor, w=0):
        if 'Fuente' not in self.opciones:
            self.opciones['fontType'] = 'Courier new'
        if 'fontSize' not in self.opciones:
            self.opciones['fontSize'] = 14

        fuente = font.SysFont(self.opciones['fontType'], self.opciones['fontSize'])
        if w == 0:
            w, h = fuente.size(nombre)
        else:
            h = fuente.get_height()

        rect = Rect(0, 0, w, h)
        render = fuente.render(nombre, True, fgcolor, bgcolor)
        image = Surface(rect.size)
        image.fill(bgcolor)
        image.blit(render, rect)

        return image

    def set_text(self, text):
        txt = color(self.opciones.get('colorTexto', 'sysElmText'))
        fnd = color(self.opciones.get('FondoMenus', 'sysMenBack'))
        sel = color(self.opciones.get('colorSelect', 'sysBoxSelBack'))

        self.nombre = self.parent.nombre + '.Opcion.' + text
        self.img_des = self.crear(text, txt, fnd, self.w)
        self.img_sel = self.crear(text, txt, sel, self.w)
        self.image = self.img_des
        self.dirty = 1
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
