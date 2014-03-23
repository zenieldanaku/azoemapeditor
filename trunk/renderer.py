from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP,MOUSEMOTION
from pygame import KEYDOWN,KEYUP,K_ESCAPE,QUIT,K_F1
from pygame.sprite import LayeredDirty

class Renderer:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    
    def addWidget(widget,layer=1):
        Renderer.contents.add(widget,layer=layer)
        Renderer.widgets[widget.nombre] = widget
        return widget
    
    def delWidget(widget):
        if isinstance(widget,str):
            widget = Renderer.widgets[widget]
        widget.onDestruction()
        Renderer.contents.remove(widget)
        del Renderer.widgets[widget.nombre]
    
    def setFocus(widget):
        if widget!=Renderer.currentFocus and widget!=None:
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
                elif event.key == K_F1:
                    i = 0
                    print('--Inicio de lista')
                    for widget in Renderer.contents:
                        i+=1
                        print(widget.nombre)
                    print('--Fin de lista')
                    print('Nº Total de widgets: '+str(i))
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
                                if widget.focusable:
                                    foundWidget = widget
                
                    Renderer.setFocus(foundWidget)
                    
                if Renderer.currentFocus.enabled:
                    Renderer.currentFocus.onMouseDown(event.button)
                
            elif event.type == MOUSEBUTTONUP:    
                Renderer.currentFocus.onMouseUp(event.button)
                
            elif event.type == MOUSEMOTION:
                for widget in Renderer.contents:
                    if widget.rect.collidepoint(event.pos):
                        if not widget.hasMouseOver:
                            widget.onMouseIn()
                            if widget.setFocus_onIn:
                                Renderer.setFocus(widget)
                    else:
                        if widget.hasMouseOver:
                            widget.onMouseOut()
                    
        for widget in Renderer.contents:
            if widget.hasMouseOver:
                widget.onMouseOver()
                
        Renderer.contents.update()
        return Renderer.contents.draw(fondo)