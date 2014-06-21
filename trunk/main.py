from pygame import display as pantalla,time
from renderer import Renderer
from widgets import Ventana
from constantes import C
from rundata import *
import pygame,sys,os

pygame.init()
tamanio = 20*C+8,18*C-7
os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0,0)
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
