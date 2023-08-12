import pygame

class Element:
    """
    The basic element to draw on the screen.
    """
    def __init__(self, position, sprite_sheet, area):
        self.position = position
        self._sprite_sheet = pygame.image.load(sprite_sheet)
        self.area = area

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    def draw(self, screen):
        screen.blit(self.sprite_sheet, self.position, self.area)