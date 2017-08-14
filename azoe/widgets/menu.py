from azoe.engine import EventHandler, color
from pygame import Surface, Rect, font, mouse, draw
from azoe.libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
from . import BaseWidget


class Menu(BaseWidget):
    cascada = None
    boton = None
    visible = True
    nombre = ''
    referencias = None

    def __init__(self, parent, nombre, ops, x, y, **opciones):
        super().__init__(parent, **opciones)
        self.nombre = self.parent.nombre + '.Menu.' + nombre
        self.fuente = font.SysFont('tahoma', 12)
        self.referencias = {}
        self.boton = BotonMenu(self, nombre, x, y)
        h = self.boton.rect.h
        self.cascada = Cascada(self, nombre, ops, x, h + 1)

    def show_menu(self):
        self.cascada.show_menu()

    def is_visible(self):
        return self.visible

    def hide_menu(self):
        # TODO:
        # hacer esto con recursion,
        # de manera que cierre cualquier
        # cantidad de cascadas abiertas.
        for opcion in self.cascada.opciones:
            if isinstance(opcion.command, Cascada):
                if opcion.command.mostrar:
                    opcion.command.hide_menu()

        if self.cascada.mostrar:
            self.cascada.hide_menu()


class BotonMenu(BaseWidget):
    nombre = ''
    menu = None

    def __init__(self, parent, nombre, x, y, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        if 'colorTexto' not in opciones:
            opciones['colorTexto'] = 'sysMenText'
        if 'colorBgSel' not in opciones:
            opciones['colorBgSel'] = 'sysBoxSelBack'
        super().__init__(parent, **opciones)
        self.nombre = self.parent.nombre + '.Boton'
        self.img_des = self.crear_boton(nombre, parent.fuente, color(opciones['colorTexto']),
                                        color(self.opciones['colorFondo']))
        self.img_sel = self.crear_boton(nombre, parent.fuente, color(opciones['colorTexto']),
                                        color(self.opciones['colorBgSel']))
        self.image = self.img_des
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x, y))
        EventHandler.add_widgets(self)

    @staticmethod
    def crear_boton(nombre, fuente, fgcolor, bgcolor):
        w, h = fuente.size(nombre)
        rect = Rect(-1, -1, w + 15, h + 1)
        render = render_textrect(nombre, fuente, rect, fgcolor, bgcolor, 1)
        return render

    def on_mouse_down(self, dummy):
        EventHandler.set_focus(self.parent.cascada)
        self.parent.parent.solo_un_menu(self.parent)

    def on_mouse_in(self):
        super().on_mouse_in()
        self.image = self.img_sel
        self.dirty = 1

    def on_mouse_out(self):
        super().on_mouse_out()
        self.image = self.img_des
        self.dirty = 1


class Cascada(BaseWidget):
    opciones = None
    parent = None
    mostrar = False

    def __init__(self, parent, nombre, opciones, x, y):
        super().__init__()
        self.visible = False
        self.componentes = LayeredDirty()
        self.parent = parent
        self.nombre = parent.nombre + '.Cascada:' + nombre
        self.layer = self.parent.layer + 2
        self.x, self.y = x, y
        _fuente = font.SysFont('Tahoma', 11)
        self.w = 0
        key_x = 0

        for n in range(len(opciones)):
            w = 19 + _fuente.size(opciones[n]['nom'])[0]  # ancho(icono)+ancho(nombre)
            if 'win' in opciones[n]:
                opciones[n]['scr'] = '...'
                w += _fuente.size('...')[0]
            if 'key' in opciones[n]:
                ancho = _fuente.size(opciones[n]['key'])[0]
                w += ancho + 30
                if ancho > key_x:
                    key_x = ancho + 70
            if 'csc' in opciones[n]:
                opciones[n]['scr'] = 'flecha'
                w += 30
            if 'win' not in opciones[n] and 'csc' not in opciones[n]:
                opciones[n]['scr'] = None

            if w > self.w:
                self.w = w

        h = 19
        ajuste = 0
        self.h = h * len(opciones) + 2
        _h = 0
        for n in range(len(opciones)):
            _nom = opciones[n]['nom']
            if _nom != 'barra':
                opcion = OpcionCascada(self, opciones[n], 1, n * h + ajuste + 1, self.w, key_x)
                _h = opcion.rect.bottom
                if 'csc' in opciones[n]:
                    x = self.x + self.w - 3
                    y = (n + 1) * h + ajuste - 1
                    opcion.command = Cascada(self, _nom, opciones[n]['csc'], x, y)
                elif 'win' in opciones[n]:
                    opcion.command = opciones[n]['win']
                else:
                    opcion.command = opciones[n]['cmd']
                self.add_to_references(_nom, opcion)
            else:
                opcion = BaseWidget()
                opcion.image = self._linea_horizontal(self.w - 1)
                opcion.rect = opcion.image.get_rect(topleft=(3, _h + 4))
                ajuste -= 10
            self.componentes.add(opcion)
        self.image = Surface((self.w + 5, self.h + ajuste))
        self.image.fill(color('sysMenBack'), (1, 1, self.w + 3, self.h + ajuste - 2))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # EventHandler.add_widget(self)

    def add_to_references(self, key, item):
        recursion = True
        ancestro = self.parent
        while recursion:
            if hasattr(ancestro, 'parent') and isinstance(ancestro.parent, Menu):
                ancestro = ancestro.parent
            else:
                recursion = False
        if hasattr(ancestro, 'referencias'):
            ancestro.referencias[key] = item

    @staticmethod
    def _linea_horizontal(w):
        line = Surface((w, 2))
        draw.line(line, (100, 100, 100), [0, 0], [w, 0])
        draw.line(line, (200, 200, 200), [0, 1], [w, 1])
        return line

    def get_relative_mouse_position(self):
        abs_x, abs_y = mouse.get_pos()
        dx = abs_x - self.x
        dy = abs_y - self.y
        return dx, dy

    def get_component(self):
        x, y = self.get_relative_mouse_position()
        if self.componentes.get_sprites_at((x, y)):
            return self.componentes.get_sprites_at((x, y))[-1]
        return self

    def on_mouse_down(self, button):
        item = self.get_component()
        if item != self:
            item.on_mouse_down(button)
        if not self.parent.is_visible():
            self._visible = False

    def on_mouse_up(self, button):
        item = self.get_component()
        if item != self:
            item.on_mouse_up(button)

    def show_menu(self):
        EventHandler.add_widgets(self)
        self.mostrar = True
        self._visible = True
        self.dirty = 1

    def hide_menu(self):
        self.mostrar = False
        for componente in self.componentes:
            if isinstance(componente, OpcionCascada):
                componente.ser_deseleccionado()
                if isinstance(componente.command, Cascada):
                    componente.command.hide_menu()
        self._visible = False
        self.dirty = 1

    def on_mouse_over(self):
        if self.mostrar:
            for item in self.componentes:
                item.on_mouse_out()
            item = self.get_component()
            if item != self:
                item.on_mouse_in()
        self.dirty = 1

    def on_focus_in(self):
        super().on_focus_in()
        self.show_menu()

    def on_focus_out(self):
        super().on_focus_out()
        recursion = True
        ancestro = self.parent
        while recursion:
            if hasattr(ancestro, 'parent') and hasattr(ancestro.parent, 'hide_menu'):
                ancestro = ancestro.parent
            else:
                recursion = False
        ancestro.hide_menu()

    def key_combination(self, key):
        for componente in self.componentes:
            if componente.key_combination == key:
                componente.execute_key_binding()

    def update(self):
        self.componentes.update()
        self.componentes.draw(self.image)


class OpcionCascada(BaseWidget):
    command = None
    setFocus_onIn = True

    def __init__(self, parent, data, x, y, max_w, key_x, **opciones):
        super().__init__(parent, **opciones)
        if 'Fuente' not in self.opciones:
            self.opciones['fontType'] = 'Tahoma'
        if 'fontSize' not in self.opciones:
            self.opciones['fontSize'] = 11
        fuente = font.SysFont(self.opciones['fontType'], self.opciones['fontSize'])
        self.x, self.y = x, y
        self.nombre = self.parent.nombre + '.OpcionCascada.' + data['nom']
        icon = data.get('icon', False)
        rapido = data.get('key', False)
        self.KeyCombination = rapido
        self.img_uns = self.crear(data, fuente, color('sysElmText'), color('sysMenBack'), max_w, key_x, icon, rapido)
        self.img_sel = self.crear(data, fuente, color('sysElmText'), color('sysBoxSelBack'), max_w, key_x, icon, rapido)
        self.img_des = self.crear(data, fuente, color('sysDisText'), color('sysMenBack'), max_w, key_x, icon, rapido)
        self.image = self.img_uns
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def crear(data, fuente, fgcolor, bgcolor, w, key_x, icono, rapido):
        h = fuente.get_height() + 3

        flecha = False
        abrv = False
        if rapido:
            abrv = fuente.render(rapido, True, fgcolor, bgcolor)

        nombre = data['nom']
        if data['scr'] == '...':
            nombre += data['scr']
        elif data['scr'] == 'flecha':
            flecha = Surface((9, 9))
            flecha.fill(bgcolor)
            draw.polygon(flecha, fgcolor, [[1, 1], [1, 8], [6, 4]])

        render = fuente.render(nombre, True, fgcolor, bgcolor)

        imagen = Surface((w, h))
        imagen.fill(bgcolor)

        x = 19
        if icono:
            x = imagen.blit(icono, (0, 0)).w
        if x:
            imagen.blit(render, (x, 2))
        if flecha:
            imagen.blit(flecha, (w - 10, 4))

        if rapido:
            imagen.blit(abrv, (key_x, 2))
        return imagen

    def on_mouse_down(self, button):
        if self.enabled:
            if isinstance(self.command, Cascada):
                self.command.show_menu()
            else:
                self.command()
                self.parent.on_focus_out()

    def on_mouse_in(self):
        if self.enabled:
            super().on_mouse_in()
            self.ser_seleccionado()

    def on_mouse_out(self):
        super().on_mouse_out()
        if self.enabled:
            self.ser_deseleccionado()

    def ser_seleccionado(self):
        if self.enabled:
            self.image = self.img_sel
            self.dirty = 1

    def ser_deseleccionado(self):
        if self.enabled:
            self.image = self.img_uns
            self.dirty = 1

    def ser_deshabilitado(self):
        self.image = self.img_des
        self.enabled = False
        self.dirty = 1

    def ser_habilitado(self):
        self.image = self.img_uns
        self.enabled = True
        self.dirty = 1

    def on_mouse_over(self):
        print(self.nombre)
        if isinstance(self.command, Cascada):
            self.command.show_menu()

    def execute_key_binding(self):
        self.command()


class ContextMenu(Cascada):
    def __init__(self, parent, comandos=False):
        if not comandos:
            comandos = [{'nom': 'Dummy', 'cmd': lambda: None}]
        super().__init__(parent, 'ContextMenu', comandos, 0, 0)

    def show(self):
        x, y = mouse.get_pos()
        self.rect.topleft = x, y
        self.x, self.y = x, y
        self.show_menu()

    def on_focus_out(self):
        self.hasFocus = False
        self.hide_menu()
