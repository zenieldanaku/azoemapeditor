from pygame import Color

import os
try:
    import ctypes
    ##http://msdn.microsoft.com/en-us/library/windows/desktop/ms724371%28v=vs.85%29.aspx
    gc = ctypes.windll.user32.GetSysColor
    #esta funcion esta porque pygame tira un error con 0x0
    hexa = lambda num: Color('0x'+hex(gc(num))[2:].rjust(6,'0'))
    
    sysElmFace =          hexa(15)    #color de frente de elementos
    sysElmShadow =        hexa(16)    #color del borde de abajo de elementos 3D (botones, etc)    
    sysElmLight =         hexa(20)    #color del borde de arriba de elementos 3D
    sysElmText =          hexa(18)    #color de texto de elementos
    sysDisText =          hexa(17)    #color de texto deshabilitado
    sysBoxBack =          hexa(5)     #color para el fondo de cuadros (de texto, etc)
    sysBoxBorder =        hexa(6)     #color de borde de cuadros
    sysBoxText =          hexa(8)     #color de texto de cuadros
    sysBoxSelBack =       hexa(13)    #color de fondo de seleccion en cuadros
    sysBoxSelText =       hexa(14)    #color de text de seleccion en cuadros
    sysMenBack =          hexa(4)     #color de fondo de los menus
    sysMenText =          hexa(7)     #color de texto en menus
    sysScrBack =          hexa(0)     #color de fondo de la barras de scroll
    sysScrArrow =         hexa(9)     #color de las flechas de barras de scroll
except:
    sysElmFace = Color   (*[125]*3)   #color de frente de elementos
    sysElmShadow = Color (*[100]*3)   #color del borde de abajo de elementos 3D (botones, etc)
    sysElmLight = Color  (*[150]*3)   #color del borde de arriba de elementos 3D
    sysElmText = Color   (*[0]*3)     #color de texto de elementos
    sysDisText = Color   (153,168,172)#color de texto deshabilitado
    sysBoxBack = Color   (*[255]*3)   #color para el fondo de cuadros (de texto, etc)
    sysBoxBorder = Color (*[100]*3)   #color de borde de cuadros
    sysBoxText = Color   (*[125]*3)   #color de texto de cuadros
    sysBoxSelBack = Color(*[230]*3)   #color de fondo de seleccion en cuadros
    sysBoxSelText = Color(*[0]*3)     #color de text de seleccion en cuadros
    sysMenBack = Color   (*[125]*3)   #color de fondo de los menus
    sysMenText = Color   (*[0]*3)     #color de texto en menus
    sysScrBack = Color   (*[205]*3)   #color de fondo de la barras de scroll
    sysScrArrow = Color  (*[70]*3)     #color de las flechas de barras de scroll
    
def color(color):
    if isinstance(color, str):
        if color.startswith('#'):
            return Color(color)
        elif color in globals():
            return globals()[color]
        else:
            raise ValueError('Color no reconocido' + color)
    else: #suponemos un array rgb
        return Color(*color)