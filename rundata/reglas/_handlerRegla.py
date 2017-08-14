from azoe.widgets import BaseWidget, ToolTip
from ._guias import LineaGuiaX, LineaGuiaY
from pygame import Surface, draw, mouse
from azoe.engine import EventHandler


class HandlerRegla(BaseWidget):
    selected = False
    pressed = False
    lineas = []
    tip = 'Haga clic y arrastre para generar dos guías'
    lineaX = None
    lineaY = None
    newLine = False

    def __init__(self, parent, x, y, **opciones):
        super().__init__(parent, **opciones)
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + '.HandlerRegla'
        self.image = self._crear()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.w, self.h = self.image.get_size()
        self.tooltip = ToolTip(self, self.tip, self.x, self.y)

    @staticmethod
    def _crear():
        imagen = Surface((16, 16))
        imagen.fill((255, 255, 255), (1, 1, 14, 14))
        draw.line(imagen, (0, 0, 0), (0, 10), (14, 10))
        draw.line(imagen, (0, 0, 0), (10, 0), (10, 14))
        return imagen

    def on_mouse_down(self, button):
        if button == 1 and self.enabled:
            self.pressed = True
            self.lineaX = LineaGuiaX(self.parent, len(self.lineas))
            self.lineaY = LineaGuiaY(self.parent, len(self.lineas))
            self.newLine = True

    def on_mouse_up(self, button):
        if button == 1 and self.enabled:
            self.pressed = False
            self.lineas.append(self.lineaX)
            self.lineas.append(self.lineaY)
            self.lineaX = None
            self.lineaY = None

    def on_mouse_in(self):
        super().on_mouse_in()
        self.toggle_selection(True)

    def on_mouse_out(self):
        self.toggle_selection(False)
        if not self.pressed:
            super().on_mouse_out()
            self.tooltip.hide()

    def on_mouse_over(self):
        x, y = mouse.get_pos()
        if self.pressed:
            if not self.rect.collidepoint((x, y)) and self.newLine:
                EventHandler.add_widgets(self.lineaX, self.lineaY)
                self.newLine = False

            self.mover_lineas()
        if self.hasFocus:
            self.tooltip.show()

    def toggle_selection(self, select):
        if select and self.enabled:
            draw.line(self.image, (125, 255, 255), (1, 10), (14, 10))
            draw.line(self.image, (125, 255, 255), (10, 1), (10, 14))
        else:
            draw.line(self.image, (0, 0, 0), (0, 10), (14, 10))
            draw.line(self.image, (0, 0, 0), (10, 0), (10, 14))

    def scroll(self, dx, dy):
        for linea in self.lineas:
            if isinstance(linea, LineaGuiaX):
                linea.rect.y -= dy
            elif isinstance(linea, LineaGuiaY):
                linea.rect.x -= dx

    def mover_lineas(self):
        x, y = self.parent.get_relative_mouse_position()
        abs_x, abs_y = mouse.get_pos()

        self.lineaX.rect.y = abs_y
        self.lineaY.rect.x = abs_x
        self.lineaX.x = y
        self.lineaY.y = x
        self.lineaX.dirty = 1
        self.lineaY.dirty = 1

    def update(self):
        if not self.enabled:
            for linea in self.lineas:
                EventHandler.del_widgets(linea)
            self.lineas.clear()
