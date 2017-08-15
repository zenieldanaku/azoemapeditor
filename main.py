from pygame import display as pantalla, time
from azoe.engine.resources import Resources
from azoe import EventHandler, Ventana
from globales import ANCHO, ALTO
from globales import Sistema
from rundata import *
import pygame
import sys
import os

rutas = [os.getcwd() + '\\proyectos',
         os.getcwd() + '\\assets',
         os.getcwd() + '\\export']

for ruta in rutas:
    if not os.path.exists(ruta):
        os.mkdir(ruta)

pygame.init()
tamanio = ANCHO, ALTO
os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)
pantalla.set_caption("Azoe Engine's Map Editor")
fondo = pantalla.set_mode(tamanio)
config = Resources.abrir_json('config/config.json')
try:
    opciones = Resources.abrir_json(config['use_colors'])

except (IOError, KeyError):
    opciones = {}

Sistema.init(**opciones)
Ventana(fondo.get_size(), **opciones)
BarraMenus = BarraMenus(**opciones)
BarraEstado = BarraEstado(**opciones)
Simbolos = PanelSimbolos(**opciones)
Grilla = Grilla(**opciones)

hayCambios = True
FPS = time.Clock()
while hayCambios:
    FPS.tick(60)
    events = pygame.event.get()
    hayCambios = EventHandler.update(events, fondo)

    if hayCambios:
        pantalla.update(hayCambios)
    Sistema.update()
pygame.quit()
sys.exit()
