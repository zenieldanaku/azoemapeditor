from pygame import Rect, Surface, draw, mouse, SRCALPHA, PixelArray, K_RCTRL, K_LCTRL, K_RSHIFT, K_LSHIFT
from azoe.widgets import SubVentana, Boton, BotonAceptarCancelar, Label
from azoe.engine.RLE import serialize, encode, comprimir
from pygame.sprite import DirtySprite, LayeredDirty
from azoe.engine import EventHandler
from globales import Sistema as Sys, C


class EditarSimbolo(SubVentana):
    pressed = False
    shift = False
    control = False
    brocha = 5
    esTransparente = False
    tile = None
    origin = None
    LAYER_COLISION = 0
    LAYER_SPRITE = 1
    color_colision = 255, 0, 255, 255
    color_transparente = 0, 0, 0, 0
    color_actual = None
    modo = 'Pintar'
    crop_visible = True
    crop_area = None
    # layer = 20

    def __init__(self):
        titulo = None
        self.nombre = 'Editar Simbolo'
        super().__init__(12 * C, 10 * C, self.nombre, False)
        x, y, w, h = self.x, self.y, self.w, self.h
        self.color_actual = self.color_colision

        self.area = self.crear_area()
        self.areaArray = PixelArray(self.area.image.copy())
        self.background = Surface((10 * C, 8 * C))

        self.capas = LayeredDirty()
        self.capas.add(self.area, layer=self.LAYER_COLISION)
        if Sys.selected is not None:
            tile = Sys.selected
            _titulo = ' #' + str(tile.index)
        else:
            tile = EventHandler.get_widget('PanelSimbolos.AreaPrev').get_actual()
            _titulo = ' (nuevo)'

        if tile is not None:
            self.origin = tile
            self.tile = self.crear_sprite(tile, self.area.rect.center)
            self.capas.add(self.tile, layer=self.LAYER_SPRITE)
            self.crop_area = self.crear_crop_area(self.tile.rect)
            titulo = self.nombre + ': ' + tile.get_real_name() + _titulo
        else:
            self.crop_visible = False

        self.cursor = Cursor(self.brocha)
        self.capas.add(self.cursor, layer=2)

        self.btnMas = Boton(self, x + w - C, y + C, 'Aumentar', lambda: self.ajustar_brocha(+1), '+',
                            tip='Aumenta en un punto el tamaño de la brocha')
        self.btnMenos = Boton(self, x + w - C, y + 2 * C - 7, 'Disminuir', lambda: self.ajustar_brocha(-1), '-',
                              tip='Disminuye en un punto el tamaño de la brocha')
        self.btnTrans = Boton(self, x + w - C, y + 3 * C - 7, 'Transparencia', self.alternar_transparencia, 'Tr',
                              tip='Alterna entre la transparencia del sprite')
        self.btnCapas = Boton(self, x + w - C, y + 4 * C - 14, 'AlterarCapas', self.alternar_capas, 'Cp',
                              tip='Alerna el orden de las capas de sprite y de colisiones')
        self.btnBrocha = Boton(self, x + w - C, y + 5 * C - 14, 'AlternarBrocha', self.alternar_brocha, 'Br',
                               'Alterna entre el color sólido y el transparente')
        self.btnCrop = Boton(self, x + w - C, y + 6 * C - 14, 'VerCropArea', self.alternar_crop, 'Cr',
                             'Muestra u oculta el area de corte')

        self.btnAceptar = BotonAceptarCancelar(self, x + w - C * 4 - 16, y + h - 28, self.aceptar)
        self.btnCancelar = BotonAceptarCancelar(self, x + w - C * 2 - 10, y + h - 28)
        self.lblBrocha = Label(self, 'TamanioDeBrocha', x + 3, y + h - 28,
                               'Brocha: ' + str(self.brocha) + ' ' + self.modo)

        self.agregar(self.btnMas)
        self.agregar(self.btnMenos)
        self.agregar(self.btnTrans)
        self.agregar(self.btnCapas)
        self.agregar(self.btnBrocha)
        self.agregar(self.btnCrop)
        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)
        self.agregar(self.lblBrocha)
        if self.tile is None:
            self.btnAceptar.ser_deshabilitado()
            self.btnCrop.ser_deshabilitado()
            titulo = self.nombre
        elif self.origin.img_cls is not None:
            self.area.image.blit(self.origin.img_cls, self.tile.rect)
        self.titular(titulo)

        EventHandler.set_focus(self)

    @staticmethod
    def crear_area():
        spr = DirtySprite()
        spr.image = Surface((10 * C, 8 * C), SRCALPHA)
        spr.image.fill((0, 0, 0, 0))
        spr.rect = spr.image.get_rect()
        spr.dirty = 2
        return spr

    @staticmethod
    def crear_crop_area(tile_rect):
        return tile_rect.inflate(1, 1)

    @staticmethod
    def crear_sprite(sprite, center_pos):
        spr = DirtySprite()
        spr.img_pos = sprite.img_pos
        spr.img_neg = sprite.img_neg
        spr.image = spr.img_pos
        spr.rect = spr.image.get_rect(center=center_pos)
        spr.dirty = 2
        return spr

    def alternar_brocha(self):
        if self.color_actual == self.color_colision:
            self.color_actual = self.color_transparente
            self.modo = 'Borrar'
        else:
            self.color_actual = self.color_colision
            self.modo = 'Pintar'
        self.lblBrocha.set_text('Brocha: ' + str(self.brocha) + ' ' + self.modo)

    def ajustar_brocha(self, mod):
        self.brocha += mod
        if self.brocha < 1:
            self.brocha = 1
        if self.brocha > 99:
            self.brocha = 99
        self.lblBrocha.set_text('Brocha: ' + str(self.brocha) + ' ' + self.modo)
        self.cursor.alterar_tamanio(self.brocha)

    def aceptar(self):
        _crop = self.crop_area.inflate(-1, -1)
        image = self.area.image.subsurface(_crop)

        self.origin.img_cls = image
        self.origin.cls_code = comprimir(encode(serialize(image)))

        EventHandler.del_widget(self)

    def alternar_transparencia(self):
        self.esTransparente = not self.esTransparente

    def alternar_capas(self):
        self.capas.switch_layer(self.LAYER_COLISION, self.LAYER_SPRITE)

    def alternar_crop(self):
        self.crop_visible = not self.crop_visible

    def pintar(self):
        x, y = mouse.get_pos()
        rect = Rect(0, 0, self.brocha, self.brocha)
        dx = x - (self.x + C) - rect.w // 2
        dy = y - (self.y + C) - rect.h // 2

        self.areaArray = PixelArray(self.area.image.copy())
        w, h = self.area.image.get_size()
        for pxy in range(dy, rect.h + dy):
            if 0 <= pxy <= h - 1:
                for pxx in range(dx, rect.w + dx):
                    if 0 <= pxx <= w - 1:
                        if self.modo == 'Pintar':
                            self.areaArray[pxx, pxy] = self.color_colision
                        elif self.modo == 'Borrar':
                            self.areaArray[pxx, pxy] = self.color_transparente
        self.area.image = self.areaArray.make_surface()

    def on_mouse_up(self, button):
        super().on_mouse_up(button)
        self.pressed = False

    def on_mouse_down(self, button):
        super().on_mouse_down(button)
        x, y = mouse.get_pos()
        _rect = self.area.rect.copy()
        _rect.topleft = (self.x + C, self.y + C)
        if button == 1:
            if _rect.collidepoint((x, y)):
                self.pressed = True
        elif button == 4:
            self.ajustar_brocha(+1)
        elif button == 5:
            self.ajustar_brocha(-1)

    def on_mouse_over(self):
        super().on_mouse_over()
        x, y = mouse.get_pos()
        _rect = self.area.rect.copy()
        _rect.topleft = (self.x + C, self.y + C)
        if _rect.collidepoint((x, y)):
            self.cursor.visible = 1
            dx = x - (self.x + C) - self.brocha // 2
            dy = y - (self.y + C) - self.brocha // 2
            self.cursor.mover(dx, dy)
        else:
            self.cursor.visible = 0

    def on_key_down(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = True
        elif event.key == K_RCTRL or event.key == K_LCTRL:
            self.control = True

    def on_key_up(self, event):
        if event.key == K_RSHIFT or event.key == K_LSHIFT:
            self.shift = False
        elif event.key == K_RCTRL or event.key == K_LCTRL:
            self.control = False

    def update(self):
        self.background.fill((0, 0, 0))
        if self.pressed:
            self.pintar()

        if self.tile is not None:
            if self.esTransparente:
                self.tile.image = self.tile.img_neg
            else:
                self.tile.image = self.tile.img_pos

        self.capas.update()
        self.capas.draw(self.background)
        if self.crop_visible:
            draw.rect(self.background, (0, 255, 0), self.crop_area, 1)
        self.image.blit(self.background, (C, C))


class Cursor(DirtySprite):
    alterar = False

    def __init__(self, size):
        super().__init__()
        self.image = self._crear_imagen(size)
        self.rect = self.image.get_rect()

    @staticmethod
    def _crear_imagen(size):
        img = Surface((size, size))
        img.set_colorkey((0, 0, 0))

        rect = img.get_rect()
        draw.rect(img, (0, 255, 255), (0, 0, rect.right, rect.bottom), 1)

        return img

    def mover(self, x, y):
        self.rect.topleft = x, y

    def alterar_tamanio(self, nuevotamanio):
        self.alterar = nuevotamanio

    def update(self):
        if self.alterar:
            self.image = self._crear_imagen(self.alterar)
            self.alterar = False
        self.dirty = 1
