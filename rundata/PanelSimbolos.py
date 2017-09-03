from globales import Sistema as Sys, C, LAYER_COLISIONES, LAYER_FONDO
from azoe.widgets import Marco, Boton, DropDownList, FileOpenDialog
from azoe import color, cargar_imagen, split_spritesheet
from .simbolos import SimboloSimple, SimboloMultiple
from pygame.sprite import LayeredDirty
from pygame import Rect, draw, Surface
from os import path


class PanelSimbolos(Marco):
    simbolos = None
    botones = {}

    def __init__(self):
        self.nombre = 'PanelSimbolos'
        super().__init__(21 * C, 19, 4 * C + 8, 16 * C - 1)
        self.simbolos = LayeredDirty()
        self.Items = DropDownList(self, 'Items', self.x + 3, self.y + 3 * C, self.w - 6)
        self.PrevArea = PreviewArea(self, self.x + 3, self.y + 4 * C - 8, self.w - 6, 4 * C)
        n, s, t, c, d, i = 'nom', 'scr', 'tipo', 'cmd', 'des', Sys.iconos  # aliases
        elementos = [
            {n: 'Nuevo', c: Sys.new_project, s: i['nuevo'], d: "Crear un mapa nuevo"},
            {n: 'Abrir', c: Sys.open_project, s: i['abrir'], d: "Abrir un mapa existente"},
            {n: 'Guardar', c: lambda: Sys.save_project(Sys.Guardado),
             s: [i['guardar'], i['guardar_dis']], d: "Guardar el mapa actual"},
            {n: 'barra'},
            {n: 'Cortar', c: Sys.cortar, s: [i['cortar'], i['cortar_dis']], d: "Cortar"},
            {n: 'Copiar', c: Sys.copiar, s: [i['copiar'], i['copiar_dis']], d: "Copiar"},
            {n: 'Pegar', c: Sys.pegar, s: [i['pegar'], i['pegar_dis']], d: "Pegar"},
            {n: 'barra'},
            {n: 'SetFondo', c: Sys.set_ruta_fondo, s: [i['fondo'], i['fondo_dis']], d: "Cargar imagen de fondo"},
            {n: 'addMob', c: lambda: FileOpenDialog(self.add_mob, Sys.fdAssets, ft=['.png']),
             s: [i['mob'], i['mob_dis']], d: "Cargar símbolo de mob"},
            {n: 'addProp', c: lambda: FileOpenDialog(self.add_props, Sys.fdAssets, ft=['.png']),
             s: [i['prop'], i['prop_dis']], d: "Cargar símbolo de prop"},

            {n: 'delSim', c: self.PrevArea.eliminar_simbolo_actual, s: [i['borrar'], i['borrar_dis']],
             d: "Eliminar este símbolo"}
        ]
        x = self.x + 4
        y = 19 + 4
        for e in elementos:
            if e['nom'] != 'barra':
                boton = Boton(self, x + 5, y, e['nom'], e['cmd'], e['scr'], tip=e['des'])
                x = boton.rect.right - 2
                self.botones[e['nom']] = boton
            else:
                x = self.x + 4
                y += 32
        self.habilitar(False)

    def on_key_down(self, tecla):
        simbolo = self.PrevArea.get_actual()
        simbolo.renombrar(self.Items.get_item_actual())
        self.PrevArea.simbolo_actual = simbolo.get_real_name()

    def add_mob(self, ruta):
        sprite = split_spritesheet(ruta)
        nombre = path.split(ruta)[1][0:-4]
        _rect = sprite[0].get_rect(center=self.PrevArea.area.center)
        datos = {'nombre': nombre, 'imagenes': sprite, 'grupo': 'mobs', 'tipo': 'Mob', 'ruta': ruta,
                 'pos': [_rect.x, _rect.y, 0]}
        simbolo = SimboloMultiple(self.PrevArea, datos)
        self.add_to_prev_area(nombre, simbolo)

    def add_props(self, ruta):
        sprite = cargar_imagen(ruta)
        nombre = path.split(ruta)[1][0:-4]
        _rect = sprite.get_rect(center=self.PrevArea.area.center)
        datos = {'nombre': nombre, 'image': sprite, 'grupo': 'props', 'tipo': 'Prop', 'ruta': ruta,
                 'pos': [_rect.x, _rect.y, 0]}
        simbolo = SimboloSimple(self.PrevArea, datos)
        self.add_to_prev_area(nombre, simbolo)

    def add_to_prev_area(self, nombre, simbolo):
        self.Items.set_item(nombre)
        self.PrevArea.agregar_simbolo(simbolo)

    def habilitar(self, control):
        for nombre in self.botones:
            if nombre not in ['Nuevo', 'Abrir', 'delSim']:
                item = self.botones[nombre]
                if control:
                    item.ser_habilitado()
                else:
                    item.ser_deshabilitado()

    @staticmethod
    def hide_menu():
        print('dummy')


class PreviewArea(Marco):
    simbolos = None
    simbolo_actual = ''

    def __init__(self, parent, x, y, w, h):
        self.nombre = parent.nombre + '.AreaPrev'
        super().__init__(x, y, w, h, False, parent)
        luz = color('sysElmLight')
        sombra = color('sysElmShadow')
        grilla = color((150, 200, 200))
        self.img_pos = self._dibujar_grilla(self._biselar(self.image, sombra, luz), grilla)
        self.img_neg = self._dibujar_grilla(self._biselar(Surface((w, h)), sombra, luz), grilla)
        self.image = self.img_pos

        self.area = Rect(self.x + 2, self.y + 2, self.w, self.h)
        self.simbolos = LayeredDirty()

    @staticmethod
    def _dibujar_grilla(imagen, color_linea):
        w, h = imagen.get_size()
        marco = Rect(0, 0, w - 2, h - 2)
        for x in range(1 * C, 6 * C, C):
            draw.line(imagen, color_linea, (x, marco.top), (x, marco.bottom))

        for y in range(1 * C, 13 * C, C):
            draw.line(imagen, color_linea, (marco.left, y), (marco.right, y))
        return imagen

    def agregar_simbolo(self, simbolo_nuevo):
        for simbolo in self.simbolos:
            simbolo.visible = False

        if simbolo_nuevo not in self.simbolos:
            self.simbolos.add(simbolo_nuevo)
        self.agregar(simbolo_nuevo)

    def eliminar_simbolo_actual(self):
        simbolo = self.get_actual()

        self.simbolos.remove(simbolo)
        self.quitar(simbolo)
        self.parent.Items.del_item(simbolo)

    def get_actual(self):
        for simbolo in self.simbolos:
            if simbolo.get_real_name() == self.simbolo_actual:
                return simbolo

    def habilitar(self, control):
        if not control:
            self.simbolos.empty()
            self.limpiar()
            self.parent.Items.clear()

    def update(self):
        nombre = self.parent.Items.get_item_actual()
        if nombre != self.simbolo_actual:
            for simbolo in self.simbolos:
                if simbolo.get_real_name() != nombre:
                    simbolo.visible = False
                else:
                    self.simbolo_actual = simbolo.get_real_name()
                    simbolo.visible = True
                    self.parent.Items.set_text(self.simbolo_actual)

        if len(self.simbolos):
            self.parent.botones['delSim'].ser_habilitado()
        else:
            self.parent.botones['delSim'].ser_deshabilitado()

        capa = Sys.capa_actual
        if capa == LAYER_FONDO:
            self.image = self.img_pos
            for simbolo in self.simbolos:
                simbolo.imagen_positiva()
        elif capa == LAYER_COLISIONES:
            self.image = self.img_neg
            for simbolo in self.simbolos:
                simbolo.imagen_negativa()
        self.dirty = 1
