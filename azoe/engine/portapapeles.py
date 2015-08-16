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
        if item is not None:
            if hasattr(destino, "pegar"):
                destino.pegar(item)
            elif hasattr(destino,"paste"):
                destino.paste(item)
            elif hasattr(destino, __repr__) and hasattr(item, __repr__):
                raise TypeError(str(destino) + "cannot 'paste'"+str(item))
            else:
                raise TypeError()
    
    def __repr__(self):
        return 'item: '+str(self._item)+' ('+str(self._tipo)+')'
    