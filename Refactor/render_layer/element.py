import pygame

class Element:
    """
    The basic element to draw on the screen.
    """
    cached_sprite_sheets = {}
    def __init__(self, position, sprite_sheet, area):
        self.position = position
        if sprite_sheet in Element.cached_sprite_sheets:
            self._sprite_sheet = Element.cached_sprite_sheets[sprite_sheet]
        else:
            self._sprite_sheet = pygame.image.load(sprite_sheet)
            Element.cached_sprite_sheets[sprite_sheet] = self._sprite_sheet
        self.area = area

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @property
    def width(self):
        return self.area[2]

    @property
    def height(self):
        return self.area[3]

    @property
    def left_x(self):
        return self.position[0]

    @property
    def right_x(self):
        return self.position[0] + self.width

    @property
    def top_y(self):
        return self.position[1]

    @property
    def bottom_y(self):
        return self.position[1] + self.height

    def draw(self, screen, offset):
        screen.blit(self.sprite_sheet,
                    (self.position[0]+offset[0], self.position[1]+offset[1]),
                    self.area)