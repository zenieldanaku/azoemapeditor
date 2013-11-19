from pygame.sprite import LayeredDirty
from pygame import KEYDOWN, KEYUP,\
MOUSEBUTTONDOWN, MOUSEBUTTONUP,MOUSEMOTION,QUIT,mouse,K_ESCAPE

class Renderer:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    mouse_move_wigets = []
          
    def addWidget(widget,layer=1):
        Renderer.contents.add(widget,layer=layer)
        Renderer.widgets[widget.nombre] = widget
        return widget
    
    #def delWidget(widget):
    #    if widget in Renderer.contents:
    #        Renderer.contents.remove(widget)
    #        del Renderer.widgets[widget.nombre]
    
    def registerForMouseMove(self,widget):
        self.mouse_move_wigets.append(widget)
    
    def setFocus(widget):
        if widget!=Renderer.currentFocus and widget.focusable:
            Renderer.currentFocus.onFocusOut()
            Renderer.currentFocus = widget
            Renderer.currentFocus.onFocusIn()
    
    def update(events,fondo):
        args = None
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                else:
                    args = Renderer.currentFocus.onKeyDown(event)
                
            elif event.type == KEYUP:
                args = Renderer.currentFocus.onKeyUp(event)
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    foundWidget = None
                    for widget in Renderer.contents:
                        if widget.rect.collidepoint(event.pos):
                            foundWidget = widget
                    Renderer.setFocus(foundWidget)
                    
                args = Renderer.currentFocus.onMouseDown(event)
                
            elif event.type == MOUSEBUTTONUP:    
                args = Renderer.currentFocus.onMouseUp(event)
                
            elif event.type == MOUSEMOTION:
                for widget in Renderer.contents:
                    if widget.rect.collidepoint(event.pos):
                        widget.onMouseOver(event)

        ret = Renderer.contents.draw(fondo)
        #if args != None:
        #    ret.append(fondo.blit(*args))
        return ret