class MainSystem:
    def __init__(self):
        self.quit = False
        self._new_system = None
        self.visible = True

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def has_new_system(self):
        return self._new_system is not None

    def clear_new_system(self):
        self._new_system = None

    def new_system(self):
        return self._new_system