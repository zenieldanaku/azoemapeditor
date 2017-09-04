from globales import Sistema, C, LAYER_FONDO, LAYER_COLISIONES
from pygame import transform, Surface, draw, mouse, K_RSHIFT, K_LSHIFT
from pygame.sprite import LayeredDirty, DirtySprite, Rect
from .menus.cuadroEntradas import UnaEntrada
from azoe.widgets import Canvas, ContextMenu
from .simbolos import SimboloCNVS
from azoe import EventHandler

__all__ = ['SpecialCanvas']


class SpecialCanvas(Canvas):
    capas = None
    tiles = None
    px, py = 0, 0
    scrolling_enabled = False
    ScrollX = None
    ScrollY = None
    ReglaX = None
    ReglaY = None
    Grilla = None
    HandlerRegla = None
    guias = None
    fondo_rect = Rect(0, 0, 0, 0)

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.capas = LayeredDirty()
        self.tiles = LayeredDirty()
        self.guias = []
        comandos = [
            {'nom': 'Entrada', 'cmd': lambda: UnaEntrada(self.px, self.py)},
            {'nom': 'Pegar', 'cmd': lambda: Sistema.pegar(), 'icon': Sistema.iconos['pegar']}]
        self.context = ContextMenu(self, comandos)
        self.fondo = Surface(self.image.get_size())
        self.pintar_fondo_cuadriculado(self.fondo)

    def on_mouse_over(self):
        if self.SeleccionMultiple:
            x, y = self.get_relative_mouse_position()
            tiles = self.tiles.get_sprites_at((x, y))
            lista = self.tiles.sprites()
            if tiles:
                ref = tiles[0]
                idx = lista.index(ref)
                if ref.isMoving:
                    dx = ref.dx
                    dy = ref.dy

                    for tile in lista[idx + 1:] + lista[:idx]:
                        tile.mover(dx, dy)

    def on_mouse_down(self, button):
        if button == 1 or button == 3:
            super().on_mouse_down(button)
            if button == 3:
                self.px, self.py = self.get_relative_mouse_position()

        elif self.scrolling_enabled:
            if self.shift:
                if button == 5:
                    self.scroll(dx=-C)
                if button == 4:
                    self.scroll(dx=+C)
            else:
                if button == 5:
                    self.scroll(dy=-C)
                if button == 4:
                    self.scroll(dy=+C)

    def on_key_down(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = True
        for tile in self.tiles:
            if tile.selected:
                tile.on_key_down(event.key, self.shift)

    def on_key_up(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = False

        for tile in self.tiles:
            if tile.selected:
                tile.on_key_up(event.key)

    def actualizar_tamanio_fondo(self, w, h):
        self.fondo = transform.scale(self.fondo, (w, h))
        self.fondo_rect = self.fondo.get_rect()
        self.ReglaX.actualizar_tamanio(w)
        self.ReglaY.actualizar_tamanio(h)
        self.Grilla.actualizar_tamanio(w, h)
        self.ScrollX.actualizar_tamanio(w)
        self.ScrollY.actualizar_tamanio(h)
        self.scrolling_enabled = True
        # self.doc_w, self.doc_h = w, h
        # self.Th, self.Tw = w, h
        self.dirty = 1

    def paste(self, cluster):
        pos = mouse.get_pos()
        if self.rect.collidepoint(pos):  # Ctrl+V o menu contextual
            cluster.rect.center = self.get_relative_mouse_position()
        else:  # Boton "pegar" en panel
            cluster.rect.center = self.rect.center

        for element in cluster.elements:
            element.paste(*cluster.rect.topleft)
            if cluster.mode == 'copy':
                element.item['original'] = False
                self.colocar_tile(element.item)
            else:
                element.item.ser_deselegido()
                self.tiles.add(element.item)

    def colocar_tile(self, datos):
        rect = datos['rect']
        z = datos['pos'][2]
        datos['pos'] = rect.x, rect.y, z
        datos['index'] = Sistema.PROYECTO.add_item(datos)
        self.add_tile(datos)
        self.update()

    def add_tile(self, datos):
        self.tiles.add(SimboloCNVS(self, datos))

    def del_tile(self, tile):
        Sistema.PROYECTO.del_item(tile)
        self.tiles.remove(tile)
        index = tile.index
        for _tile in self.tiles:
            if _tile.index > index:
                _tile.index -= 1

    def scroll(self, dx=0, dy=0):
        if self.fondo_rect.top + dy > 0 or self.fondo_rect.bottom + dy <= 480:
            dy = 0
        if self.fondo_rect.left + dx > 0 or self.fondo_rect.right + dx <= 640:
            dx = 0
        self.fondo_rect.move_ip(dx, dy)

        self.capas.update(dx, dy)
        self.ReglaX.scroll(dx)
        self.ReglaY.scroll(dy)
        self.Grilla.scroll(dx, dy)
        for linea in self.guias:
            if linea.lin == 'x':
                linea.scroll(dy)
            elif linea.lin == 'y':
                linea.scroll(dx)

        for tile in self.tiles:
            tile.rect.move_ip(dx, dy)
        self.dirty = 1

    def render(self):
        base = self.capas.get_sprites_from_layer(LAYER_COLISIONES)[0].image
        for tile in self.tiles:
            base.blit(tile.img_cls, tile.rect)
        return base

    def habilitar(self, control):
        if not control:
            self.capas.empty()
            self.tiles.empty()
            self.actualizar_tamanio_fondo(20 * C, 15 * C)
            self.pintar_fondo_cuadriculado(self.fondo)
            self.enabled = False
        else:
            self.enabled = True

    def set_bg_image(self, sprite):
        EventHandler.set_focus(self)
        self.actualizar_tamanio_fondo(*sprite.rect.size)
        img = BackgroundImage(*sprite.rect.size)

        if sprite not in self.capas:
            self.capas.add(sprite, layer=LAYER_FONDO)
            self.capas.add(img, layer=LAYER_COLISIONES)

    def update(self):
        super().update()
        self.pintar_fondo_cuadriculado(self.fondo)
        self.tiles.update()
        self.capas.update()

        self.capas.draw(self.fondo)
        self.tiles.draw(self.fondo)

        if self.eleccion.size != (0, 0):
            draw.rect(self.fondo, (0, 255, 255), self.eleccion, 1)
        for tile in self.tiles:
            Sistema.PROYECTO.update_item_pos(tile)
        self.image.blit(self.fondo, (0, 0))
        self.dirty = 1


class BackgroundImage(DirtySprite):
    def __init__(self, w, h):
        super().__init__()
        self.image = Surface((w, h))
        self.rect = self.image.get_rect()

    def update(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)
        self.dirty = 1
