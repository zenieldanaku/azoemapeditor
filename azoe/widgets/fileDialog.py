from . import Marco, Entry, BotonAceptarCancelar, DropDownList, subVentana
from . import Label, ScrollV, Tree, BaseOpcion, ToolTip
from pygame import Rect, font, key, KMOD_LCTRL, KMOD_RCTRL
from azoe.libs.textrect import render_textrect
from pygame.sprite import LayeredDirty
import os


class FileDiag(subVentana):
    pressed = False
    carpetaActual = ''
    ArchivosSeleccionados = []
    UltimaSeleccion = ''
    nombredeArchivo = ''
    tipoSeleccinado = ''
    carpetaVieja = ''
    layer = 10

    def __init__(self, comando, filetypes=None, permitirmultiple=False, carpeta_actual=os.getcwd(), **opciones):
        c = 32
        self.comando = comando['cmd']
        self.TipoComando = comando['tipo']
        self.nombre = 'FileDialog.'
        _nombre = ''
        if self.TipoComando == 'A':
            _nombre = 'Abrir'
        elif self.TipoComando == 'G':
            _nombre = 'Guardar'
        elif self.TipoComando == 'Gc':
            _nombre = 'Guardar como...'
        self.nombre += _nombre
        super().__init__(16 * c, 10 * c + 18, _nombre, **opciones)
        self.SeleccionMultiple = permitirmultiple
        self.carpetaActual = ''
        self.ArchivosSeleccionados = []
        self.UltimaSeleccion = ''
        self.nombredeArchivo = ''
        self.tipoSeleccinado = ''
        self.carpetaVieja = ''

        if filetypes is None:
            filetypes = ['*.png', '*.json', '*.mob', '*.quest']
        x, y, w, h = self.x, self.y, self.w, self.h  # abreviaturas de legibilidad
        self.carpetas = ArbolCarpetas(self, x + 2, y + 19, w // 2 - 2, 8 * c, carpeta_actual)
        self.archivos = ListaDeArchivos(self, x + w // 2, y + 19, w // 2 - 2, 8 * c, self.SeleccionMultiple)
        self.entryNombre = Entry(self, 'IngresarRuta', x + 2 * c + 3, y + 8 * c + 23, 11 * c + 16, '')
        self.BtnAccion = BotonAceptarCancelar(self, x + 14 * c - 8, y + 8 * c + 24, self.ejecutar_comando,
                                              comando['scr'])
        self.tipos = DropDownList(self, 'TipoDeArchivo', x + 2 * c + 3, y + 9 * c + 19, 11 * c + 16, filetypes)
        self.BtnCancelar = BotonAceptarCancelar(self, x + 14 * c - 8, y + 9 * c + 20)
        self.lblNombre = Label(self, 'Nombre', x + 4, y + 9 * c - 7, texto='Nombre:',
                               **{'fontType': 'Tahoma', 'fontSize': 13})
        self.lblTipo = Label(self, 'Tipo', x + 4, y + 9 * c + 19, texto="Tipo:",
                             **{'fontType': 'Tahoma', 'fontSize': 13})

        self.agregar(self.carpetas)
        self.agregar(self.archivos)
        self.agregar(self.entryNombre)
        self.agregar(self.BtnAccion)
        self.agregar(self.tipos)
        self.agregar(self.BtnCancelar)
        self.agregar(self.lblTipo)
        self.agregar(self.lblNombre)

    def titular(self, texto):
        fuente = font.SysFont('verdana', 12)
        rect = Rect(2, 2, self.w - 4, fuente.get_height() + 1)
        render = render_textrect(texto, fuente, rect, (255, 255, 255), (0, 0, 0))
        self.image.blit(render, rect)

    def ejecutar_comando(self):
        if self.TipoComando == 'A':
            if self.SeleccionMultiple:
                rutas = []
                for archivo in self.ArchivosSeleccionados:
                    rutas.append(os.path.join(self.carpetaActual, archivo))
                self.comando(rutas)
            else:

                ruta = os.path.join(self.carpetaActual, self.UltimaSeleccion)
                self.comando(ruta)

        elif self.TipoComando == 'G' or self.TipoComando == 'Gc':
            if self.tipoSeleccinado != '' and not self.nombredeArchivo.endswith(self.tipoSeleccinado):
                ruta = os.path.join(self.carpetaActual, self.nombredeArchivo + self.tipoSeleccinado)
            else:
                ruta = os.path.join(self.carpetaActual, self.nombredeArchivo)
            self.comando(ruta)

        self.cerrar()

    def update(self):
        tipo = self.tipos.ItemActual.lstrip('*')
        if self.tipoSeleccinado != tipo:
            self.tipoSeleccinado = tipo
            self.archivos.actualizar_lista(self.carpetaActual, self.tipoSeleccinado.lstrip('.'))

        self.carpetaActual = self.carpetas.CarpetaSeleccionada
        if self.carpetaActual != self.carpetaVieja:
            self.carpetaVieja = self.carpetaActual
            self.archivos.actualizar_lista(self.carpetaActual, self.tipoSeleccinado.lstrip('.'))

        nombre = self.entryNombre.devolver_texto()
        if nombre != '':
            self.nombredeArchivo = nombre

        if self.archivos.Seleccionados:
            if self.SeleccionMultiple:
                for archivo in self.archivos.Seleccionados:
                    if archivo not in self.ArchivosSeleccionados:
                        self.ArchivosSeleccionados.append(archivo)
                self.entryNombre.setMultipleTexts(self.archivos.Seleccionados)

            elif self.archivos.UltimaSeleccion != self.nombredeArchivo:
                self.entryNombre.setText(self.archivos.UltimaSeleccion)
                self.UltimaSeleccion = self.archivos.UltimaSeleccion


class ArbolCarpetas(Marco):
    CarpetaSeleccionada = ''

    def __init__(self, parent, x, y, w, h, carpeta_actual, **opciones):
        super().__init__(x, y, w, h, False, parent, **opciones)
        self.nombre = self.parent.nombre + '.ArbolDeCarpetas'
        self.arbol = Tree(self, self.x, self.y, self.w - 16, self.h, self._generar_arbol(os.getcwd()), carpeta_actual)
        self.agregar(self.arbol)
        self.CarpetaSeleccionada = carpeta_actual

    @staticmethod  # decorator! ^^ 'cause explicit is better than implicit
    def _generar_arbol(path):
        walk = []
        x, y = -1, -1
        root_ = ''
        roots = []
        for dirname, dirnames, dummy in os.walk(path):
            split = os.path.split(dirname)
            nombre = split[1]
            root = os.path.split(split[0])[1]
            if '.git' in dirnames:
                dirnames.remove('.git')
            if '.idea' in dirnames:
                dirnames.remove('.idea')
            if '__pycache__' in dirnames:
                dirnames.remove('__pycache__')
            for subdirname in dirnames:
                if subdirname.startswith('_'):
                    dirnames.remove(subdirname)

            if root in roots:
                x = roots.index(root)
            elif root != root_:
                roots.append(root)
                x += 1
                root_ = root

            if dirnames:
                empty = False
            else:
                empty = True

            walk.append({'x': x, 'obj': nombre, 'empty': empty, 'path': dirname, 'hijos': dirnames})

        return walk

    def scroll(self, dy):
        pass

    def update(self):
        item = self.arbol.ItemActual
        if item != '':
            self.CarpetaSeleccionada = item


class ListaDeArchivos(Marco):
    SeleccionMultiple = False
    UltimaSeleccion = ''

    def __init__(self, parent, x, y, w, h, permitirmultiple=False, **opciones):
        if 'colorFondo' not in opciones:
            opciones['colorFondo'] = 'sysMenBack'
        self.nombre = parent.nombre + '.ListaDeArchivos'
        super().__init__(x, y, w, h, False, parent, **opciones)
        self.ScrollY = ScrollV(self, self.x + self.w - 16, self.y)
        self.agregar(self.ScrollY)
        self.items = LayeredDirty()
        self.Seleccionados = []
        self.SeleccionMultiple = permitirmultiple
        self.doc_h = h

    @staticmethod
    def _filtrar_extensiones(archivos, extension):
        if extension != '':
            filtrado = []
            for archivo in archivos:
                if extension != '':
                    split = archivo[0].split('.')
                    ext = split[-1]
                    if ext == extension:
                        filtrado.append(archivo)
            return filtrado
        else:
            return archivos

    @staticmethod
    def _listar_archivos(fold):
        lista = []
        for item in os.listdir(fold):
            if os.path.isfile(os.path.join(fold, item)):
                lista.append([item, os.path.join(fold, item)])
        return lista

    def crear_lista(self, opciones, ext):
        m = self.SeleccionMultiple
        lista = self._filtrar_extensiones(opciones, ext)
        h = 0
        for n in range(len(lista)):
            nom = lista[n][0]
            ruta = lista[n][1]
            dy = self.y + (n * h)
            opcion = _Opcion(self, nom, ruta, self.x, dy, self.w - 16, multi=m)
            h = opcion.image.get_height()
            self.items.add(opcion)
            if self.rect.contains(opcion.rect):
                self.agregar(opcion)

    def borrar_lista(self):
        for item in self.items:
            self.items.remove(item)
            if item in self:
                self.quitar(item)

    def scroll(self, dy=0):
        pass

    def actualizar_lista(self, carpeta, tipo):
        self.borrar_lista()
        nuevalista = self._listar_archivos(carpeta)
        self.crear_lista(nuevalista, tipo)

    def on_mouse_down(self, button):
        if self.ScrollY.enabled:
            if button == 5:
                self.ScrollY.moverCursor(dy=+10)
            if button == 4:
                self.ScrollY.moverCursor(dy=-10)

    def update(self):
        for item in self.items:
            if item.isSelected:
                self.UltimaSeleccion = item.texto
                if item.texto not in self.Seleccionados:
                    self.Seleccionados.append(item.texto)
                    if not self.SeleccionMultiple:
                        break


class _Opcion(BaseOpcion):
    isSelected = False
    texto = ''
    MultipleSelection = False

    def __init__(self, parent, nombre, ruta, x, y, w=0, multi=False, **opciones):
        super().__init__(parent, nombre, x, y, w)
        self.texto = nombre
        self.tooltip = ToolTip(self, ruta, x, y)
        self.MultipleSelection = multi

    def on_focus_in(self):
        super().on_focus_in()
        self.image = self.img_sel
        self.isSelected = True
        self.dirty = 1

    def on_focus_out(self):
        super().on_focus_out()
        mods = key.get_mods()
        if not (mods & KMOD_LCTRL or mods & KMOD_RCTRL) or not self.MultipleSelection:
            self.image = self.img_des
            self.isSelected = False
            self.dirty = 1

    def update(self):
        if self.hasMouseOver:
            self.tooltip.show()
        else:
            self.tooltip.hide()
