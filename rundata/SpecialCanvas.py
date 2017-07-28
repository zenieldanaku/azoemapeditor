from globales import Sistema as Sys, C, LAYER_FONDO, LAYER_COLISIONES
from pygame import transform, Surface, draw, mouse, K_RSHIFT, K_LSHIFT
from pygame.sprite import LayeredDirty, DirtySprite
from .menus.cuadroEntradas import UnaEntrada
from azoe.widgets import Canvas, ContextMenu
from .simbolos import SimboloCNVS
from azoe import EventHandler


class SpecialCanvas(Canvas):
    capas = None
    tiles = None
    px, py = 0, 0
    ScrollX = None
    ScrollY = None
    ReglaX = None
    ReglaY = None
    Grilla = None
    HandlerRegla = None

    def __init__(self, parent, x, y, w, h, clip, **opciones):
        super().__init__(parent, x, y, w, h, clip, **opciones)
        self.capas = LayeredDirty()
        self.tiles = LayeredDirty()
        comandos = [
            {'nom': 'Entrada', 'cmd': lambda: UnaEntrada(self.px, self.py)},
            {'nom': 'Pegar', 'cmd': lambda: Sys.pegar(), 'icon': Sys.iconos['pegar']},
        ]
        self.context = ContextMenu(self, comandos)

    def on_mouse_over(self):
        x, y = self.get_relative_mouse_position()
        for tile in self.tiles.get_sprites_at((x, y)):
            if tile.isMoving:
                if self.SeleccionMultiple:
                    self.mover_tiles(tile.dx, tile.dy)

    def on_mouse_down(self, button):
        if button == 1 or button == 3:
            super().on_mouse_down(button)
            if button == 3:
                self.px, self.py = self.get_relative_mouse_position()

        elif self.ScrollY.enabled:
            if self.shift:
                if button == 5:
                    self.scroll(dx=+10)
                if button == 4:
                    self.scroll(dx=-10)
            else:
                if button == 5:
                    self.scroll(dy=+10)
                if button == 4:
                    self.scroll(dy=-10)

    def on_key_down(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = True
        for tile in self.tiles:
            if tile.selected:
                if tile.on_key_down(event.key, self.shift):  # delete
                    index = tile.index
                    self.tiles.remove(tile)
                    Sys.selected = None
                    del Sys.PROYECTO.script[tile.grupo][tile.get_real_name()][index]
                    for _tile in self.tiles:
                        if _tile.index > index:
                            _tile.index -= 1

    def on_key_up(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = False

        for tile in self.tiles:
            if tile.selected:
                tile.on_key_up(event.key)

    def actualizar_tamanio_fondo(self, w, h):
        self.FONDO = transform.scale(self.FONDO, (w, h))
        self.image = self.FONDO.subsurface(self.clip)
        self.ReglaX.actualizar_tamanio(w)
        self.ReglaY.actualizar_tamanio(h)
        self.Grilla.actualizar_tamanio(w, h)
        self.ScrollX.actualizar_tamanio(w)
        self.ScrollY.actualizar_tamanio(h)
        self.doc_w, self.doc_h = w, h
        self.Th, self.Tw = w, h
        self.dirty = 1

    @staticmethod
    def _imagen_colisiones(w, h):
        spr = DirtySprite()
        spr.image = Surface((w, h))
        spr.rect = spr.image.get_rect()
        spr.dirty = 2
        return spr

    def pegar(self, item):
        if type(item) == dict:  # copy
            self.colocar_tile(item)
        else:  # cut
            pos = mouse.get_pos()
            x, y = self.get_relative_mouse_position()
            if self.rect.collidepoint(pos):  # Ctrl+V o menu contextual
                item.rect.center = x, y
            else:  # Boton "pegar" en panel
                item.rect.center = self.rect.center

            item.x, item.y = item.rect.topleft
            self.tiles.add(item)

    def colocar_tile(self, datos):
        pos = mouse.get_pos()
        rect = datos['rect']
        if self.rect.collidepoint(pos):
            if datos['original']:
                rect.center = self.get_relative_mouse_position(*rect.center)
            else:
                rect.center = self.get_relative_mouse_position()
        else:
            rect.center = self.rect.center
        z = datos['pos'][2]
        datos['pos'] = rect.x, rect.y, z
        datos['index'] = Sys.PROYECTO.add_item(datos)
        self.add_tile(datos)
        self.update()

    def add_tile(self, datos):
        tile = SimboloCNVS(self, datos)
        self.tiles.add(tile)

    def scroll(self, dx=0, dy=0):
        # try:
        # top,left,right,bottom = self.clip.top,self.clip.left,self.clip.right,self.clip.bottom
        # print('antes:',(top,left,right,bottom),end= ', ')
        # self.clip.x += -dx
        # self.clip.y += -dy
        # print(dx,dy)
        # self.ReglaX.scroll(dx,dy)
        # self.ReglaY.scroll(dx,dy)
        # self.Grilla.scroll(dx,dy)
        # x,y,w,h = self.clip

        # self.FONDO.set_clip(self.clip)
        # self.FONDO.scroll(-dx,-dy)
        for capa in self.capas:
            capa.rect.move_ip(-dx, -dy)
        self.dirty = 1
        # print()
        # top,left,right,bottom = self.clip.top,self.clip.left,self.clip.right,self.clip.bottom
        # x,y,w,h = self.clip
        # print('despues:',(top,left,right,bottom))
        # self.image = self.FONDO.subsurface(self.clip)
        # self.HandlerRegla.scroll(dx,dy)

        # except Exception as error:
        #    print('aca',error)
        #    pass

        # self.clip.x -= dx
        # self.clip.y -= dy
        # self.image.set_clip(self.clip)

    def render(self):
        base = self.capas.get_sprites_from_layer(LAYER_COLISIONES)[0].image
        for tile in self.tiles:
            base.blit(tile.img_cls, tile.rect)
        return base

    def mover_tiles(self, dx, dy):

        cadena = []
        for tile in self.tiles:
            if not tile.isMoving:  # el que estamos moviendo manualmente
                if tile.selected:
                    cadena.insert(tile.index,
                                  tile.tipo + ' ' + tile.get_real_name() +
                                  ' #' + str(tile.index) + ' @ (' + str(tile.rect.x) +
                                  ',' + str(tile.rect.y) + ',' + str(tile.z) + ')')
                    tile.mover(dx, dy)  # el resto de los que estan seleccionados
            else:
                cadena.insert(tile.index,
                              tile.tipo + ' ' + tile.get_real_name() +
                              ' #' + str(tile.index) + ' @ (' + str(tile.rect.x) +
                              ',' + str(tile.rect.y) + ',' + str(tile.z) + ')')
            Sys.estado = ', '.join(cadena)

    def habilitar(self, control):
        if not control:
            self.capas.empty()
            self.tiles.empty()
            self.clip.topleft = 0, 0
            self.actualizar_tamanio_fondo(15 * C, 15 * C)
            self.enabled = False
        else:
            self.enabled = True

    def update(self):
        super().update()

        if Sys.IMG_FONDO is None:
            self.capas.empty()
            self.pintar_fondo_cuadriculado()

        else:
            spr = Sys.IMG_FONDO
            if self.FONDO.get_size() != spr.rect.size:
                EventHandler.set_focus(self)
                self.actualizar_tamanio_fondo(*spr.rect.size)
                img = self._imagen_colisiones(*spr.rect.size)

                if spr not in self.capas:
                    self.capas.add(spr, layer=LAYER_FONDO)
                    self.capas.add(img, layer=LAYER_COLISIONES)
            self.capas.draw(self.FONDO)

        self.tiles.update()
        self.tiles.draw(self.FONDO)
        if self.eleccion.size != (0, 0):
            draw.rect(self.FONDO, (0, 255, 255), self.eleccion, 1)
        for tile in self.tiles:
            Sys.PROYECTO.update_item_pos(tile)
        self.dirty = 1
