from .basemenu import BaseMenu

class Menu_Archivo(BaseMenu):
    def  __init__(self,x,y):
        self.nombre = 'Menu Archivo'
        nombres = ['Nuevo','Abrir...','Guardar','Guardar como...','Cerrar']
        super().__init__(nombres,x,y)
        
    
    def Nuevo(self):
        pass
    def Abrir(self):
        pass
    def Guardar(self):
        pass
    def Guardar_como(self):
        pass
    def Cerrar(self):
        pass