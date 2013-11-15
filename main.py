import pygame,sys
from pygame import display as pantalla,time,mouse
from widgets import *
from renderer import render_engine
from constantes import *

pygame.init()
tamanio = 24*C,20*C
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)

add = render_engine.addWidget # function alias

ventana = add(Ventana(fondo.get_size()),0)
grilla = add(Grilla((2*C)+2,2*C,15*C,15*C))
barra_H = add(Barra((17*C)+8, 2*C, 1/2*C, grilla.h))
barra_V = add(Barra((2*C)+2, (17*C)+8, grilla.w, 1/2*C))
herramientas = add(Herramientas(0,2*C,2*C,16*C))
panel = add(PanelSimbolos(18*C-1,2*C,6*C,16*C-1))

botones_1 = ['Archivo','Editar','Mapa']
menu_1 = add(Menu_barra('Menu_1',0,0,24*C,1*C,botones_1))
menu_2 = add(Menu_barra('Menu_2',0,C,24*C,1*C,[]))
menu_3 = add(Menu_barra('Menu_3',0,18*C,24*C,1*C,[]))
estado = add(Menu_barra('estado',0,(19*C),24*C,1*C,[]))

currentFocus = ventana
ventana.onFocusIn()

FPS = time.Clock()
while True:
    FPS.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = mouse.get_pos()
                for widget in render_engine.contents:
                    if widget.rect.collidepoint(mousepos):
                        if widget!=currentFocus and widget.focusable:
                            currentFocus.onFocusOut()
                            currentFocus = widget
                            currentFocus.onFocusIn()
                            print(currentFocus.nombre)
    
    cambios = render_engine.update(events,fondo)
    pantalla.update(cambios)