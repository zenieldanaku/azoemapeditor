from pygame import Surface, Color, font, display
from azoe.engine import color, EventHandler
from .basewidget import BaseWidget


class ToolTip(BaseWidget):
    focusable = False
    aparicion = -1

    def __init__(self, parent, mensaje, x, y, **opciones):
        opciones = self._opciones_por_default(opciones)
        super().__init__(parent, **opciones)
        self.x, self.y = x, y
        self.mensaje = mensaje
        self.nombre = self.parent.nombre + '.ToolTip'
        #self.layer = self.parent.layer
        self.image = self._crear(mensaje, opciones)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.w, self.h = self.rect.size
        w = display.get_surface().get_size()[0]
        self._ajustar(w)
        if self.nombre not in EventHandler.widgets:
            EventHandler.add_widget(self)

    @staticmethod
    def _crear(texto, opciones):
        fuente = font.SysFont(opciones['fontType'], opciones['fontSize'])
        fg_color, bg_color = opciones['colorText'], opciones['colorFondo']
        w, h = fuente.size(texto)
        fondo = Surface((w + 4, h + 2))
        fondo.fill(bg_color, (1, 1, w + 2, h))
        render = fuente.render(texto, True, fg_color, bg_color)
        fondo.blit(render, (2, 1))
        return fondo

    @staticmethod
    def _opciones_por_default(opciones):
        if 'Fuente' not in opciones:
            opciones['fontType'] = "tahoma"  # Sys.fdLibs+"\\fonts_tahoma.ttf"
        if 'fontSize' not in opciones:
            opciones['fontSize'] = 11
        if 'colorText' not in opciones:
            opciones['colorText'] = color('sysElmText')
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = Color(255, 255, 225)  # color de sistema

        return opciones

    def _ajustar(self, ancho):
        while True:
            if self.rect.x + self.w > ancho:
                self.rect.x -= 1
            else:
                self.rect.y = self.parent.y + self.h + 16
                break

    def show(self, delay=20):
        self.aparicion += 1
        if self.mensaje != '':
            if self.aparicion >= delay:
                alpha = self.image.get_alpha()
                self.image.set_alpha(alpha + 60)
        self.dirty = 1

    def hide(self):
        self.image.set_alpha(0)
        # self.i = -1
        self.dirty = 1
