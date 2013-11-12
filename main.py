import pygame,sys
from pygame import display as pantalla

pygame.init()
C = 32
tamanio = 24*C,20*C
pantalla.set_caption("MapGen")
fondo = pantalla.set_mode(tamanio)

gris = pygame.Color(125,125,125)
grilla_rect = pygame.Rect(((2*C)+2,2*C),(16*C,16*C))
herramientas = pygame.Rect((0,2*C),(2*C,16*C))
panel = pygame.Rect(((19*C),2*C),(5*C,16*C))
barra_V = pygame.Rect(((18*C)+5,2*C),(round(1/2*C),16*C))
cursor_V = pygame.Rect(((18*C)+5,10*C),(round(1/2*C),1/2*C))
barra_H = pygame.Rect(((2*C)+2,(18*C)+5),(16*C,round(1/2*C)))
cursor_H = pygame.Rect((10*C,(18*C)+5),(1/2*C,round(1/2*C)))
estado = pygame.Rect((0,(19*C)-2),(24*C,1*C))
menu_1 = pygame.Rect((0,0),(24*C,1*C))
menu_2 = pygame.Rect((0,C),(24*C,1*C))

c_H_press = False
c_V_press = False

FPS = pygame.time.Clock()

fondo.fill(gris)
pygame.draw.rect(fondo, (255,255,255), barra_V)
pygame.draw.rect(fondo, (255,255,255), barra_H)
pygame.draw.rect(fondo, (125,0,125),cursor_H)
pygame.draw.rect(fondo, (125,0,125),cursor_V)

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
                if cursor_H.collidepoint(x,y): 
                    c_H_press = True
                elif cursor_V.collidepoint(x,y):
                    c_V_press = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(x/32)*C+5
                y = int(y/32)*C+5
                if barra_V.collidepoint(x,y):
                    if c_V_press:
                        pygame.draw.rect(fondo, (255,255,255), barra_V)
                        _cursor_V = pygame.Rect((x,y),cursor_V.size)
                        fondo.fill((125,0,125),(_cursor_V))
                        cursor_V = _cursor_V
                elif barra_H.collidepoint(x,y):
                    if c_H_press:
                        pygame.draw.rect(fondo, (255,255,255), barra_H)
                        _cursor_H = pygame.Rect((x,y),cursor_H.size)
                        fondo.fill((125,0,125),((x,y),cursor_H.size))
                        fondo.fill((125,0,125),(_cursor_H))
                        cursor_H = _cursor_H
                
        
    pygame.draw.rect(fondo, (0,0,0), grilla_rect, 2)
    pygame.draw.rect(fondo, (0,0,0), herramientas, 2)
    pygame.draw.rect(fondo, (0,0,0), panel, 2)
    pygame.draw.rect(fondo, (0,0,0), estado, 2)
    pygame.draw.rect(fondo,(0,0,0),menu_1,2)
    pygame.draw.rect(fondo,(0,0,0),menu_2,2)
    pantalla.flip()