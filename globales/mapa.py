# from os import path


class Proyecto:
    rutas = None  # {}
    script = None  # {}
    mapa = None  # {}

    def __init__(self, data):
        self.rutas = {'fondo': data['fondo'],
                      'colisiones': data['colisiones'],
                      'props': data['props'],
                      'mobs': data['mobs']}

        self.script = {
            "fondo": "",
            "colisiones": "",
            "props": {},
            "mobs": {},
            "entradas": {},
            "salidas": {},
            "refs": {}
        }

    def cargar(self, data):
        for key in data:
            if key in self.script:
                self.script[key] = data[key]
            elif key.startswith('fd_'):
                self.rutas[key[3:]] = data[key]

    def guardar(self, ):
        d = self.script.copy()
        for key in self.rutas:
            d['fd_' + key] = self.rutas[key]

        return d

    def update_item_pos(self, tile):
        nombre = tile.get_real_name()
        grupo = tile.grupo
        index = tile.index
        x, y = tile.rect.topleft
        layer = tile.layer
        rot = tile.rot

        self.script[grupo][nombre][index] = x, y, layer, rot

    def add_reference(self, nombre, ruta, code):
        if nombre not in self.script['refs']:
            self.script['refs'][nombre] = {'ruta': ruta, 'code': code}

    def add_entry(self, nombre, px, py):
        if nombre not in self.script['entradas']:
            self.script['entradas'][nombre] = {'x': px, 'y': py}

    def add_item(self, datos):
        nombre = datos['nombre']
        ruta = datos['ruta']
        grupo = datos['grupo']
        code = datos['cols_code']

        root = self.script[grupo]
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            self.add_reference(nombre, ruta, code)
        else:
            if self.script['refs'][nombre]['code'] == code:
                root[nombre].append([])
                index = len(root[nombre]) - 1
            else:
                nombre += '_' + str(len(self.script['refs']))
                data = {'nombre': nombre, 'ruta': ruta, 'grupo': grupo, 'cols_code': code}
                index = self.add_item(data)

        return index

    def del_item(self, item):
        del self.script[item.grupo][item.get_real_name()][item.index]


class Stage:
    def __init__(self):
        self.data = {
            "entradas": {
                "<nombre>": {
                    "chunk": "",
                    "pos": [0, 0]
                }
            },
            "salidas": [{
                "stage": "",
                "nombre": "",
                "rect": [0, 0, 0, 0],
                "chunk": "",
                "entrada": "",
                "direcciones": []}
            ],
            "ambiente": "",
            "amanece": [0, 0],
            "atardece": [0, 0],
            "anochece": [0, 0]
        }

    def exportar(self, data):
        self.data.clear()
        for item in ['ambiente', 'amanece', 'atardece', 'anochece']:
            self.data[item] = data[item]

        for nombre in data['entradas']:
            self.data['entradas'][nombre] = {}
            entrada = self.data['entradas'][nombre]
            entrada['chunk'] = data['entradas'][nombre]['chunk']
            entrada['pos'] = data['entradas'][nombre]['pos']

        for datos in data['salidas']:
            # datos = stage, nombre, rect, chunk, entrada, direcciones
            self.data['salidas'].append(datos)


class Chunk:
    def __init__(self):
        self.data = {
            "fondo": "maps/fondos/filename.png",
            "colisiones": "maps/colisiones/filename.png",
            "props": {},
            "mobs": {},
            "limites": {
                "izq": None,
                "der": None,
                "inf": None,
                "sup": None
            },
            "refs": {}
        }

    def exportar(self, data):
        self.data.clear()
        self.data['fondo'] = data['ruta_fondo']
        self.data['colisiones'] = data['ruta_colisiones']
        for tipo in ['props', 'mobs']:
            for nombre in data[tipo]:
                self.data[tipo][nombre] = list()
                lista = self.data[tipo][nombre]
                for x, y, z, r in data[tipo][nombre]:
                    lista.append([x, y, z, r])

        for item in ['limites', 'refs']:
            for limite in data[item]:
                self.data[item][limite] = data[item][limite]
