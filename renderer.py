from pygame.sprite import LayeredDirty
from pygame import KEYDOWN, KEYUP,\
MOUSEBUTTONDOWN, MOUSEBUTTONUP,MOUSEMOTION,QUIT,K_ESCAPE

class Renderer:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    mouse_move_wigets = []
    
    def addWidget(widget,layer=1):
        Renderer.contents.add(widget,layer=layer)
        Renderer.widgets[widget.nombre] = widget
        return widget
    
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
                    Renderer.currentFocus.onKeyDown(event)
                
            elif event.type == KEYUP:
                Renderer.currentFocus.onKeyUp(event)
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    foundWidget = None
                    for widget in Renderer.contents:
                        if widget._visible:
                            if widget.rect.collidepoint(event.pos):
                                foundWidget = widget
                    Renderer.setFocus(foundWidget)

                if Renderer.currentFocus.enabled:
                    Renderer.currentFocus.onMouseDown(event.button)
                
            elif event.type == MOUSEBUTTONUP:    
                Renderer.currentFocus.onMouseUp(event.button)
                
            elif event.type == MOUSEMOTION:
                for widget in Renderer.contents:
                    if widget.rect.collidepoint(event.pos):
                        widget.onMouseOver()
                    else:
                        widget.onMouseOut()
        
        Renderer.contents.update()        
        return Renderer.contents.draw(fondo)