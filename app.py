from typing import Tuple

import pygame

# Initialize Pygame
pygame.init()

# Full-screen display mode
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

fading = False
fade_alpha = 0
new_image = None


# Load image function
def load_image(path: str, size: Tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(pygame.image.load(path), size)


# Show new image with fade effect
def show_new_image(new_image_path: str) -> None:
    new_image = load_image(new_image_path, (infoObject.current_w, infoObject.current_h))
    for alpha in range(0, 255, 2):
        new_image.set_alpha(alpha)
        screen.blit(new_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)  # Adjust delay for smoother fade effect


# Function to initiate fade effect
def initiate_fade(new_image_path: str) -> None:
    global fade_alpha, fading, new_image
    fade_alpha = 0  # Reset alpha to 0
    fading = True  # Start fading
    new_image = load_image(new_image_path, (infoObject.current_w, infoObject.current_h))


def display_recording_text() -> None:
    font_size = 40
    text = "RECORDING AUDIO"
    position = (75, 45)
    if pygame.time.get_ticks() % 1500 > 500:
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topleft=position)
        pygame.draw.circle(screen, (255, 0, 0), (text_rect.left - 25, text_rect.centery), 15)
        screen.blit(text_surf, text_rect)


def display_text(text: str, position: Tuple[int, int], font_size: int = 30, visible: bool = True) -> None:
    font = pygame.font.Font(None, font_size)
    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, position)


# Main function to run the game loop
def main():
    global fade_alpha, fading, new_image
    running = True
    visible = True
    background_image_path = 'images/example_image.jpg'
    background_image = load_image(background_image_path, (infoObject.current_w, infoObject.current_h))
    screen.blit(background_image, (0, 0))

    # blink_event = pygame.USEREVENT + 1
    # pygame.time.set_timer(blink_event, 1000)  # ms

    i = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    initiate_fade(f'images/example_{i}.png')
                    i += 1
            # elif event.type == blink_event:
            #     visible = not visible

        # Fade effect logic
        if fading:
            if fade_alpha < 255:
                fade_alpha += 5  # Increment alpha
                if new_image is not None:
                    new_image.set_alpha(fade_alpha)
                    screen.blit(background_image, (0, 0))  # Draw the old image
                    screen.blit(new_image, (0, 0))  # Draw the new image on top with increasing alpha
                    display_recording_text()
                pygame.display.flip()
            else:
                fading = False  # Stop fading
                background_image = new_image  # Set new image as the background

        if not fading:
            screen.blit(background_image, (0, 0))
            display_recording_text()
            pygame.display.flip()

        # pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
