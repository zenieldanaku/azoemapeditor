from azoe import color, Marco
from globales import C
from .menus import *


class BarraMenus(Marco):
    menus = {}
    # layer = 1

    def __init__(self, **opciones):
        self.nombre = 'Barra_Menus'
        super().__init__(0, 0, 24 * C, 19, False, **opciones)

        self.menus = {}
        self.image.fill(color(opciones.get('colorFondo', 'sysMenBack')))
        prev = 0
        for menu_nom in ['Archivo', 'Editar', 'Mapa']:
            menu = eval('Menu' + menu_nom + '(self,prev,3)')
            prev = menu.boton.rect.right
            self.menus[menu.nombre] = menu

    def on_focus_in(self):
        super().on_focus_in()
        self.ocultar_menus()

    def on_focus_out(self):
        super().on_focus_out()
        for menu in self.menus:
            self.menus[menu].hide_menu()

    def solo_un_menu(self, _menu=None):
        if _menu is not None:
            for menu in self.menus:
                if menu != _menu.nombre:
                    self.menus[menu].hide_menu()
        self.menus[_menu.nombre].show_menu()

    def ocultar_menus(self):
        for menu in self.menus:
            self.menus[menu].hide_menu()

    def update(self):
        for menu in self.menus:
            self.menus[menu].update()
