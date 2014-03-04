from pygame import display as pantalla,time
from renderer import Renderer
from widgets import Ventana
from constantes import C
from rundata import *
import pygame,sys,os

pygame.init()
tamanio = 24*C,20*C
os.environ['SDL_VIDEO_WINDOW_POS'] = "{!s},{!s}".format(50,50)
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)
ventana = Renderer.addWidget(Ventana(fondo.get_size()),0)
Renderer.currentFocus = ventana
ventana.onFocusIn()

hayCambios = True
FPS = time.Clock()
while hayCambios:
    FPS.tick(60)
    events = pygame.event.get()
    hayCambios = Renderer.update(events,fondo)
    if hayCambios:
        pantalla.update(hayCambios)

pygame.quit()
sys.exit()