import pygame
from Refactor.render_layer.elements_scene import ElementsScene
from sprite import Sprite, SpriteData

FRAME_RATE = 12

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    sprite = Sprite(SpriteData("Refactor/data/aircmd.json"))
    sprite.set_pos(0, 0)
    sprite.set_state("red_create")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        scene = ElementsScene(600, 400, [
            sprite.generate_render_element(),
        ])
        scene.draw(screen)
        sprite.next_frame()

        pygame.display.flip()
        pygame.time.wait(1000//FRAME_RATE)

if __name__ == "__main__":
    main()