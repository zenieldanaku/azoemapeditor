from pygame import Surface, Rect, font, draw, mouse
from azoe.widgets import BaseWidget, ToolTip
from ._guias import LineaGuiaX, LineaGuiaY
from azoe.engine import EventHandler
from globales import C


class BaseRegla(BaseWidget):
    pressed = False
    lineas = []  # list
    linea = None  # object
    fondo = None
    image = None
    clip = Rect(0, 0, 0, 0)
    tooltip = None
    newLine = False
    tip = 'Haga clic y arrastre para generar una guía' + ' '  # el espacio es intencional

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent)
        self.clip = Rect(0, 0, w, h)
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.lineas = []

    @staticmethod
    def crear(d):
        pass

    def mover_linea(self):
        pass

    def actualizar_tamanio(self, nuevotamanio):
        self.fondo = self.crear(nuevotamanio)
        self.image.blit(self.fondo, self.clip)
        self.dirty = 1

    def on_mouse_up(self, button):
        if button == 1 and self.enabled:
            self.pressed = False
            self.lineas.append(self.linea)
            self.linea = None

    def on_mouse_out(self):
        if not self.pressed:
            super().on_mouse_out()
        self.tooltip.hide()

    def on_mouse_over(self):
        x, y = mouse.get_pos()
        if self.pressed:
            if not self.rect.collidepoint((x, y)) and self.newLine:
                EventHandler.add_widgets(self.linea)
                self.newLine = False

            self.mover_linea()
        if self.hasFocus:
            self.tooltip.show()

    def update(self):
        if not self.enabled:
            for linea in self.lineas:
                EventHandler.del_widgets(linea)
            self.lineas.clear()


class ReglaH(BaseRegla):

    def __init__(self, parent, x, y):
        super().__init__(parent, x, y, parent.w, 16)
        self.nombre = self.parent.nombre + '.ReglaH'
        self.image = Surface((parent.w, 16))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.fondo = self.crear(parent.w)
        self.image.blit(self.fondo, self.clip)
        self.tooltip = ToolTip(self, self.tip + 'horizontal', self.x, self.y)

    @staticmethod
    def crear(d):
        fuente = font.SysFont('verdana', 8)
        regla = Surface((d, C // 2))
        regla.fill((255, 255, 255), (1, 1, d - 2, 14))

        for numero, i in enumerate(range(1, 33)):
            draw.line(regla, (0, 0, 0), (i * C, 0), (i * C, 16))
            digitos = [i for i in str(numero * C)]
            gx = 0
            for digito in digitos:
                render = fuente.render(digito, True, (0, 0, 0), (255, 255, 255))
                dx = (i - 1) * C + gx + 4
                regla.blit(render, (dx, 4))
                gx += 4

        return regla

    def mover_linea(self):
        abs_x, abs_y = mouse.get_pos()
        x, y = self.parent.get_relative_mouse_position()

        self.linea.rect.y = abs_y
        self.linea.y = y
        self.linea.dirty = 1

    def scroll(self, dx):
        self.clip.move_ip(dx, 0)
        self.image.blit(self.fondo, self.clip)
        self.dirty = 1

    def on_mouse_down(self, button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.linea = LineaGuiaX(self.parent, len(self.lineas))
            self.newLine = True


class ReglaV(BaseRegla):

    def __init__(self, parent, x, y):
        super().__init__(parent, x, y, 16, parent.h)
        self.nombre = self.parent.nombre + '.ReglaV'
        self.image = Surface((16, parent.h))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.fondo = self.crear(parent.h)
        self.image.blit(self.fondo, self.clip)
        self.tooltip = ToolTip(self, self.tip + 'vertical', self.x, self.y)

    @staticmethod
    def crear(d):
        fuente = font.SysFont('verdana', 8)
        regla = Surface((C // 2, d))
        regla.fill((255, 255, 255), (1, 1, 14, d - 2))

        for numero, i in enumerate(range(1, 33)):
            draw.line(regla, (0, 0, 0), (0, i * C), (C // 2, i * C))
            digitos = [i for i in str(numero * C)]
            gy = 0
            for digito in digitos:
                render = fuente.render(digito, True, (0, 0, 0), (255, 255, 255))
                dy = (i - 1) * C + gy + 1
                regla.blit(render, (4, dy))
                gy += 9

        return regla

    def mover_linea(self):
        abs_x, abs_y = mouse.get_pos()
        x, y = self.parent.get_relative_mouse_position()

        self.linea.rect.x = abs_x
        self.linea.x = x
        self.linea.dirty = 1

    def scroll(self, dy):
        self.clip.move_ip(0, dy)
        self.image.blit(self.fondo, self.clip)
        self.dirty = 1

    def on_mouse_down(self, button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.linea = LineaGuiaY(self.parent, len(self.lineas))
            self.newLine = True
