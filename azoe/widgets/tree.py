from . import Marco, BaseWidget, BaseOpcion, ToolTip, ScrollV
from azoe.engine import EventHandler, color
from pygame import Rect, Surface, draw
from pygame.sprite import LayeredDirty


class Tree(Marco):
    ItemActual = ''
    items = None

    def __init__(self, parent, x, y, w, h, walk, actual, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        self.nombre = parent.nombre + '.Tree'
        super().__init__(x, y, w, h, False, **opciones)
        self.parent = parent
        self.layer = self.parent.layer + 1
        self.items = LayeredDirty()
        self.crear_lista(walk, actual)
        self.ItemActual = actual  # ruta
        self.ScrollY = ScrollV(self, self.x + self.w, self.y)
        self.agregar(self.ScrollY)
        self.doc_h = h

    def scroll(self, dy):
        pass

    def crear_lista(self, opciones, actual):
        h = 0
        parentesco = {}
        for y in range(len(opciones)):
            x = opciones[y]['x']
            dx = self.x + (x * 16)
            dy = self.y + (y * h)

            item = Item(self, y, dx, dy, opciones[y])

            root = opciones[y]['root']
            if root not in parentesco:
                parentesco[root] = []
            parentesco[root].append(item)

            if item.opcion.path == actual:
                item.opcion.select()
            h = item.h
            self.items.add(item)
            self.agregar(item)

        for padre in self.items:
            if padre.path in parentesco:
                for hijo in parentesco[padre.path]:
                    padre.hijos.add(hijo)

    def mover(self, item, dy):
        idx = item.idx

        h = 0
        for hijo in item.hijos:
            dh, dy = hijo.get_h()
            h += dh
            idx += dy

        for i in range(idx, len(self.items)):
            widget = self.items.get_sprite(i)
            widget.mover(dh * dy)

    def reselect(self, opcion):
        for item in self.items:
            item.opcion.deselect()
        self.ItemActual = opcion

    def regenerate(self, walk, ruta):
        for item in self.items:
            item.on_destruction()
            self.quitar(item)
        self.items.empty()
        self.crear_lista(walk, ruta)


class Item(BaseWidget):
    hijos = None
    folded = False

    def __init__(self, parent, idx, x, y, keyargs, **opciones):
        super().__init__(parent, **opciones)
        self.x, self.y = x, y
        self.idx = idx
        self.nombre = self.parent.nombre + '.Item:' + keyargs['path']
        self.nom_obj = keyargs['obj']
        self.ruta = keyargs['root']
        self.path = keyargs['path']
        self.hijos = LayeredDirty()
        self.visible = 0  # no es que sea invisible, es que no tiene imagen
        self.opcion = _Opcion(self, self.nom_obj, keyargs['path'], x + 16 + 3, y)
        h = self.opcion.image.get_height()
        self.cursor = _Cursor(self, x, y, 16, h - 2, keyargs['empty'])
        w = self.cursor.rect.w + 3 + self.opcion.rect.w
        self.rect = Rect(x, y, w, h)
        self.w, self.h = self.rect.size
        if self.rect.bottom < self.parent.rect.bottom:
            EventHandler.add_widget(self.opcion)
            EventHandler.add_widget(self.cursor)

    def on_destruction(self):
        EventHandler.del_widget(self.opcion.tooltip)
        EventHandler.del_widget(self.opcion)
        EventHandler.del_widget(self.cursor)

    def reubicar_en_ventana(self, dx=0, dy=0):
        super().reubicar_en_ventana(dx, dy)
        self.opcion.reubicar_en_ventana(dx, dy)
        self.cursor.reubicar_en_ventana(dx, dy)

    def collapse_children(self):
        for hijo in self.hijos:
            hijo.hide()
            hijo.collapse_children()
        self.folded = True

    def expand_children(self):
        for hijo in self.hijos:
            hijo.show()
            if hijo.cursor.open:
                hijo.expand_children()
        self.folded = False

    def hide(self):
        self.opcion.visible = 0
        self.cursor.visible = 0
        self.enabled = False

    def show(self):
        if self.rect.bottom < self.parent.rect.bottom:
            self.opcion.visible = 1
            self.cursor.visible = 1
            self.enabled = True

    def mover(self, dy):
        for obj in [self, self.opcion, self.cursor]:
            obj.y += dy
            obj.rect.y += dy

    def get_h(self):
        h = self.h
        y = 0
        if not self.folded:
            for hijo in self.hijos:
                dh, y = hijo.get_h()
                y = 1
                h += dh

        return h, y


class _Opcion(BaseOpcion):
    path = ''
    selected = False

    def __init__(self, parent, nombre, path, x, y, w=0):
        super().__init__(parent, nombre, x, y, w)
        self.layer = self.parent.layer
        self.texto = nombre
        self.path = path
        self.tooltip = ToolTip(self.parent, path, x, y)
        self.nombre = self.parent.nombre + '.Opcion'

    def select(self):
        self.selected = True
        self.image = self.img_sel
        self.dirty = 1

    def deselect(self):
        self.selected = False
        self.image = self.img_des
        self.dirty = 1

    def on_mouse_down(self, button):
        if button == 1:
            self.parent.parent.reselect(self.path)
            self.select()

    def on_focus_out(self):
        super().on_focus_out()
        self.deselect()

    def update(self):
        if self.hasMouseOver:
            self.tooltip.show()
        else:
            self.tooltip.hide()


class _Cursor(BaseWidget):
    image = None
    open = True

    def __init__(self, parent, x, y, w, h, vacio, **opciones):
        super().__init__(parent, **opciones)
        self.nombre = self.parent.nombre + '.Cursor'
        self.layer = self.parent.layer  # overwrite
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.vacio = vacio
        self.img_cld = self._crear(self.w, self.h, False)
        self.img_opn = self._crear(self.w, self.h, True)
        self.set_status()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @staticmethod
    def _crear(w, h, closed):
        imagen = Surface((w, h))
        imagen.fill(color('sysMenBack'))
        rect = imagen.get_rect()
        if closed:
            draw.line(imagen, (0, 0, 0), (5, rect.h // 2), (rect.w - 4, rect.h // 2), 2)
        else:
            draw.line(imagen, (0, 0, 0), (5, rect.h // 2), (rect.w - 4, rect.h // 2), 2)
            draw.line(imagen, (0, 0, 0), (8, 4), (8, rect.h - 4), 2)
        draw.rect(imagen, (0, 0, 0), (2, 2, rect.w - 2, rect.h - 2), 1)
        return imagen

    def on_mouse_down(self, button):
        if button == 1:
            if not self.vacio:
                self.open = not self.open

            if self.open:
                dy = +1
            else:
                dy = -1

            self.set_status()
            self.parent.parent.mover(self.parent, dy)

    def set_status(self):
        if self.open:
            self.image = self.img_opn
            self.parent.expand_children()
            self.dirty = 1
        else:
            self.image = self.img_cld
            self.parent.collapse_children()
            self.dirty = 1
