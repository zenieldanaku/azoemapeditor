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

    def __init__(self, comando, filetypes=None, permitirmultiple=False, carpeta_actual='', **opciones):
        c = 32
        self.comando = comando['cmd']
        self.nombre = 'FileDialog.' + comando['scr']
        super().__init__(16 * c, 10 * c + 18+22, comando['scr'], **opciones)
        self.SeleccionMultiple = permitirmultiple
        self.carpetaActual = ''
        self.ArchivosSeleccionados = []
        self.UltimaSeleccion = ''
        self.nombredeArchivo = ''
        self.tipoSeleccinado = ''
        self.carpetaVieja = ''

        x, y, w, h = self.x, self.y, self.w, self.h  # abreviaturas de legibilidad
        ft, fs = 'fontType', 'fontSize'
        self.dir_base = Entry(self, 'IngrsarDireccion',  x + 2, y + 21, w-2, os.getcwd())
        self.carpetas = ArbolCarpetas(self, x + 2, y + 43, w // 2 - 2, 8 * c, carpeta_actual)
        self.archivos = ListaDeArchivos(self, x + w // 2, y + 43, w // 2 - 2, 8 * c, self.SeleccionMultiple)
        self.entryNombre = Entry(self, 'IngresarRuta', x + 2 * c + 3, y + 9 * c + 15, 11 * c + 16, '')
        self.accion = BotonAceptarCancelar(self, x + 14 * c - 8, y + 9 * c + 16, self.do_command, comando['scr'])
        self.tipos = DropDownList(self, 'TipoDeArchivo', x + 2 * c + 3, y + 10 * c + 11, 11 * c + 16, filetypes)
        self.BtnCancelar = BotonAceptarCancelar(self, x + 14 * c - 8, y + 10 * c + 12)
        self.lblNombre = Label(self, 'Nombre', x + 4, y + 9 * c + 16, texto='Nombre:', **{ft: 'Tahoma', fs: 13})
        self.lblTipo = Label(self, 'Tipo', x + 4, y + 10 * c + 12, texto="Tipo:", **{ft: 'Tahoma', fs: 13})

        self.agregar(self.dir_base)
        self.agregar(self.carpetas)
        self.agregar(self.archivos)
        self.agregar(self.entryNombre)
        self.agregar(self.accion)
        self.agregar(self.tipos)
        self.agregar(self.BtnCancelar)
        self.agregar(self.lblTipo)
        self.agregar(self.lblNombre)

    def titular(self, texto):
        fuente = font.SysFont('verdana', 12)
        rect = Rect(2, 2, self.w - 4, fuente.get_height() + 1)
        render = render_textrect(texto, fuente, rect, (255, 255, 255), (0, 0, 0))
        self.image.blit(render, rect)

    def do_command(self):
        pass

    def on_key_down(self, keydata):
        ruta = self.dir_base.devolver_texto()
        if ruta.endswith('\\'):
            ruta = ruta[:-1]
        self.carpetas.regenerate(ruta, ruta)

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


class FileOpenDialog(FileDiag):
    def __init__(self, cmd, fd, ft=None):
        comando = {'scr': 'Abrir', 'cmd': cmd}
        super().__init__(comando, ft, permitirmultiple=True, carpeta_actual=fd)

    def do_command(self):
        if self.SeleccionMultiple:
            rutas = []
            for archivo in self.ArchivosSeleccionados:
                rutas.append(os.path.join(self.carpetaActual, archivo))
            self.comando(rutas)
        else:

            ruta = os.path.join(self.carpetaActual, self.UltimaSeleccion)
            self.comando(ruta)
        self.cerrar()


class FileSaveDialog(FileDiag):
    def __init__(self, cmd, fd, ft=None):
        comando = {'scr': 'Guardar', 'cmd': cmd}
        super().__init__(comando, ft, permitirmultiple=False, carpeta_actual=fd)

    def do_command(self):
        if self.tipoSeleccinado != '' and not self.nombredeArchivo.endswith(self.tipoSeleccinado):
            ruta = os.path.join(self.carpetaActual, self.nombredeArchivo + self.tipoSeleccinado)
        else:
            ruta = os.path.join(self.carpetaActual, self.nombredeArchivo)
        self.comando(ruta)
        self.cerrar()


class ArbolCarpetas(Marco):
    CarpetaSeleccionada = ''
    arbol = None

    def __init__(self, parent, x, y, w, h, carpeta_actual, **opciones):
        super().__init__(x, y, w, h, False, parent, **opciones)
        self.nombre = self.parent.nombre + '.ArbolDeCarpetas'
        self.arbol = Tree(self, self.x, self.y, self.w - 16, self.h, self._generar_arbol(os.getcwd()), carpeta_actual)
        self.agregar(self.arbol)
        self.CarpetaSeleccionada = self.arbol.ItemActual

    def regenerate(self, path, carpeta):
        self.arbol.regenerate(self._generar_arbol(path), carpeta)

    @staticmethod
    def _generar_arbol(_path):
        walk = []
        dx = _path.count('\\')
        for dirname, hijos, _ in os.walk(_path):
            _split = os.path.split(dirname)
            nombre = _split[1]
            root = _split[0]
            for exclude in ['.git', '.idea', '__pycache__']:
                if exclude in hijos:
                    hijos.remove(exclude)
            for subdirname in hijos:
                if subdirname.startswith('_'):
                    hijos.remove(subdirname)

            if hijos:
                empty = False
            else:
                empty = True

            x = dirname.count('\\') - dx
            walk.append({'x': x, 'root': root, 'obj': nombre, 'empty': empty, 'path': dirname, 'hijos': hijos})

        return walk

    def scroll(self, dy):
        pass

    def update(self):
        item = self.arbol.ItemActual
        if item != '':
            self.CarpetaSeleccionada = item
        self.dirty = 1

    def on_destruction(self):
        self.arbol.on_destruction()


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
        print(button)

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