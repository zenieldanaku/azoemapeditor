import pygame,sys
from pygame import display as pantalla,draw,time
from clases import Grilla, barra_desplazamiento
from constantes import Colores as k, C

pygame.init()
tamanio = 24*C,20*C
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)

grilla = Grilla(((2*C)+2,2*C),(18*C,18*C))
barra_V = barra_desplazamiento((18*C)+5, 2*C, 1/2*C, 16*C)
barra_H = barra_desplazamiento((2*C)+2, (18*C)+5, 16*C, 1/2*C)

herramientas = pygame.Rect((0,2*C),(2*C,16*C))
panel = pygame.Rect(((19*C),2*C),(5*C,16*C))
#barra_V = pygame.Rect(,(round(1/2*C),16*C))
#cursor_V = pygame.Rect(((18*C)+5,10*C),(round(1/2*C),1/2*C))
#barra_H = pygame.Rect(,(16*C,round(1/2*C)))
#cursor_H = pygame.Rect((10*C,(18*C)+5),(1/2*C,round(1/2*C)))
estado = pygame.Rect((0,(19*C)-2),(24*C,1*C))
menu_1 = pygame.Rect((0,0),(24*C,1*C))
menu_2 = pygame.Rect((0,C),(24*C,1*C))

FPS = time.Clock()

fondo.fill(k.gris)
#draw.rect(fondo, k.blanco, barra_V)
#draw.rect(fondo, k.blanco, barra_H)
#draw.rect(fondo, k.violeta,cursor_H)
#draw.rect(fondo, k.violeta,cursor_V)

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
                x,y = pygame.mouse.get_pos()
                x = int(x/32)*C+5
                y = int(y/32)*C+5
                if barra_H.cursor.rect.collidepoint(x,y): 
                    barra_H.cursor.pressed = True
                
                elif barra_V.cursor.rect.collidepoint(x,y):
                    barra_V.cursor.pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(x/32)*C+5
                y = int(y/32)*C+5
                if barra_V.rect.collidepoint(x,y):
                    if barra_V.cursor.pressed:
                        barra_V.cursor.pressed = False
                        barra_V.cursor.reposisionar(x-5,y-5)
                        
                        barra_V.redibujar()
                        #_cursor_V = pygame.Rect((x,y),cursor_V.size)
                        #fondo.fill((125,0,125),(_cursor_V))
                        #cursor_V = _cursor_V
                        
                        pass
                
                elif barra_H.rect.collidepoint(x,y):
                    if barra_H.cursor.pressed:
                        barra_H.cursor.pressed = False
                        barra_H.cursor.reposisionar(x-5,y-5)
                        barra_H.redibujar()
                        #_cursor_H = pygame.Rect((x,y),cursor_H.size)
                        #fondo.fill((125,0,125),((x,y),cursor_H.size))
                        #fondo.fill((125,0,125),(_cursor_H))
                        #cursor_H = _cursor_H
                        #barra_H.cursor.pressed = False
                        pass
    
    fondo.blit(grilla.image,(2,2))
    fondo.blit(barra_V.image,barra_V.rect)
    fondo.blit(barra_H.image,barra_H.rect)
    
    draw.rect(fondo,(0,0,0), herramientas, 2)
    draw.rect(fondo,(0,0,0), panel, 2)
    draw.rect(fondo,(0,0,0), estado, 2)
    draw.rect(fondo,(0,0,0),menu_1,2)
    draw.rect(fondo,(0,0,0),menu_2,2)
    pantalla.update()
    
