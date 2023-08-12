import pygame
from element import Element


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    element = Element((0, 0), "img/Building/aircmd.png", (0, 0, 282, 243))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((255, 255, 255))
        element.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()