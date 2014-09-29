from pygame import display as pantalla,time
from globales import EventHandler, ANCHO,ALTO
from widgets import Ventana
from rundata import *
import pygame,sys,os

rutas = [os.getcwd()+'\\proyectos',
         os.getcwd()+'\\assets',
         os.getcwd()+'\\export']

for ruta in rutas:
    if not os.path.exists(ruta):
        os.mkdir(ruta)

pygame.init()
tamanio = ANCHO,ALTO
os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0,0)
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)
BarraMenus = barraMenus()
BarraEstado = barraEstado()
Grilla = Grilla()
Simbolos = PanelSimbolos()
Ventana(fondo.get_size())

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
