class MouseData:
    x = 0
    y = 0
    target = None # el widget bajo el mouse. ok
    #esto es para poder pasarle los datos a otro elemento,
    #o hacer lo que se llama bubbling (o sea, en vez de pass,
    #se llama a click del padre hasta que alguien responde,
    #en caso de elementos anidados)
    button = 0

class KeyData:
    key = 0
    mods = 0
    target = None
