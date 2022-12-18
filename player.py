import json
import pygame

# Initialize pygame
pygame.init()

animations = {}

# Set the window size
window = pygame.display.set_mode((500, 500))

animation_name = None

def load_data(path):
    global window, animations, animation_name
    with open("data/aircmd.json") as f:
        animation_data = json.load(f)

    img = animation_data["img"]

    # Load the sprite sheet and the animation data
    sprite_sheet = pygame.image.load(f"img/{img}")

    # Get the global frame size from the animation data
    frame_width = animation_data["frame_width"]
    frame_height = animation_data["frame_height"]

    # Loop through the animation data and create the animation dictionaries
    animations = {}
    for animation in animation_data["animations"]:
        name = animation["name"]
        frames = []
        for frame in animation["frames"]:
            row = frame["row"]
            col = frame["col"]
            x = col * frame_width
            y = row * frame_height
            frames.append(sprite_sheet.subsurface(
                pygame.Rect(x, y, frame_width, frame_height)))
        animations[name] = frames

    # Set the name of the animation to play
    animation_name = animation_data["animations"][2]["name"]
    pygame.display.set_mode((frame_width, frame_height))


if __name__ == "__main__":
    load_data("data/aircmd.json")
    # Create a variable to keep track of the current frame
    current_frame = 0
    # Set the frame rate
    frame_rate = 12
    # Create a variable to control when the animation should stop
    stop_animation = False
    # Create a clock to control the frame rate
    clock = pygame.time.Clock()
    
    while not stop_animation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("You pressed the right mouse button at (%d, %d)" % event.pos)

        if animation_name is not None:
            # Get the current time
            current_time = pygame.time.get_ticks()
            current_frame = (current_time * frame_rate // 1000) % len(animations[animation_name])

            # Clear the screen
            window.fill((0, 0, 0))

            # Draw the current frame
            window.blit(animations[animation_name][current_frame], (0, 0))

            # Update the display
            pygame.display.update()

        # Wait for the next frame
        clock.tick(12)
