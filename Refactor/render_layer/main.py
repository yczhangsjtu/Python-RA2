import pygame
from element import Element
from elements_scene import ElementsScene


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    scene = ElementsScene(600, 400, [
        Element((0, 0), "img/Building/aircmd.png", (282, 0, 282, 243)),
        Element((100, 0), "img/Building/aircmd.png", (282, 0, 282, 243)),
        Element((200, 100), "img/Building/aircmd.png", (282, 0, 282, 243)),
        Element((200, 200), "img/Building/aircmd.png", (282, 0, 282, 243)),
        Element((300, 200), "img/Building/aircmd.png", (282, 0, 282, 243)),
        Element((400, 300), "img/Building/aircmd.png", (282, 0, 282, 243)),
    ])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        scene.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()