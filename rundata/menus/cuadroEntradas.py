from azoe.widgets import SubVentana, Label, Entry, BotonAceptarCancelar, DataGrid, ScrollV
from globales import C, Sistema
from pygame import font


class CuadroEntrada(SubVentana):
    # layer = 20

    def __init__(self):
        super().__init__(6 * C + 16, 9 * C - 16, 'Entradas')
        self.nombre = 'CuadroEntradas'
        dx = 18
        self.grid = DataGrid(self, 'datos', self.x + 3 + dx, self.y + 23 + 15, cel_w=53, n_fil=9, sep=2)

        fuente = font.SysFont('Tahoma', 12)
        nombre = Label(self, 'nmbr', self.x + 9 + dx, self.y + 22, 'Nombre', fuente=fuente)
        lbl_pos_x = Label(self, 'PosX', self.x + C * 2 + 16 + dx, self.y + 22, 'X', fuente=fuente)
        lbl_pos_y = Label(self, 'PosY', self.x + C * 4 + 6 + dx, self.y + 22, 'Y', fuente=fuente)

        sort = sorted([nombre for nombre in Sistema.PROYECTO.script['entradas']])
        relleno = []
        for nombre in sort:
            x = Sistema.PROYECTO.script['entradas'][nombre]['x']
            y = Sistema.PROYECTO.script['entradas'][nombre]['y']
            relleno.append([nombre, x, y])

        self.grid.rellenar(relleno)
        scroll = ScrollV(self.grid, self.x + self.w - 16 - 4, self.y + 20 + 19)

        self.btnAceptar = BotonAceptarCancelar(self, self.x + 63, self.y + self.h - 23, self.aceptar)
        self.btnCanelar = BotonAceptarCancelar(self, self.x + self.w - 73, self.y + self.h - 23)

        self.agregar(nombre, lbl_pos_x, lbl_pos_y, scroll, self.btnAceptar, self.btnCanelar)

    def on_destruction(self):
        super().on_destruction()
        self.grid.on_destruction()

    def reubicar_en_ventana(self, dx=0, dy=0):
        self.grid.reubicar_en_ventana(dx, dy)
        super().reubicar_en_ventana(dx, dy)

    def aceptar(self):
        pass


class UnaEntrada(SubVentana):
    entrada_nombre = ''
    entrada_px = 0
    entrada_py = 0

    def __init__(self, px, py):
        super().__init__(4 * C + 16, C * 3 - 2, 'Insertar Entrada')
        fuente = font.SysFont('tahoma', 12)
        self.lblNombre = Label(self, 'nmbr', self.x + 3, self.y + 23, 'Nombre', fuente=fuente)
        self.lblPosX = Label(self, 'PosX', self.x + 3, self.y + 23 + 23, 'X', fuente=fuente)
        self.lblPosY = Label(self, 'PosY', self.x + C * 2 + 9, self.y + 23 + 23, 'Y', fuente=fuente)

        self.entryNombre = Entry(self, 'nmbr', self.x + C * 2 + 9, self.y + 20, 68)
        self.entryPosX = Entry(self, 'PosX', self.x + 3 + 10, self.y + 43, C + 26, texto=str(px))
        self.entryPosY = Entry(self, 'PosY', self.x + C * 2 + 19, self.y + 43, C + 26, texto=str(py))

        self.btnAceptar = BotonAceptarCancelar(self, self.x + 3, self.y + 70, self.aceptar)
        self.btnCancelar = BotonAceptarCancelar(self, self.x + C * 2 + 9, self.y + 70)

        self.agregar(self.lblNombre)
        self.agregar(self.lblPosX)
        self.agregar(self.lblPosY)

        self.agregar(self.entryNombre)
        self.agregar(self.entryPosY)
        self.agregar(self.entryPosX)

        self.agregar(self.btnAceptar)
        self.agregar(self.btnCancelar)

        self.btnAceptar.ser_deshabilitado()

    def aceptar(self):
        Sistema.PROYECTO.add_entry(self.entrada_nombre, self.entrada_px, self.entrada_py)
        self.cerrar()

    def update(self):
        self.entrada_nombre = self.entryNombre.return_text()
        self.entrada_px = self.entryPosX.return_text()
        self.entrada_py = self.entryPosY.return_text()

        if self.entrada_nombre != '':
            self.btnAceptar.ser_habilitado()
        else:
            self.btnAceptar.ser_deshabilitado()
