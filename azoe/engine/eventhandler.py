from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP,MOUSEMOTION,KEYDOWN,KEYUP
from pygame import K_ESCAPE,QUIT,K_F1,K_F2,K_RCTRL,K_LCTRL,K_RALT,K_LALT,key
from pygame.sprite import LayeredDirty

class EventHandler:
    contents = LayeredDirty()
    widgets = {}
    currentFocus = None
    control = False
    alt = False
    key = None
    
    @classmethod
    def addWidget(cls,widget):
        print(widget)
        cls.contents.add(widget,layer = widget.layer)
        cls.widgets[widget.nombre] = widget
        return widget
    
    @classmethod
    def delWidget(cls,widget):
        if isinstance(widget,str):
            widget = cls.widgets[widget]
        widget.onDestruction()
        cls.contents.remove(widget)
        if widget.nombre in cls.widgets:
            del cls.widgets[widget.nombre]
    
    @classmethod
    def getWidget(cls,widget):
        if isinstance(widget,str):#suponemos que es su nombre
            widget = cls.widgets[widget]
        return widget
    
    @classmethod
    def setFocus(cls,widget):
        if widget!=cls.currentFocus and widget!=None:
            if cls.currentFocus != None:
                cls.currentFocus.onFocusOut()
            cls.currentFocus = widget
            cls.currentFocus.onFocusIn()
    
    @classmethod
    def update(cls,events,fondo):
        args = None
        cls.key = None
        for event in events:
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_RCTRL or event.key == K_LCTRL:
                    cls.control = True
                elif event.key == K_LALT:
                    cls.alt = True
                elif event.key == K_RALT:
                    cls.control = True
                    cls.alt = True    
                elif event.key == K_ESCAPE:
                    return False
                elif event.key == K_F1:
                    i = 0
                    print('--Inicio de lista')
                    for widget in cls.contents:
                        i+=1
                        print(widget.nombre)
                    print('--Fin de lista')
                    print('Nº Total de widgets: '+str(i))
                elif event.key == K_F2:
                    print('--Inicio de lista')
                    layers = cls.contents.layers()
                    for idx in layers:
                        print('\n--Widgets en layer '+str(idx))
                        sprites = cls.contents.get_sprites_from_layer(idx)
                        for widget in sprites:
                            print(widget.nombre)
                    print('--Fin de lista')
                else:
                    cls.key = key.name(event.key)
                cls.currentFocus.onKeyDown(event)
                
            elif event.type == KEYUP:
                if event.key == K_RCTRL or event.key == K_LCTRL:
                    cls.control = False
                elif event.key == K_LALT:
                    cls.alt = False
                elif event.key == K_RALT:
                    cls.control = False
                    cls.alt = False
                else:
                    cls.currentFocus.onKeyUp(event)
                
            elif event.type == MOUSEBUTTONDOWN:
                if event.button in (1,3):
                    foundWidget = None
                    for widget in cls.contents:
                        if widget._visible:
                            if widget.rect.collidepoint(event.pos):
                                if widget.focusable:
                                    foundWidget = widget
                
                    cls.setFocus(foundWidget)
                    
                if cls.currentFocus.enabled:
                    cls.currentFocus.onMouseDown(event.button)
                
            elif event.type == MOUSEBUTTONUP:    
                cls.currentFocus.onMouseUp(event.button)
                
            elif event.type == MOUSEMOTION:
                for widget in cls.contents:
                    if widget.rect.collidepoint(event.pos):
                        if not widget.hasMouseOver:
                            widget.onMouseIn()
                            if widget.setFocus_onIn:
                                cls.setFocus(widget)
                    else:
                        if widget.hasMouseOver:
                            widget.onMouseOut()
                    
        for widget in cls.contents:
            if widget.hasMouseOver:
                widget.onMouseOver()
        
        cls.contents.update()
        return cls.contents.draw(fondo)
