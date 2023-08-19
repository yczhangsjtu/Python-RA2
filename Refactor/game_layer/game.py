import pygame

class Game:
    def __init__(self, width, height, frame_rate):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.systems = []
        self.frame_rate = frame_rate

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.time.wait(int(1000 / self.frame_rate))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            for system in self.systems:
                system.handle_event(event)

    def update(self):
        for system in self.systems:
            system.update()
        # If any system sets its quit bit, remove this system from
        # the game's list of systems.
        self.systems = [system for system in self.systems if not system.quit]

        # If any system produces a new system, append the new system
        # to the game's list of systems.
        systems_to_append = []
        for system in self.systems:
            if system.has_new_system():
                systems_to_append.append(system.new_system())
                system.clear_new_system()
        self.systems.extend(systems_to_append)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for system in self.systems:
            if system.visible():
                system.draw(self.screen)
        pygame.display.flip()