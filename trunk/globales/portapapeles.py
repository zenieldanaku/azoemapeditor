class Portapapeles:
    _item = None
    _tipo = None
    def __init__(self):
        self._item = None
        self._tipo = None
    
    def cortar(self,item):
        self._tipo = 'cut'
        self._item = item
    
    def copiar(self,item):
        self._tipo = 'copy'
        self._item = item
        
    def pegar(self,destino):
        item = self._item
        if self._tipo == 'cut':
            self._item = None
            self._tipo = None
        if item != None:
            destino.pegar(item)
    
    def __repr__(self):
        return 'item: '+str(self._item)+' ('+str(self._tipo)+')'
    