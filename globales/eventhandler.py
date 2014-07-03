from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP,MOUSEMOTION
from pygame import KEYDOWN,KEYUP,K_ESCAPE,QUIT,K_F1
from pygame.sprite import LayeredDirty

class EventHandler:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    
    @staticmethod
    def addWidget(widget,layer=1):
        EventHandler.contents.add(widget,layer=layer)
        EventHandler.widgets[widget.nombre] = widget
        return widget
    
    @staticmethod
    def delWidget(widget):
        if isinstance(widget,str):
            widget = EventHandler.widgets[widget]
        widget.onDestruction()
        EventHandler.contents.remove(widget)
        if widget.nombre in EventHandler.widgets:
            del EventHandler.widgets[widget.nombre]
    
    @staticmethod
    def getWidget(widget):
        if isinstance(widget,str):#suponemos que es su nombre
            widget = EventHandler.widgets[widget]
        return widget
    
    @staticmethod
    def setFocus(widget):
        if widget!=EventHandler.currentFocus and widget!=None:
            EventHandler.currentFocus.onFocusOut()
            EventHandler.currentFocus = widget
            EventHandler.currentFocus.onFocusIn()
    
    @staticmethod
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
                    for widget in EventHandler.contents:
                        i+=1
                        print(widget.nombre)
                    print('--Fin de lista')
                    print('Nº Total de widgets: '+str(i))
                else:
                    EventHandler.currentFocus.onKeyDown(event)
                
            elif event.type == KEYUP:
                EventHandler.currentFocus.onKeyUp(event)
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    foundWidget = None
                    for widget in EventHandler.contents:
                        if widget._visible:
                            if widget.rect.collidepoint(event.pos):
                                if widget.focusable:
                                    foundWidget = widget
                
                    EventHandler.setFocus(foundWidget)
                    
                if EventHandler.currentFocus.enabled:
                    EventHandler.currentFocus.onMouseDown(event.button)
                
            elif event.type == MOUSEBUTTONUP:    
                EventHandler.currentFocus.onMouseUp(event.button)
                
            elif event.type == MOUSEMOTION:
                for widget in EventHandler.contents:
                    if widget.rect.collidepoint(event.pos):
                        if not widget.hasMouseOver:
                            widget.onMouseIn()
                            if widget.setFocus_onIn:
                                EventHandler.setFocus(widget)
                    else:
                        if widget.hasMouseOver:
                            widget.onMouseOut()
                    
        for widget in EventHandler.contents:
            if widget.hasMouseOver:
                widget.onMouseOver()
        
        EventHandler.contents.update()
        return EventHandler.contents.draw(fondo)