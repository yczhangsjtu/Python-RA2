import pygame
from Refactor.render_layer.elements_scene import ElementsScene
from sprite import Sprite, SpriteData


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    sprite = Sprite(SpriteData("Refactor/data/aircmd.json"))
    sprite.set_pos(0, 0)
    scene = ElementsScene(600, 400, [
        sprite.generate_render_element(),
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