# este es el objeto de trabajo, no sé donde ponerlo.

class Mapa:
    script = {}
    
    def __init__(self):
        self.script= {
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
    
    def guardar(self):
        return self.script
    
    def cargar(self,data):
        self.script.update(data)

class Proyecto:
    script = {}
    
    def __init__(self,data):
        self.script= {
            "referencias":{'fd_fondo':data['fondo'],
                           'fd_colisiones':data['colisiones'],
                           'fd_props':data['props'],
                           'fd_mobs':data['mobs']},
            "fondo":"",
            "colisiones":"",
            "props": {},
            "mobs": {},
            "entradas":{},
            "salidas":{},
            "refs":{},
            "ambiente":data['ambiente']
        }
    def __setitem__(self,key,value):
        if key in self.script:
            self.script[key] = value
            
    def guardar(self):
        return self.script
    
    def cargar(self,data):
        self.script.update(data)
    
    def exportar(self):
        pass
        