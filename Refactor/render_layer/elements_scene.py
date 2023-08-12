import pygame

class ElementsScene:
    def __init__(self, width, height, elements):
        self.width = width
        self.height = height
        self.elements = elements

    def draw(self, screen):
        screen.fill((255, 255, 255))
        total_width = screen.get_width()
        total_height = screen.get_height()

        for element in self.elements:
            if element.right_x < 0 or element.left_x >= self.width or element.bottom_y < 0 or element.top_y >= self.height:
                continue
            element.draw(screen)

        # Cover the parts that are outside of the scene
        if total_width > self.width:
            side_width = (total_width - self.width) // 2
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, side_width, total_height))
            pygame.draw.rect(screen, (0, 0, 0), (total_width - side_width, 0, side_width, total_height))

        if total_height > self.height:
            side_height = (total_height - self.height) // 2
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, total_width, side_height))
            pygame.draw.rect(screen, (0, 0, 0), (0, total_height - side_height, total_width, side_height))

