from azoe.widgets import SubVentana, Label, Entry, BotonAceptarCancelar, Checkbox, Marco, Boton
from azoe.engine.eventhandler import EventHandler
from globales import C, Sistema
from pygame import font


class CuadroPreferencias(SubVentana):
    paneles = None
    botones = None

    def __init__(self):
        super().__init__(10 * C+12, 8 * C + 9, 'Preferencias')
        x, y, w, h = self.x, self.y, self.w, self.h
        print(x,y,w,h)
        self.paneles = {}
        self.botones = []
        fuente = font.SysFont('Tahoma', 13)
        dx, dy, dw, dh = x + 60, y + 23, 270, 210
        nombres = [{'name': 'colores', 'class': BasePanel},
                   {'name': 'keys', 'class': PanelKeyBindings},
                   ]

        for i, item in enumerate(nombres):
            name = item['name']
            self.paneles[name] = item['class'](self, dx, dy, dw, dh)
            self.botones.append(Boton(self, x + 6, i * 25 + y + 23, name, self.show,
                                      fuente=fuente, scr=name, w=48, h=21))

        BotonAceptarCancelar(self, x + w - 150, y + h - 28, lambda: None)
        BotonAceptarCancelar(self, x + w - 80, y + h - 28)

    def show(self):
        panel_name = ''
        for boton in self.botones:
            if boton.presionado:
                panel_name = boton.scr
                break

        for panel in self.paneles:
            self.paneles[panel].hide()
        self.paneles[panel_name].show()


class BasePanel(Marco):
    def __init__(self, parent, x, y, w, h):
        super().__init__(x, y, w, h, parent=parent, borde=None)
        self.parent.agregar(self)

    def show(self):
        for objeto in self.contenido:
            EventHandler.add_widgets(objeto)
            # self.parent.agregar(self)

    def hide(self):
        for objeto in self.contenido:
            EventHandler.del_widgets(objeto)


class PanelColores(BasePanel):
    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        lista = ["R", "G", "B"]
        items = {}
        dy = 23
        for i, item in enumerate(lista):
            name, txt = item
            items[name] = {
                'label': [name, x + 4, y + (dy * i) + 3, name],
                'entry': [name, x + 170, y + (dy * i), 100, txt]
            }

        self.show()


class PanelKeyBindings(BasePanel):
    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        x, y, w, h = self.x, self.y + 2, self.w, self.h

        binded = Sistema.binded_methods
        lista = [["Proyecto Nuevo", binded['new_project']],
                 ["Abrir Proyecto", binded['open_project']],
                 ["Guardar Proyecto", binded['save_project']],
                 ["Guadar Proyecto como...", binded['save_project_as']],
                 ["Cerrar Proyecto", binded['close_project']],
                 ["Cortar", binded['cortar']],
                 ["Copiar", binded['copiar']],
                 ["Pegar", binded['pegar']],
                 ["Salir", binded['exit']]
                 ]

        items = {}
        dy = 23
        for i, item in enumerate(lista):
            name, txt = item
            items[name] = {
                'check': [True, x + 2, y + (dy * i) + 4],
                'label': [name, x + 20, y + (dy * i) + 3, name],
                'entry': [name, x + 170, y + (dy * i), 100, txt]
            }

        fuente = font.SysFont('Tahoma', 12)
        for name in items:
            l = items[name]['label']
            e = items[name]['entry']
            Checkbox(self, *items[name]['check'])
            Label(self, *l[:3], texto=l[3], fuente=fuente)
            Entry(self, *e[:3], w=e[3], texto=e[4])

        self.show()
