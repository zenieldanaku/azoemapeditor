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
                "mobs": {
                    "enemies":{},
                    "npcs":{}
                }
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
    
    def actualizar(self,dicc):
        key = dicc['key']
        value = dicc['value']
        for k in self.script:
            if k == key:
                self.script[key]= value
            elif key in self.script[k]:
                self.script[k][key] = value
        