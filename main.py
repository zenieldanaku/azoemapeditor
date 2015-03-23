from pygame import display as pantalla,time
from globales import EventHandler, ANCHO,ALTO
from widgets import Ventana
from rundata import *
from globales import Sistema
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
pantalla.set_caption("Azoe Engine's Map Editor")
fondo = pantalla.set_mode(tamanio)
Sistema.init()
Ventana(fondo.get_size())
BarraMenus = barraMenus()
BarraEstado = barraEstado()
Grilla = Grilla()
Simbolos = PanelSimbolos()

hayCambios = True
FPS = time.Clock()
while hayCambios:
    FPS.tick(60)
    events = pygame.event.get()
    hayCambios = EventHandler.update(events,fondo)
    if hayCambios:
        pantalla.update(hayCambios)
    Sistema.update()
pygame.quit()
sys.exit()