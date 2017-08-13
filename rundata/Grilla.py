from azoe.widgets import BaseWidget, ScrollH, ScrollV, BotonToggle, Marco, BotonCerrar
from globales import Sistema, C, LAYER_COLISIONES, LAYER_FONDO
from .reglas import ReglaH, ReglaV, HandlerRegla
from .SpecialCanvas import SpecialCanvas
from pygame import Surface, Rect, draw, SRCALPHA


class Grilla(Marco):
    canvas = None
    ScrollX = None
    ScrollY = None
    BtnVerGr = None
    BtnVerCapa = None
    verGrilla = False
    verRegla = False

    # layer = 1

    def __init__(self):
        self.nombre = 'Grilla'
        super().__init__(0, 19, 20 * C + 15, 15 * C + 16, False)

        self.canvas = SpecialCanvas(self, self.x + 16, self.y + 16, 20 * C, 15 * C)
        self.canvas.ScrollX = ScrollH(self.canvas, self.x + 16, self.y + self.h)
        self.canvas.ScrollY = ScrollV(self.canvas, self.x + self.w, self.y + 16)
        self.canvas.Grilla = SubGrilla(self, self.x + 16, self.y + 16, 20 * C, 15 * C)

        i = Sistema.iconos  # alias
        t = [[i['ver_fondo'], i['ver_cls'], i['ver_dis']], "Alterna entre el mapa de colisiones y la imagen de fondo"]
        c = [[i['grilla'], i['grilla_tog'], i['grilla_dis']], "Muestra u oculta la grilla"]

        self.BtnVerCapa = BotonToggle(self, 24 * C + 6, 23, 'BtnVerCapa', self.cmd_ver_capa, [*t[0]], t[1])
        self.BtnVerGr = BotonToggle(self, 24 * C + 6, C + 23, 'BtnVerGr', self.cmd_ver_grilla, [*c[0]], c[1])
        self.BtnCerrarMapa = BotonCerrar(self, self.w + 1, self.y, 15, 15, 'BtnCerrarMapa', Sistema.close_proyect)
        self.canvas.ReglaX = ReglaH(self.canvas, self.x + 15, self.y)
        self.canvas.ReglaY = ReglaV(self.canvas, self.x, self.y + 15)
        self.canvas.HandlerRegla = HandlerRegla(self.canvas, self.x, self.y)

        self.agregar(self.canvas.ReglaX, self.canvas.ReglaY, self.canvas.HandlerRegla,
                     self.canvas, self.canvas.ScrollX, self.canvas.ScrollY,
                     self.BtnCerrarMapa, self.BtnVerGr, self.BtnVerCapa)

        self.habilitar(False)

    # Funciones de comando para los botones
    def cmd_ver_grilla(self):
        if self.verGrilla:
            self.quitar(self.canvas.Grilla)
            self.verGrilla = False
        else:
            self.agregar(self.canvas.Grilla)
            self.verGrilla = True

    def cmd_ver_capa(self):
        capas = self.canvas.capas
        capas.switch_layer(LAYER_COLISIONES, LAYER_FONDO)

        if Sistema.capa_actual == LAYER_FONDO:
            Sistema.capa_actual = LAYER_COLISIONES
        elif Sistema.capa_actual == LAYER_COLISIONES:
            Sistema.capa_actual = LAYER_FONDO

    def habilitar(self, control):
        if control:
            self.canvas.ScrollX.enabled = True
            self.canvas.ScrollY.enabled = True
            self.BtnVerCapa.ser_habilitado()
            self.BtnVerGr.ser_habilitado()
            self.canvas.ReglaX.enabled = True
            self.canvas.ReglaY.enabled = True
            self.canvas.HandlerRegla.enabled = True
            self.canvas.enabled = True
        else:
            self.canvas.ScrollX.enabled = False
            self.canvas.ScrollY.enabled = False
            self.BtnVerCapa.ser_deshabilitado()
            self.BtnVerGr.ser_deshabilitado()
            self.canvas.ReglaX.enabled = False
            self.canvas.ReglaY.enabled = False
            self.canvas.HandlerRegla.enabled = False
            self.canvas.enabled = False

    def update(self):
        if Sistema.PROYECTO is None:
            self.BtnCerrarMapa.ser_deshabilitado()
        else:
            if not self.BtnCerrarMapa.enabled:
                self.BtnCerrarMapa.ser_habilitado()


class SubGrilla(BaseWidget):
    focusable = False
    clip = Rect(0, 0, 0, 0)

    def __init__(self, parent, x, y, w, h, **opciones):
        super().__init__(parent, **opciones)
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + '._grilla'
        self.image = Surface((w, h), SRCALPHA)
        self.fondo = self.crear(w, h, C)
        self.image.blit(self.fondo, self.clip)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def crear(w, h, cuadro):
        marco = Rect(0, 0, w, h)
        base = Surface(marco.size, SRCALPHA)
        _color = (100, 200, 100)
        for x in range(cuadro, (h // cuadro) * cuadro, cuadro):
            draw.line(base, _color, (x, marco.top), (x, marco.bottom), 1)
        for y in range(cuadro, (w // cuadro) * cuadro, cuadro):
            draw.line(base, _color, (marco.left, y - 1), (marco.right, y - 1), 1)

        return base

    def actualizar_tamanio(self, w, h):
        self.fondo = self.crear(w, h, C)
        self.image.blit(self.fondo, self.clip)
        self.dirty = 1

    def scroll(self, dx, dy):
        self.clip.move_ip(dx, dy)
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.fondo, self.clip)
        self.dirty = 1
