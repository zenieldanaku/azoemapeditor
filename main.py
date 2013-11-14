import pygame,sys
from pygame import display as pantalla,draw,time
from widgets import Barra,Grilla,Ventana
from constantes import *

pygame.init()
tamanio = 24*C,20*C
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)

ventana = pygame.Rect((0,0),fondo.get_size())
grilla = Grilla((2*C)+2,2*C,15*C,15*C)
barra_V = Barra((17*C)+5, 2*C, 1/2*C, grilla.h)
barra_H = Barra((2*C)+2, (17*C)+5, grilla.w, 1/2*C)

herramientas = pygame.Rect((0,2*C),(2*C,16*C))
panel = pygame.Rect(((18*C),2*C),(6*C,16*C))

estado = pygame.Rect((0,(19*C)-2),(24*C,1*C))
menu_1 = pygame.Rect((0,0),(24*C,1*C))
menu_2 = pygame.Rect((0,C),(24*C,1*C))
menu_3 = pygame.Rect((0,(18*C)),(24*C,1*C))

FPS = time.Clock()

fondo.fill(gris)

while True:
    FPS.tick(60)
    events = pygame.event.get()
    
    
    barra_H.event_handler(events)
    barra_V.event_handler(events)
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    fondo.blit(grilla.image,(64,64))
    fondo.blit(barra_V.image,barra_V.rect)
    fondo.blit(barra_H.image,barra_H.rect)
    
    draw.rect(fondo,(0,0,0), herramientas, 2)
    draw.rect(fondo,(0,0,0), panel, 2)
    draw.rect(fondo,(0,0,0), estado, 2)
    draw.rect(fondo,(0,0,0),menu_1,2)
    draw.rect(fondo,(0,0,0),menu_2,2)
    draw.rect(fondo,(0,0,0),menu_3,2)
    pantalla.update()
    #cambios = 
    #pantalla.update(cambios)
    
