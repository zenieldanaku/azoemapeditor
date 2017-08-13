from pygame import Surface, mouse, mask, Rect
from pygame.sprite import Group
from . import BaseWidget


class Canvas(BaseWidget):
    doc_w = None
    doc_h = None
    pressed = False
    shift = False
    eleccion = Rect(0, 0, 0, 0)
    selected = None
    SeleccionMultiple = False
    tiles = None

    def __init__(self, parent, x, y, w, h, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = (255, 255, 245)
        if 'colorCuadro' not in opciones:
            opciones['colorCuadro'] = (191, 191, 191)
        super().__init__(parent, **opciones)
        self.nombre = self.parent.nombre + '.Canvas'
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.elX, self.elY = 0, 0
        self.Tw, self.Th = w, h
        self.selected = Group()
        self.doc_w, self.doc_h = w, h
        self.image = Surface((self.w, self.h))
        self.pintar_fondo_cuadriculado(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def pintar_fondo_cuadriculado(self, imagen, c=32):
        imagen.fill(self.opciones['colorFondo'])
        for y in range(imagen.get_height() // c):
            for x in range(imagen.get_width() // c):
                if y % 2 == 0:
                    if x % 2 == 0:
                        imagen.fill(self.opciones['colorCuadro'], (x * c, y * c, c, c))
                else:
                    if x % 2 != 0:
                        imagen.fill(self.opciones['colorCuadro'], (x * c, y * c, c, c))

    def on_mouse_down(self, button):
        x, y = self.get_relative_mouse_position()
        selected = 0
        if button == 1 or button == 3:
            if hasattr(self, 'tiles'):
                selected = 0
                for tile in self.tiles:
                    if tile.selected:
                        selected += 1
                        if selected > 1:
                            break

            if not self.shift:
                if not self.SeleccionMultiple:
                    for tile in self.tiles:
                        tile.ser_deselegido()
            tiles = self.tiles.get_sprites_at((x, y))
            if tiles:
                item = tiles[-1]
                mascara = mask.from_surface(item.image)
                if mascara.get_at((x - item.rect.x, y - item.rect.y)):
                    item.on_mouse_down(button)
                    if selected > 1:
                        self.SeleccionMultiple = True
            else:
                for tile in self.tiles:
                    tile.ser_deselegido()
                if button == 1:
                    self.pressed = True
                    self.elX, self.elY = x, y
                    if self.eleccion.size != (0, 0):
                        self.eleccion.size = (0, 0)
                elif button == 3:
                    if hasattr(self, 'context'):
                        self.context.show()

    def on_mouse_up(self, button):
        x, y = self.get_relative_mouse_position()
        tiles = []
        if button == 1:
            if hasattr(self, 'tiles'):
                tiles = self.tiles.get_sprites_at((x, y))
            if tiles:
                for tile in tiles:
                    tile.on_mouse_up(button)
            else:
                self.pressed = False
                self.SeleccionMultiple = False

            selected = 0
            for tile in self.tiles:
                if self.eleccion.contains(tile.rect):
                    tile.ser_elegido()
                    selected += 1
            if selected > 1:
                self.SeleccionMultiple = True

            self.eleccion.size = 0, 0

    def get_relative_mouse_position(self, absx=None, absy=None):
        if absx is None and absy is None:
            abs_x, abs_y = mouse.get_pos()
        else:
            abs_x = absx
            abs_y = absy
        off_x, off_y = self.image.get_offset()
        dx = abs_x + off_x - self.x
        dy = abs_y + off_y - self.y

        if dx < 0:
            dx = 0
        if dy < 0:
            dy = 0

        if dx >= self.Tw:
            dx = self.Tw
        if dy >= self.Th:
            dy = self.Th

        return dx, dy

    def cambiar_layer(self, spr, mod):
        layer = spr.layer + mod
        self.tiles.change_layer(spr, layer)

    def update(self):
        x, y = self.elX, self.elY
        if self.pressed:
            nx, ny = self.get_relative_mouse_position()
            dx = nx - x
            dy = ny - y
            if dx > 0:
                self.eleccion.x = x
            elif dx < 0:
                self.eleccion.left = x
            else:
                self.eleccion.w = 0
            self.eleccion.w = dx

            if dy > 0:
                self.eleccion.y = y
            elif dy < 0:
                self.eleccion.top = y
            else:
                self.eleccion.h = 0
            self.eleccion.h = dy
            self.eleccion.normalize()
