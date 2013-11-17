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
        if widget in Renderer.contents:
            Renderer.contents.remove(widget)
            del Renderer.widgets[widget.nombre]
    
    def setFocus(widget):
        if widget!=Renderer.currentFocus and widget.focusable:
            Renderer.currentFocus.onFocusOut()
            Renderer.currentFocus = widget
            Renderer.currentFocus.onFocusIn()
    
    def update(events,fondo):
        for widget in Renderer.contents:
            if widget.hasFocus:
                args = widget.update(events)

        ret = Renderer.contents.draw(fondo)
        if args != None:
            ret.append(fondo.blit(*args))
        return ret