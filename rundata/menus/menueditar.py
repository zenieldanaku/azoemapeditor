from .cuadroEditarSimbolo import EditarSimbolo
from .cuadroEntradas import CuadroEntrada
from .cuadropreferencias import CuadroPreferencias
from globales import Sistema as Sys
from azoe.widgets import Menu


class MenuEditar(Menu):
    def __init__(self, parent, x, y):
        binded = Sys.binded_methods
        items = [
            {"nom": 'Deshacer', 'cmd': lambda: print('deshacer'), 'key': 'Ctrl+Z'},
            {"nom": 'Rehacer', 'cmd': lambda: print('rehacer'), 'key': 'Ctrl+Alt+Z'},
            {"nom": 'barra'},
            {"nom": 'Cortar', "cmd": Sys.cortar, "icon": Sys.iconos['cortar'], 'key': binded['cortar']},
            {"nom": 'Copiar', "cmd": Sys.copiar, "icon": Sys.iconos['copiar'], 'key': binded['copiar']},
            {"nom": 'Pegar', "cmd": Sys.pegar, "icon": Sys.iconos['pegar'], 'key': binded['pegar']},
            {"nom": 'barra'},
            {"nom": 'Entradas', "win": lambda: CuadroEntrada()},
            {"nom": 'Simbolo', 'win': lambda: EditarSimbolo()},
            {'nom': 'Preferencias', 'win': lambda: CuadroPreferencias(), 'key': binded['set_preferences']}
        ]
        super().__init__(parent, 'Editar', items, x, y)

        self.referencias['Rehacer'].ser_deshabilitado()

    def update(self):
        objeto = self.referencias['Entradas']
        if Sys.PROYECTO is None:
            objeto.ser_deshabilitado()
        elif not objeto.enabled:
            objeto.ser_habilitado()
