from globales import GLOBALES as G, Resources as r
from widgets import Menu

class Menu_Mapa (Menu):
    def  __init__(self,x,y,barra):
        self.nombre = 'Menu Mapa'
        self.barra = barra
        cascadas = {
            'imagen':[
                {'nom':'Fondo','cmd':self.Set_imagen_fondo},
                {'nom':'Colisiones','cmd':self.Set_imagen_colisiones}]
        }
        opciones = [{'nom':'Grilla...','cmd':self.Grilla},
                   {'nom':'Capas...','cmd':self.Capas},
                   {'nom':'Imagen >','csc':cascadas['imagen']}]
        super().__init__('Mapa',opciones,x,y)

    def Grilla(self):
        print('grilla')
    
    def Capas(self):
        print('capas')
    
    def _cargar_imagen(self):
        try:
            imagen = r.cargar_imagen(G.ruta)
            return imagen
        except Exception as Description:
            G.estado = str(Description)
    
    def Set_imagen_fondo(self):
        imagen = self._cargar_imagen()
        G.IMG_actual = 'Fondo'
        G.IMG_fondo = imagen
        
    def Set_imagen_colisiones(self):
        imagen = self._cargar_imagen()
        G.IMG_actual = 'Colisiones'
        G.IMG_colisiones = imagen
        
        