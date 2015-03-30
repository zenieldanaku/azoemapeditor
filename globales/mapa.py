class Proyecto:
    rutas = None #{}
    script = None#{}
    mapa = None  #{}
    def __init__(self,data):
        self.rutas = {'fondo':data['fondo'],
                      'colisiones':data['colisiones'],
                      'props':data['props'],
                      'mobs':data['mobs']}
        self.script= {
            "fondo":"",
            "colisiones":"",
            "props": {},
            "mobs": {},
            "entradas":{},
            "salidas":{},
            "refs":{},
            "ambiente":data['ambiente']
        }
        self.mapa = {
            "capa_background":{
                "fondo":"",
                "colisiones":""
            },
            "capa_ground":{
                "props": {},
                "mobs": {}
            },
            "capa_top":{
                "props":{}
            },
            "entradas":{
            },
            "salidas":{
            },
            "refs":{},
            "ambiente":""
        }

    def cargar(self,data):
        for key in data:
            if key in self.script:
                self.script[key] = data[key]
            elif key.startswith('fd_'):
                self.rutas[key[3:]] = data[key]
                
    def guardar(self, ):
        d = self.script.copy()
        for key in self.rutas:
            d['fd_'+key] = self.rutas[key]
        
        return d
    
    def updateItemPos(self,tile):
        nombre = tile._nombre
        grupo = tile.grupo
        index = tile.index
        x,y = tile.rect.topleft
        layer = tile.layer
        rot = tile.rot
        
        self.script[grupo][nombre][index] = x,y,layer,rot

    def addRef(self,nombre,ruta,code):
        if nombre not in self.script['refs']:
            self.script['refs'][nombre] = {'ruta':ruta,'code':code}
    
    def addEntrada(self,nombre,px,py):
        if nombre not in self.script['entradas']:
            self.script['entradas'][nombre] = {'x':px,'y':py}
        
    def addItem(self,datos):
        nombre = datos['nombre']
        ruta = datos['ruta']
        grupo = datos['grupo']
        code = datos['cols_code']
        
        root = self.script[grupo]
        if nombre not in root:
            root[nombre] = [[]]
            index = 0
            self.addRef(nombre,ruta,code)
        else:
            if self.script['refs'][nombre]['code'] == code:
                root[nombre].append([])
                index = len(root[nombre])-1
            else:
                nombre+='_'+str(len(self.script['refs']))
                data = {'nombre':nombre,'ruta':ruta,'grupo':grupo,'cols_code':code}
                index = self.addItem(data)
                
        return index
    
    def exportarMapa(self):
        from os import path
        self.mapa['ambiente'] = self.script['ambiente']
        for layer in ['fondo','colisiones']:
            ruta = self.rutas[layer]+path.split(self.script[layer])[1]
            self.mapa['capa_background'][layer]= ruta
        
        for tipo in ['props','mobs']:
            for item in self.script[tipo]:
                self.mapa['capa_ground'][tipo][item] = []
                for x,y,z,r in self.script[tipo][item]:
                    self.mapa['capa_ground'][tipo][item].append([x,y])
                
                ruta = path.split(self.script['refs'][item]['ruta'])[1]
                self.mapa['refs'][item] = self.rutas[tipo]+ruta
        
        for nombre in self.script['entradas']:
            x = self.script['entradas'][nombre]['x']
            y = self.script['entradas'][nombre]['y']
            self.mapa['entradas'][nombre] = [int(x),int(y)]
        
        return self.mapa.copy()