from pygame import Color

gris = Color(*[125]*3)
gris_seleccion = Color(*[230]*3)
gris_oscuro_bisel = Color(*[100]*3)
gris_claro_bisel = Color(*[150]*3)
blanco = Color(255,255,255)
negro = Color(0,0,0)
violeta = Color(125,0,125)
verde = Color(0,255,0)
rojo = Color(255,0,0)
azul = Color(0,0,255)
cian_oscuro = Color(150,200,200)
cian_claro = Color(125,255,255)

import os
try:
    import ctypes
    ##http://msdn.microsoft.com/en-us/library/windows/desktop/ms724371%28v=vs.85%29.aspx
    gc = ctypes.windll.user32.GetSysColor
    #esta funcion esta porque pygame tira un error con 0x0
    def hexa(num):
        if num == 0:
            return '0x000000'
        else:
            return hex(num)
    ##color de frente de elementos
    sysElmFace = Color(hexa(gc(15)))
    ##color del borde de abajo de elementos 3D (botones, etc)
    sysElmShadow = Color(hexa(gc(16)))
    ##color del borde de arriba de elementos 3D
    sysElmLight = Color(hexa(gc(20)))
    ##color de texto de elementos
    sysElmText = Color(hexa(gc(18)))
    ##color para el fondo de cuadros (de texto, etc)
    sysBoxBack = Color(hexa(gc(5)))
    ##color de borde de cuadros
    sysBoxBorder = Color(hexa(gc(6)))
    ##color de texto de cuadros
    sysBoxText = Color(hexa(gc(8)))
    ##color de fondo de seleccion en cuadros
    sysBoxSelBack = Color(hexa(gc(13)))
    ##color de text de seleccion en cuadros
    sysBoxSelText = Color(hexa(gc(14)))
    ##color de fondo de los menus
    sysMenBack = Color(hexa(gc(4)))
    ##color de texto en menus
    sysMenText = Color(hexa(gc(7)))
    ##color de fondo de la barras de scroll
    sysScrBack = Color(hexa(gc(0)))
    ##color de las flechas de barras de scroll
    sysScrArrow = Color(hexa(gc(9)))
except:
    ##color de frente de elementos
    sysElmFace = gris
    ##color del borde de abajo de elementos 3D (botones, etc)
    sysElmShadow = gris_oscuro_bisel
    ##color del borde de arriba de elementos 3D
    sysElmLight = gris_claro_bisel
    ##color de texto de elementos
    sysElmText = negro
    ##color para el fondo de cuadros (de texto, etc)
    sysBoxBack = blanco
    ##color de borde de cuadros
    sysBoxBorder = gris_oscuro_bisel
    ##color de texto de cuadros
    sysBoxText = gris
    ##color de fondo de seleccion en cuadros
    sysBoxSelBack = gris_seleccion
    ##color de text de seleccion en cuadros
    sysBoxSelText = negro
    ##color de fondo de los menus
    sysMenBack = gris
    ##color de texto en menus
    sysMenText = negro
    ##color de fondo de la barras de scroll
    sysScrBack = Color(205,205,205)
    ##color de las flechas de barras de scroll
    sysScrArrow = Color(70,70,70)
    

def color(color):
    if isinstance(color, str):
        if color[0] == '#':
            return Color(color)
        elif color in globals():
            return globals()[color]
        else:
            raise ValueError('Color no reconocido' + color)
    else: #suponemos un array rgb
        return Color(*color)