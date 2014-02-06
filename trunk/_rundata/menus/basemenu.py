from widgets import PullDownMenu

class BaseMenu (PullDownMenu):
    visible = 0
    nombre = ''
    def __init__(self,nombres,x,y):
        super().__init__(nombres,x,y)
        self.visible = 0