from pygame import display as pantalla,time
from globales import EventHandler, C
from widgets import Ventana
from rundata import *
import pygame,sys,os

pygame.init()
tamanio = 20*C+8,18*C-19
os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0,0)
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)
BarraMenus = barraMenus()
BarraEstado = barraEstado()
Grilla = Grilla()
Simbolos = PanelSimbolos()
ventana = EventHandler.addWidget(Ventana(fondo.get_size()),0)
EventHandler.currentFocus = ventana
ventana.onFocusIn()

hayCambios = True
FPS = time.Clock()
while hayCambios:
    FPS.tick(20)
    events = pygame.event.get()
    hayCambios = EventHandler.update(events,fondo)
    if hayCambios:
        pantalla.update(hayCambios)

pygame.quit()
sys.exit()
