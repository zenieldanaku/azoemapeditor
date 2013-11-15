from pygame.sprite import LayeredDirty

class Renderer:
    contents = None
    widgets = {}
    
    def __init__(self):
        self.contents = LayeredDirty()
        self.widgets = {}
        
    def addWidget(self,widget,layer=0):
        self.contents.add(widget,layer=layer)
        self.widgets[widget.nombre] = widget
        return widget
    
    def update(self,events,fondo):
        for widget in self.contents:
            if widget.hasFocus:
                args = widget.update(events)

        ret = self.contents.draw(fondo)
        if args != None:
            ret.append(fondo.blit(*args))
        return ret

render_engine = Renderer()